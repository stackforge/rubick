import os.path
import re
import traceback
from StringIO import StringIO
import logging

import spur
import paramiko
from paramiko.rsakey import RSAKey
from paramiko.dsskey import DSSKey
from paramiko.ssh_exception import SSHException
import joker

from ostack_validator.common import Issue, index, path_relative_to
from ostack_validator.model import *
from ostack_validator.exceptions import ValidatorException


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

        try:
            self._pkey = RSAKey.from_private_key(StringIO(private_key))
        except SSHException:
            try:
                self._pkey = DSSKey.from_private_key(StringIO(private_key))
            except SSHException:
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

    def __init__(self, host, port=22, username='root', password=None,
                 private_key=None, proxy_command=None):
        super(NodeClient, self).__init__()
        self.use_sudo = (username != 'root')
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
        return self.shell.run(command, allow_error=True, *args, **kwargs)

    def open(self, path, mode='r'):
        return self.shell.open(path, mode)


connection_re = re.compile('(?:(\w+)@)?([^:]+)(?::(\d+))?')


def parse_nodes_info(nodes, password=None, private_key=None):
    result = []
    for node in nodes:
        m = connection_re.match(node)
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


class SimpleNodeDiscovery(object):
    def test_connection(self, initial_nodes, private_key):
        for node in parse_nodes_info(initial_nodes, private_key=private_key):
            client = NodeClient(**node)

            try:
                client.run(['echo', 'ok'])
            except:
                traceback.print_exc()
                return False

        return True

    def discover(self, initial_nodes, private_key):
        return parse_nodes_info(initial_nodes, private_key=private_key)


class JokerNodeDiscovery(object):
    def test_connection(self, initial_nodes, private_key):
        for node in parse_nodes_info(initial_nodes, private_key=private_key):
            client = NodeClient(**node)

            try:
                client.run(['echo', 'ok'])
            except:
                return False

        return True

    def discover(self, initial_nodes, private_key):
        j = joker.Joker(default_key=private_key)
        count = 0
        for node in parse_nodes_info(initial_nodes):
            j.add_node('node%d' % count,
                       node['host'],
                       node['port'],
                       node['username'])

        nodes = j.discover()

        return nodes


python_re = re.compile('(/?([^/]*/)*)python[0-9.]*')


class OpenstackDiscovery(object):
    logger = logging.getLogger('ostack_validator.discovery')

    node_discovery_klass = SimpleNodeDiscovery

    def test_connection(self, initial_nodes, private_key):
        d = self.node_discovery_klass()
        return d.test_connection(initial_nodes, private_key)

    def discover(self, initial_nodes, username, private_key):
        "Takes a list of node addresses "
        "and returns discovered openstack installation info"
        openstack = Openstack()

        node_discovery = self.node_discovery_klass()

        for node_info in node_discovery.discover(initial_nodes, private_key):
            try:
                client = NodeClient(
                    host=node_info['host'],
                    port=node_info['port'],
                    username=node_info['username'],
                    password=node_info.get('password'),
                    private_key=node_info['private_key'])

                client.run(['echo', 'test'])
            except:
                self.logger.exception("Can't connect to host %s" % node_info['host'])
                openstack.report_issue(
                    Issue(
                        Issue.WARNING,
                        "Can't connect to node %s" %
                        node_info['host']))
                continue

            host = self._discover_node(client)

            if len(host.components) == 0:
                continue

            openstack.add_host(host)

        if len(openstack.hosts) == 0:
            openstack.report_issue(
                Issue(Issue.FATAL, "No OpenStack nodes were discovered"))

        return openstack

    def _discover_node(self, client):
        hostname = client.run(['hostname']).output.strip()

        host = Host(name=hostname)
        host.id = self._collect_host_id(client)
        host.network_addresses = self._collect_host_network_addresses(client)

        host.add_component(self._collect_keystone_data(client))
        host.add_component(self._collect_nova_api_data(client))
        host.add_component(self._collect_nova_compute_data(client))
        host.add_component(self._collect_nova_scheduler_data(client))
        host.add_component(self._collect_glance_api_data(client))
        host.add_component(self._collect_glance_registry_data(client))
        host.add_component(self._collect_cinder_api_data(client))
        host.add_component(self._collect_cinder_volume_data(client))
        host.add_component(self._collect_cinder_scheduler_data(client))
        host.add_component(self._collect_mysql_data(client))
        host.add_component(self._collect_rabbitmq_data(client))

        return host

    def _find_process(self, client, name):
        processes = self._get_processes(client)
        for line in processes:
            if len(line) > 0 and os.path.basename(line[0]) == name:
                return line

        return None

    def _find_python_process(self, client, name):
        processes = self._get_processes(client)
        for line in processes:
            if len(line) > 0 and (line[0] == name
                                  or line[0].endswith('/' + name)):
                return line
            if len(line) > 1 and python_re.match(line[0]) \
                    and (line[1] == name or line[1].endswith('/' + name)):
                return line

        return None

    def _find_python_package_version(self, client, package):
        result = client.run(
            ['python', '-c',
             'import pkg_resources; version = pkg_resources.get_provider(pkg_resources.Requirement.parse("%s")).version; print(version)' %
             package])

        s = result.output.strip()
        parts = []
        for p in s.split('.'):
            if not p[0].isdigit():
                break

            parts.append(p)

        version = '.'.join(parts)

        return version

    def _get_processes(self, client):
        return (
            [line.split()
             for line in client.run(['ps', '-Ao', 'cmd', '--no-headers']).output.split("\n")]
        )

    def _collect_host_id(self, client):
        ether_re = re.compile('link/ether (([0-9a-f]{2}:){5}([0-9a-f]{2})) ')
        result = client.run(['bash', '-c', 'ip link | grep "link/ether "'])
        macs = []
        for match in ether_re.finditer(result.output):
            macs.append(match.group(1).replace(':', ''))
        return ''.join(macs)

    def _collect_host_network_addresses(self, client):
        ipaddr_re = re.compile('inet (\d+\.\d+\.\d+\.\d+)/\d+')
        addresses = []
        result = client.run(['bash', '-c', 'ip address list | grep "inet "'])
        for match in ipaddr_re.finditer(result.output):
            addresses.append(match.group(1))
        return addresses

    def _permissions_string_to_number(self, s):
        return 0

    def _collect_file(self, client, path):
        ls = client.run(['ls', '-l', '--time-style=full-iso', path])
        if ls.return_code != 0:
            return None

        line = ls.output.split("\n")[0]
        perm, links, owner, group, size, date, time, timezone, name = \
            line.split()
        permissions = self._permissions_string_to_number(perm)

        with client.open(path) as f:
            contents = f.read()

        return FileResource(path, contents, owner, group, permissions)

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

    def _collect_keystone_data(self, client):
        keystone_process = self._find_python_process(client, 'keystone-all')
        if not keystone_process:
            return None

        p = index(keystone_process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(keystone_process):
            config_path = keystone_process[p + 1]
        else:
            config_path = '/etc/keystone/keystone.conf'

        keystone = KeystoneComponent()
        keystone.version = self._find_python_package_version(
            client, 'keystone')
        keystone.config_files = []
        keystone.config_files.append(self._collect_file(client, config_path))

        token = keystone.config['admin_token']
        host = keystone.config['bind_host']
        if host == '0.0.0.0':
            host = '127.0.0.1'
        port = int(keystone.config['admin_port'])

        keystone_env = {
            'OS_SERVICE_TOKEN': token,
            'OS_SERVICE_ENDPOINT': 'http://%s:%d/v2.0' % (host, port)
        }

        keystone.db = dict()
        keystone.db['tenants'] = self._get_keystone_db_data(
            client, 'tenant-list', env=keystone_env)
        keystone.db['users'] = self._get_keystone_db_data(
            client, 'user-list', env=keystone_env)
        keystone.db['services'] = self._get_keystone_db_data(
            client, 'service-list', env=keystone_env)
        keystone.db['endpoints'] = self._get_keystone_db_data(
            client, 'endpoint-list', env=keystone_env)

        return keystone

    def _collect_nova_api_data(self, client):
        process = self._find_python_process(client, 'nova-api')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/nova/nova.conf'

        nova_api = NovaApiComponent()
        nova_api.version = self._find_python_package_version(client, 'nova')
        nova_api.config_files = []
        nova_api.config_files.append(self._collect_file(client, config_path))

        paste_config_path = path_relative_to(
            nova_api.config['api_paste_config'],
            os.path.dirname(config_path))
        nova_api.paste_config_file = self._collect_file(
            client, paste_config_path)

        return nova_api

    def _collect_nova_compute_data(self, client):
        process = self._find_python_process(client, 'nova-compute')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/nova/nova.conf'

        nova_compute = NovaComputeComponent()
        nova_compute.version = self._find_python_package_version(
            client, 'nova')
        nova_compute.config_files = []
        nova_compute.config_files.append(
            self._collect_file(client, config_path))

        return nova_compute

    def _collect_nova_scheduler_data(self, client):
        process = self._find_python_process(client, 'nova-scheduler')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/nova/nova.conf'

        nova_scheduler = NovaSchedulerComponent()
        nova_scheduler.version = self._find_python_package_version(
            client, 'nova')
        nova_scheduler.config_files = []
        nova_scheduler.config_files.append(
            self._collect_file(client, config_path))

        return nova_scheduler

    def _collect_glance_api_data(self, client):
        process = self._find_python_process(client, 'glance-api')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/glance/glance-api.conf'

        glance_api = GlanceApiComponent()
        glance_api.version = self._find_python_package_version(
            client, 'glance')
        glance_api.config_files = []
        glance_api.config_files.append(self._collect_file(client, config_path))

        return glance_api

    def _collect_glance_registry_data(self, client):
        process = self._find_python_process(client, 'glance-registry')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/glance/glance-registry.conf'

        glance_registry = GlanceRegistryComponent()
        glance_registry.version = self._find_python_package_version(
            client, 'glance')
        glance_registry.config_files = []
        glance_registry.config_files.append(
            self._collect_file(client, config_path))

        return glance_registry

    def _collect_cinder_api_data(self, client):
        process = self._find_python_process(client, 'cinder-api')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/cinder/cinder.conf'

        cinder_api = CinderApiComponent()
        cinder_api.version = self._find_python_package_version(
            client, 'cinder')
        cinder_api.config_files = []
        cinder_api.config_files.append(self._collect_file(client, config_path))

        paste_config_path = path_relative_to(
            cinder_api.config['api_paste_config'],
            os.path.dirname(config_path))
        cinder_api.paste_config_file = self._collect_file(
            client, paste_config_path)

        return cinder_api

    def _collect_cinder_volume_data(self, client):
        process = self._find_python_process(client, 'cinder-volume')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/cinder/cinder.conf'

        cinder_volume = CinderVolumeComponent()
        cinder_volume.version = self._find_python_package_version(
            client, 'cinder')
        cinder_volume.config_files = []
        cinder_volume.config_files.append(
            self._collect_file(client, config_path))

        rootwrap_config_path = path_relative_to(
            cinder_volume.config['rootwrap_config'],
            os.path.dirname(config_path))
        cinder_volume.rootwrap_config = self._collect_file(
            client, rootwrap_config_path)

        return cinder_volume

    def _collect_cinder_scheduler_data(self, client):
        process = self._find_python_process(client, 'cinder-scheduler')
        if not process:
            return None

        p = index(process, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(process):
            config_path = process[p + 1]
        else:
            config_path = '/etc/cinder/cinder.conf'

        cinder_scheduler = CinderSchedulerComponent()
        cinder_scheduler.version = self._find_python_package_version(
            client, 'cinder')
        cinder_scheduler.config_files = []
        cinder_scheduler.config_files.append(
            self._collect_file(client, config_path))

        return cinder_scheduler

    def _collect_mysql_data(self, client):
        process = self._find_process(client, 'mysqld')
        if not process:
            return None

        mysqld_version_re = re.compile('mysqld\s+Ver\s(\S+)\s')

        mysql = MysqlComponent()

        version_result = client.run(['mysqld', '--version'])
        m = mysqld_version_re.match(version_result.output)
        mysql.version = m.group(1) if m else 'unknown'

        mysql.config_files = []
        config_locations_result = client.run(
            ['bash', '-c',
             'mysqld --help --verbose | grep "Default options are read from the following files in the given order" -A 1'])
        config_locations = config_locations_result.output.strip().split(
            "\n")[-1].split()
        for path in config_locations:
            f = self._collect_file(client, path)
            if f:
                mysql.config_files.append(f)

        return mysql

    def _collect_rabbitmq_data(self, client):
        process = self._find_process(client, 'beam.smp')
        if not process:
            return None

        if ' '.join(process).find('rabbit') == -1:
            return None

        rabbitmq = RabbitMqComponent()
        rabbitmq.version = 'unknown'

        return rabbitmq
