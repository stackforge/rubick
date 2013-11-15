from collections import deque
import logging
import os.path
import paramiko
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException
import re
from recordtype import recordtype
from rubick.common import index, find, path_relative_to, all_subclasses
from rubick.exceptions import ValidatorException
from rubick.model import *
import shlex
import spur
from StringIO import StringIO
import tempfile


def parse_nodes_info(nodes, password=None, private_key=None):
    result = []
    for node in nodes:
        m = parse_nodes_info.connection_re.match(node)
        if not m:
            continue

        username = m.group(1) or 'root'
        host = m.group(2)
        port = int(m.group(3) or '22')

        result.append(
            dict(host=host,
                 port=port,
                 username=username,
                 password=password,
                 private_key=private_key))

    return result

parse_nodes_info.connection_re = re.compile('(?:(\w+)@)?([^:]+)(?::(\d+))?')


def parse_private_key(private_key):
    try:
        return RSAKey.from_private_key(StringIO(private_key))
    except SSHException:
        try:
            return DSSKey.from_private_key(StringIO(private_key))
        except SSHException:
            return None


# SshShell wrapper to add support for sock parameter (for proxy command)
class SshShell(spur.SshShell):

    def __init__(self,
                 hostname,
                 username=None,
                 password=None,
                 port=22,
                 private_key=None,
                 connect_timeout=None,
                 missing_host_key=None,
                 sock=None):
        super(SshShell, self).__init__(hostname=hostname,
                                       username=username,
                                       password=password,
                                       port=port,
                                       connect_timeout=connect_timeout,
                                       missing_host_key=missing_host_key)

        self._pkey = parse_private_key(private_key)
        if not self._pkey:
            raise ValidatorException("Unknown private key format")

        self._sock = sock

    def _connect_ssh(self):
        if self._client is None:
            if self._closed:
                raise RuntimeError("Shell is closed")

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(self._missing_host_key)
            client.connect(
                hostname=self._hostname,
                port=self._port,
                username=self._username,
                password=self._password,
                pkey=self._pkey,
                timeout=self._connect_timeout,
                sock=self._sock)

            self._client = client

        return self._client


class NodeClient(object):
    logger = logging.getLogger('rubick.ssh')

    def __init__(self, host, port=22, username='root', password=None,
                 private_key=None, proxy_command=None):
        super(NodeClient, self).__init__()
        self.use_sudo = (username != 'root')

        if proxy_command and proxy_command.find('%%PATH_TO_KEY%%') != -1:
            self._pkey_file = tempfile.NamedTemporaryFile(suffix='.key')
            self._pkey_file.write(private_key)
            self._pkey_file.flush()

            proxy_command = proxy_command.replace('%%PATH_TO_KEY%%',
                                                  self._pkey_file.name)

        sock = paramiko.ProxyCommand(proxy_command) if proxy_command else None

        self.shell = SshShell(
            hostname=host,
            port=port,
            username=username,
            password=password,
            private_key=private_key,
            missing_host_key=spur.ssh.MissingHostKey.accept,
            sock=sock)

    def run(self, command, *args, **kwargs):
        if self.use_sudo:
            command = ['sudo'] + command
        result = self.shell.run(command, allow_error=True, *args, **kwargs)
        self.logger.debug('Executed command: %s, '
                          'result code %d, output:\n%s' % (' '.join(command),
                                                           result.return_code,
                                                           result.output))
        return result

    def open(self, path, mode='r'):
        self.logger.debug('Opening file %s mode %s' % (path, mode))
        return self.shell.open(path, mode)


ProcessInfo = recordtype('ProcessInfo', ['pid', 'command'])


class ExtendedNodeClient(object):

    def __init__(self, client):
        super(ExtendedNodeClient, self).__init__()
        self._client = client

    def run(self, command, *args, **kwargs):
        return self._client.run(command, *args, **kwargs)

    def open(self, path, mode='r'):
        return self._client.open(path, mode)

    def get_processes(self, reload=False):
        if not hasattr(self, '_processes') or reload:
            self._processes = get_processes(self._client)

        return self._processes

    def get_listen_sockets(self, reload=False):
        if not hasattr(self, '_listen_sockets') or reload:
            self._listen_sockets = get_listen_sockets(self._client)

        return self._listen_sockets

    def get_host_id(self, reload=False):
        if not hasattr(self, '_host_id') or reload:
            self._host_id = get_host_id(self._client)

        return self._host_id


def get_processes(client):
    if hasattr(client, 'get_processes'):
        return client.get_processes()

    lines = client.run(['ps', '-Ao', 'pid,cmd',
                        '--no-headers']).output.split("\n")
    results = []
    for line in lines:
        line = line.strip()
        if line == '':
            continue

        parts = line.split()

        pid = int(parts.pop(0))
        command = ' '.join(parts)
        results.append(ProcessInfo(pid=pid, command=command))

    return results


def get_process_by_pid(client, pid):
    return find(get_processes(client), lambda p: p.pid == pid)


def get_listen_sockets(client):
    if hasattr(client, 'get_listen_sockets'):
        return client.get_listen_sockets()

    result = client.run(['lsof', '-i', '-s', 'TCP:LISTEN', '-nP', '-Fn'])
    if result.return_code != 0:
        return {}

    host_addresses = get_host_network_addresses(client)
    sockets = {}

    current_pid = 0
    for line in result.output.split("\n"):
        if line.startswith('p'):
            current_pid = int(line[1:])
            sockets.setdefault(current_pid, [])
        elif line.startswith('n'):
            host, port = line[1:].split(':', 1)
            if host == '*':
                for address in host_addresses:
                    sockets[current_pid].append((address, port))
            else:
                sockets[current_pid].append((host, port))

    return sockets


def get_process_listen_sockets(client, pid):
    sockets_per_process = get_listen_sockets(client)
    if pid not in sockets_per_process:
        return []

    return sockets_per_process[pid]


def find_process_by_name(client, name):
    processes = get_processes(client)
    for process in processes:
        args = shlex.split(process.command)
        if os.path.basename(args[0]) == name:
            return process

    return None


def find_process(client, pid=None, name=None, sockets=None):
    if pid:
        return find(get_processes(client), lambda p: p.pid == pid)
    elif sockets:
        current_sockets = get_listen_sockets(client)
        x = find(current_sockets.items(), lambda x: sockets[0] in x[1])
        if not x:
            return None

        return get_process_by_pid(x[0])
    elif name:
        processes = get_processes(client)
        for process in processes:
            args = shlex.split(process.command)
            if os.path.basename(args[0]) == name:
                return process

    return None


def find_python_process(client, name):
    processes = get_processes(client)
    for process in processes:
        args = shlex.split(process.command)
        if len(args) > 0 and (args[0] == name or args[0].endswith('/' + name)):
            return process
        if len(args) > 1 and find_python_process.python_re.match(args[0]) \
                and (args[1] == name or args[1].endswith('/' + name)):
            return process

    return None

find_python_process.python_re = re.compile('(/?([^/]*/)*)python[0-9.]*')


def find_python_package_version(client, package):
    result = client.run(
        ['python', '-c',
            'import pkg_resources; version = pkg_resources'
            '.get_provider(pkg_resources.Requirement.parse("%s"))'
            '.version; print(version)' %
            package])

    s = result.output.strip()
    parts = []
    for p in s.split('.'):
        if not p[0].isdigit():
            break

        parts.append(p)

    version = '.'.join(parts)

    return version


def get_host_id(client):
    if hasattr(client, 'get_host_id'):
        return client.get_host_id()

    ether_re = re.compile('link/ether (([0-9a-f]{2}:){5}([0-9a-f]{2})) ')
    result = client.run(['bash', '-c', 'ip link | grep "link/ether "'])
    macs = []
    for match in ether_re.finditer(result.output):
        macs.append(match.group(1).replace(':', ''))
    return ''.join(macs)


def get_host_network_addresses(client):
    ipaddr_re = re.compile('inet (\d+\.\d+\.\d+\.\d+)/\d+')
    addresses = []
    result = client.run(['bash', '-c', 'ip address list | grep "inet "'])
    for match in ipaddr_re.finditer(result.output):
        addresses.append(match.group(1))
    return addresses


def permissions_string_to_number(s):
    # TODO(someone): implement it
    return 0


def collect_file(client, path):
    ls = client.run(['ls', '-l', '--time-style=full-iso', path])
    if ls.return_code != 0:
        return None

    line = ls.output.split("\n")[0]
    perm, links, owner, group, size, date, time, timezone, name = \
        line.split()
    permissions = permissions_string_to_number(perm)

    with client.open(path) as f:
        contents = f.read()

    return FileResource(path, contents, owner, group, permissions)


def collect_component_configs(client, component,
                              command, default_config=None):
    config_files = []

    args = shlex.split(command)[1:]

    p = index(args, lambda s: s == '--config-file')
    if p != -1 and p + 1 < len(args):
        config_path = args[p + 1]
    else:
        config_path = default_config

    if config_path:
        r = collect_file(client, config_path)
        if r:
            config_files.append(r)

    p = index(args, lambda s: s == '--config-dir')
    if p != -1 and p + 1 < len(args):
        result = client.run(['ls', '%s/*.conf' % args[p + 1]])
        if result.return_code == 0:
            for config_path in result.output.split("\n"):
                config_files.extend(
                    collect_file(client, config_path))

    component.config_files = config_files

    for i, arg in enumerate(args):
        if arg.startswith('--'):
            name = arg[2:]
            if '=' in name:
                name, value = name.split('=', 1)
            elif i + 1 < len(args):
                value = args[i + 1]
                i += 1
            else:
                continue

            component.config.set_cli(name, value)


# Marker class
class BaseDiscovery(object):

    def __init__(self):
        self._seen_items = []

    def seen(self, driver, host, **data):
        return False


class HostDiscovery(BaseDiscovery):
    item_type = 'host'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        hostname = client.run(['hostname']).output.strip()

        item = Host(name=hostname)
        item.id = get_host_id(client)
        item.network_addresses = get_host_network_addresses(client)

        process_sockets = get_listen_sockets(client)

        # Service detection part
        process = find_python_process(client, 'keystone-all')
        if process:
            driver.enqueue(
                'keystone', host=host, pid=process.pid,
                sockets=process_sockets.get(process.pid, []))

        for service in [
            'nova-api', 'nova-volume', 'nova-scheduler',
            'glance-api', 'glance-registry',
            'cinder-api', 'cinder-volume', 'cinder-scheduler',
            'neutron-server', 'neutron-dhcp-agent', 'neutron-l3-agent',
            'neutron-metadata-agent', 'neutron-openvswitch-agent',
            'swift-proxy-server', 'swift-container-server',
            'swift-account-server', 'swift-object-server'
        ]:
            process = find_python_process(client, service)
            if not process:
                continue

            driver.enqueue(
                service, host=host, pid=process.pid,
                sockets=process_sockets.get(process.pid, []))

        for service in ['mysql', 'rabbitmq']:
            process = find_process(client, name=service)
            if not process:
                continue

            driver.enqueue(
                service, host=host, pid=process.pid,
                sockets=process_sockets.get(process.pid, []))

        self._seen_items.append(item)

        return item

    def seen(self, driver, host, **data):
        item = find(self._seen_items, lambda h: host in h.network_addresses)
        return item is not None


class ServiceDiscovery(BaseDiscovery):

    def seen(self, driver, host, **data):
        if 'sockets' in data:
            item = find(self._seen_items,
                        lambda s: data['sockets'] == s.listen_sockets)
        elif 'port' in data:
            item = find(self._seen_items,
                        lambda s: (host, data['port']) in s.listen_sockets)
        else:
            client = driver.client(host)
            host_id = client.get_host_id()
            item = find(self._seen_items, lambda s: host_id == s.host_id)

        return item is not None


class KeystoneDiscovery(ServiceDiscovery):
    item_type = 'keystone'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'keystone-all')
        if not process:
            return None

        keystone = KeystoneComponent()
        keystone.host_id = get_host_id(client)
        keystone.listen_sockets = get_process_listen_sockets(client,
                                                             process.pid)
        keystone.version = find_python_package_version(client, 'keystone')
        keystone.config_files = []

        collect_component_configs(
            client, keystone, process.command,
            default_config='/etc/keystone/keystone.conf')

        token = keystone.config['admin_token']
        host = keystone.config['bind_host']
        if host == '0.0.0.0':
            host = '127.0.0.1'
        port = int(keystone.config['admin_port'])

        keystone_env = {
            'OS_SERVICE_TOKEN': token,
            'OS_SERVICE_ENDPOINT': 'http://%s:%d/v2.0' % (host, port)
        }

        def db(command):
            return self._get_keystone_db_data(client, command,
                                              env=keystone_env)

        keystone.db = dict()
        keystone.db['tenants'] = db('tenant-list')
        keystone.db['users'] = db('user-list')
        keystone.db['services'] = db('service-list')
        keystone.db['endpoints'] = db('endpoint-list')

        self._seen_items.append(keystone)

        return keystone

    def _get_keystone_db_data(self, client, command, env={}):
        result = client.run(['keystone', command], update_env=env)
        if result.return_code != 0:
            return []

        lines = result.output.strip().split("\n")

        columns = []
        last_pos = 0
        l = lines[0]
        while True:
            pos = l.find('+', last_pos + 1)
            if pos == -1:
                break

            columns.append({'start': last_pos + 1, 'end': pos - 1})

            last_pos = pos

        l = lines[1]
        for c in columns:
            c['name'] = l[c['start']:c['end']].strip()

        data = []
        for l in lines[3:-1]:
            d = dict()
            for c in columns:
                d[c['name']] = l[c['start']:c['end']].strip()

            data.append(d)

        return data


class NovaApiDiscovery(ServiceDiscovery):
    item_type = 'nova-api'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'nova-api')
        if not process:
            return None

        nova_api = NovaApiComponent()
        nova_api.host_id = get_host_id(client)
        nova_api.listen_sockets = get_process_listen_sockets(client,
                                                             process.pid)
        nova_api.version = find_python_package_version(client, 'nova')

        collect_component_configs(
            client, nova_api, process.command,
            default_config='/etc/nova/nova.conf')

        config_dir = '/etc/nova'
        if len(nova_api.config_files) > 0:
            config_dir = os.path.dirname(nova_api.config_files[0].path)

        paste_config_path = path_relative_to(
            nova_api.config['api_paste_config'], config_dir)
        nova_api.paste_config_file = collect_file(
            client, paste_config_path)

        self._seen_items.append(nova_api)

        return nova_api


class NovaComputeDiscovery(ServiceDiscovery):
    item_type = 'nova-compute'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'nova-compute')
        if not process:
            return None

        nova_compute = NovaComputeComponent()
        nova_compute.host_id = get_host_id(client)
        nova_compute.listen_sockets = get_process_listen_sockets(client,
                                                                 process.pid)
        nova_compute.version = find_python_package_version(client, 'nova')

        collect_component_configs(
            client, nova_compute, process.command,
            default_config='/etc/nova/nova.conf')

        self._seen_items.append(nova_compute)

        return nova_compute


class NovaSchedulerDiscovery(ServiceDiscovery):
    item_type = 'nova-scheduler'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'nova-scheduler')
        if not process:
            return None

        nova_scheduler = NovaSchedulerComponent()
        nova_scheduler.host_id = get_host_id(client)
        nova_scheduler.listen_sockets = get_process_listen_sockets(client,
                                                                   process.pid)
        nova_scheduler.version = find_python_package_version(client, 'nova')

        collect_component_configs(
            client, nova_scheduler, process.command,
            default_config='/etc/nova/nova.conf')

        self._seen_items.append(nova_scheduler)

        return nova_scheduler


class GlanceApiDiscovery(ServiceDiscovery):
    item_type = 'glance-api'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'glance-api')
        if not process:
            return None

        glance_api = GlanceApiComponent()
        glance_api.host_id = get_host_id(client)
        glance_api.listen_sockets = get_process_listen_sockets(client,
                                                               process.pid)
        glance_api.version = find_python_package_version(client, 'glance')

        collect_component_configs(
            client, glance_api, process.command,
            default_config='/etc/glance/glance.conf')

        self._seen_items.append(glance_api)

        return glance_api


class GlanceRegistryDiscovery(ServiceDiscovery):
    item_type = 'glance-registry'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'glance-registry')
        if not process:
            return None

        glance_registry = GlanceRegistryComponent()
        glance_registry.host_id = get_host_id(client)
        glance_registry.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        glance_registry.version = find_python_package_version(client, 'glance')

        collect_component_configs(
            client, glance_registry, process.command,
            default_config='/etc/glance/glance.conf')

        self._seen_items.append(glance_registry)

        return glance_registry


class CinderApiDiscovery(ServiceDiscovery):
    item_type = 'cinder-api'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'cinder-api')
        if not process:
            return None

        cinder_api = CinderApiComponent()
        cinder_api.host_id = get_host_id(client)
        cinder_api.listen_sockets = get_process_listen_sockets(client,
                                                               process.pid)
        cinder_api.version = find_python_package_version(client, 'cinder')

        collect_component_configs(
            client, cinder_api, process.command,
            default_config='/etc/cinder/cinder.conf')

        config_dir = '/etc/cinder'
        if len(cinder_api.config_files) > 0:
            config_dir = os.path.dirname(cinder_api.config_files[0].path)

        paste_config_path = path_relative_to(
            cinder_api.config['api_paste_config'], config_dir)
        cinder_api.paste_config_file = collect_file(
            client, paste_config_path)

        self._seen_items.append(cinder_api)

        return cinder_api


class CinderVolumeDiscovery(ServiceDiscovery):
    item_type = 'cinder-volume'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'cinder-volume')
        if not process:
            return None

        cinder_volume = CinderVolumeComponent()
        cinder_volume.host_id = get_host_id(client)
        cinder_volume.listen_sockets = get_process_listen_sockets(client,
                                                                  process.pid)
        cinder_volume.version = find_python_package_version(client, 'cinder')

        collect_component_configs(
            client, cinder_volume, process.command,
            default_config='/etc/cinder/cinder.conf')

        config_dir = '/etc/cinder'
        if len(cinder_volume.config_files) > 0:
            config_dir = os.path.dirname(cinder_volume.config_files[0].path)

        rootwrap_config_path = path_relative_to(
            cinder_volume.config['rootwrap_config'], config_dir)
        cinder_volume.rootwrap_config = collect_file(
            client, rootwrap_config_path)

        self._seen_items.append(cinder_volume)

        return cinder_volume


class CinderSchedulerDiscovery(ServiceDiscovery):
    item_type = 'cinder-scheduler'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'cinder-scheduler')
        if not process:
            return None

        cinder_scheduler = CinderSchedulerComponent()
        cinder_scheduler.host_id = get_host_id(client)
        cinder_scheduler.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        cinder_scheduler.version = find_python_package_version(client,
                                                               'cinder')

        collect_component_configs(
            client, cinder_scheduler, process.command,
            default_config='/etc/cinder/cinder.conf')

        self._seen_items.append(cinder_scheduler)

        return cinder_scheduler


class MysqlDiscovery(ServiceDiscovery):
    item_type = 'mysql'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_process(client, name='mysqld')
        if not process:
            return None

        mysqld_version_re = re.compile('mysqld\s+Ver\s(\S+)\s')

        mysql = MysqlComponent()
        mysql.host_id = get_host_id(client)
        mysql.listen_sockets = get_process_listen_sockets(client, process.pid)

        version_result = client.run(['mysqld', '--version'])
        m = mysqld_version_re.match(version_result.output)
        mysql.version = m.group(1) if m else 'unknown'

        mysql.config_files = []
        config_locations_result = client.run(
            ['bash', '-c',
             'mysqld --help --verbose '
             '| grep "Default options are read from" -A 1'])
        config_locations = config_locations_result.output.strip().split(
            "\n")[-1].split()
        for path in config_locations:
            f = collect_file(client, path)
            if f:
                mysql.config_files.append(f)

        self._seen_items.append(mysql)

        return mysql


class RabbitmqDiscovery(ServiceDiscovery):
    item_type = 'rabbitmq'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_process(client, name='beam.smp')
        if not process:
            process = find_process(client, name='beam')
            if not process:
                return None

        if process.command.find('rabbit') == -1:
            return None

        rabbitmq = RabbitMqComponent()
        rabbitmq.host_id = get_host_id(client)
        rabbitmq.listen_sockets = get_process_listen_sockets(client,
                                                             process.pid)
        rabbitmq.version = 'unknown'

        env_file = '/etc/rabbitmq/rabbitmq-env.conf'
        env_vars = {}
        result = client.run(['bash', '-c', 'source %s && set' % env_file])
        if result.return_code == 0:
            lines = result.output.split("\n")
            env_vars = dict((k, v) for k, v in lines.split('=', 1))

        rabbitmq_env_vars = \
            dict((key.replace('RABBITMQ_', ''), value)
                 for key, value in env_vars if key.startswith('RABBITMQ_'))

        for key, value in rabbitmq_env_vars:
            rabbitmq.config.set_env(key, value)

        args = shlex.split(process.command)
        for i, s in enumerate(args):
            if s == '-rabbit' and i + 2 <= len(args):
                rabbitmq.config.set_cli(args[i + 1], args[i + 2])

        self._seen_items.append(rabbitmq)

        return rabbitmq


class SwiftProxyServerDiscovery(ServiceDiscovery):
    item_type = 'swift-proxy-server'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'swift-proxy-server')
        if not process:
            return None

        swift_proxy_server = SwiftProxyServerComponent()
        swift_proxy_server.host_id = get_host_id(client)
        swift_proxy_server.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        swift_proxy_server.version = find_python_package_version(client,
                                                                 'swift')

        collect_component_configs(
            client, swift_proxy_server, process.command,
            default_config='/etc/swift/proxy-server.conf')

        self._seen_items.append(swift_proxy_server)

        return swift_proxy_server


class SwiftContainerServerDiscovery(ServiceDiscovery):
    item_type = 'swift-container-server'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'swift-container-server')
        if not process:
            return None

        swift_container_server = SwiftContainerServerComponent()
        swift_container_server.host_id = get_host_id(client)
        swift_container_server.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        swift_container_server.version = find_python_package_version(client,
                                                                     'swift')

        collect_component_configs(
            client, swift_container_server, process.command,
            default_config='/etc/swift/container-server/1.conf')

        self._seen_items.append(swift_container_server)

        return swift_container_server


class SwiftAccountServerDiscovery(ServiceDiscovery):
    item_type = 'swift-account-server'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'swift-account-server')
        if not process:
            return None

        swift_account_server = SwiftAccountServerComponent()
        swift_account_server.host_id = get_host_id(client)
        swift_account_server.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        swift_account_server.version = find_python_package_version(client,
                                                                   'swift')

        collect_component_configs(
            client, swift_account_server, process.command,
            default_config='/etc/swift/account-server/1.conf')

        self._seen_items.append(swift_account_server)

        return swift_account_server


class SwiftObjectServerDiscovery(ServiceDiscovery):
    item_type = 'swift-object-server'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'swift-object-server')
        if not process:
            return None

        swift_object_server = SwiftObjectServerComponent()
        swift_object_server.host_id = get_host_id(client)
        swift_object_server.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        swift_object_server.version = find_python_package_version(client,
                                                                  'swift')

        collect_component_configs(
            client, swift_object_server, process.command,
            default_config='/etc/swift/object-server/1.conf')

        self._seen_items.append(swift_object_server)

        return swift_object_server


class NeutronServerDiscovery(ServiceDiscovery):
    item_type = 'neutron-server'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'neutron-server')
        if not process:
            return None

        neutron_server = NeutronServerComponent()
        neutron_server.host_id = get_host_id(client)
        neutron_server.listen_sockets = get_process_listen_sockets(client,
                                                                   process.pid)
        neutron_server.version = find_python_package_version(client, 'neutron')

        collect_component_configs(
            client, neutron_server, process.command,
            default_config='/etc/neutron/neutron.conf')

        self._seen_items.append(neutron_server)

        return neutron_server


class NeutronDhcpAgentDiscovery(ServiceDiscovery):
    item_type = 'neutron-dhcp-agent'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'neutron-dhcp-agent')
        if not process:
            return None

        neutron_dhcp_agent = NeutronDhcpAgentComponent()
        neutron_dhcp_agent.host_id = get_host_id(client)
        neutron_dhcp_agent.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        neutron_dhcp_agent.version = find_python_package_version(client,
                                                                 'neutron')

        collect_component_configs(
            client, neutron_dhcp_agent, process.command,
            default_config='/etc/neutron/dhcp_agent.ini')

        self._seen_items.append(neutron_dhcp_agent)

        return neutron_dhcp_agent


class NeutronL3AgentDiscovery(ServiceDiscovery):
    item_type = 'neutron-l3-agent'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'neutron-l3-agent')
        if not process:
            return None

        neutron_l3_agent = NeutronL3AgentComponent()
        neutron_l3_agent.host_id = get_host_id(client)
        neutron_l3_agent.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        neutron_l3_agent.version = find_python_package_version(client,
                                                               'neutron')

        collect_component_configs(
            client, neutron_l3_agent, process.command,
            default_config='/etc/neutron/l3_agent.ini')

        self._seen_items.append(neutron_l3_agent)

        return neutron_l3_agent


class NeutronMetadataAgentDiscovery(ServiceDiscovery):
    item_type = 'neutron-metadata-agent'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'neutron-metadata-agent')
        if not process:
            return None

        neutron_metadata_agent = NeutronMetadataAgentComponent()
        neutron_metadata_agent.host_id = get_host_id(client)
        neutron_metadata_agent.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        neutron_metadata_agent.version = find_python_package_version(client,
                                                                     'neutron')

        collect_component_configs(
            client, neutron_metadata_agent, process.command,
            default_config='/etc/neutron/metadata_agent.ini')

        self._seen_items.append(neutron_metadata_agent)

        return neutron_metadata_agent


class NeutronOpenvswitchAgentDiscovery(ServiceDiscovery):
    item_type = 'neutron-openvswitch-agent'

    def discover(self, driver, host, **data):
        client = driver.client(host)

        process = find_python_process(client, 'neutron-openvswitch-agent')
        if not process:
            return None

        neutron_openvswitch_agent = NeutronOpenvswitchAgentComponent()
        neutron_openvswitch_agent.host_id = get_host_id(client)
        neutron_openvswitch_agent.listen_sockets = get_process_listen_sockets(
            client, process.pid)
        neutron_openvswitch_agent.version = find_python_package_version(
            client, 'neutron')

        collect_component_configs(
            client, neutron_openvswitch_agent, process.command,
            default_config='/etc/neutron/plugins/ml2/ml2_conf.ini')

        self._seen_items.append(neutron_openvswitch_agent)

        return neutron_openvswitch_agent


DiscoveryTask = recordtype('DiscoveryTask', ['type', 'host', 'data'])


class DiscoveryDriver(object):

    def __init__(self, defaultPrivateKey):
        self.queue = deque()
        self.defaultPrivateKey = defaultPrivateKey
        self._hosts = {}
        self._clients = {}

    def setHostConnectionInfo(self, host, port=22,
                              username='root', password=None, privateKey=None):
        self._hosts[host] = dict(
            host=host,
            port=port,
            username=username,
            password=password,
            private_key=privateKey or self.defaultPrivateKey)

    def client(self, host):
        if host not in self._clients:
            host_info = self._hosts[host] if host in self._hosts else dict(
                host=host, port=22,
                username='root', private_key=self.defaultPrivateKey)

            self._clients[host] = ExtendedNodeClient(NodeClient(**host_info))

        return self._clients[host]

    def enqueue(self, type, host, **data):
        self.queue.append(DiscoveryTask(type, host, data))


class OpenstackDiscovery(object):
    logger = logging.getLogger('rubick.discovery')

    def discover(self, initial_nodes, private_key):
        "Takes a list of node addresses "
        "and returns discovered openstack installation info"
        agents = dict([(c.item_type, c())
                       for c in all_subclasses(BaseDiscovery)
                       if hasattr(c, 'item_type')])

        driver = DiscoveryDriver(private_key)

        # Set connection info and queue initial nodes
        for info in parse_nodes_info(initial_nodes, private_key):
            driver.setHostConnectionInfo(
                host=info['host'], port=info['port'],
                username=info['username'], password=info['password'],
                privateKey=info['private_key'])

            driver.enqueue('host', info['host'])

        items = []
        while len(driver.queue) > 0:
            task = driver.queue.popleft()

            self.logger.info('Processing item of type %s, host = %s' %
                             (task.type, task.host))
            if task.type in agents.keys():
                agent = agents[task.type]

                if agent.seen(driver, task.host, **task.data):
                    continue

                item = agent.discover(driver, task.host, **task.data)

                if item:
                    items.append(item)
            else:
                self.logger.error('Unknown item type: %s' % task.type)

        # Rebuild model tree
        openstack = Openstack()

        for host in filter(lambda i: isinstance(i, Host), items):
            openstack.add_host(host)

        for service in filter(lambda i: isinstance(i, Service), items):
            host = find(openstack.hosts, lambda h: h.id == service.host_id)
            if not host:
                continue

            host.add_component(service)

        return openstack
