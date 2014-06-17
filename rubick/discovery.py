# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
from collections import deque
import logging
import os.path
import re
from recordtype import recordtype
import shlex
import spur
import stat
import tempfile

import paramiko
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException
from six import StringIO

from rubick.common import index, find, all_subclasses
from rubick.exceptions import ValidatorException
import rubick.model as model


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
        self.host = host
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

    def __getattr__(self, name):
        return getattr(self._client, name)

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


def permissions_string_to_mode(s):
    mode = 0

    if s[0] == 'd':
        mode |= stat.S_IFDIR
    elif s[0] == 's':
        mode |= stat.S_IFSOCK
    elif s[0] == 'l':
        mode |= stat.S_IFLNK
    else:
        mode |= stat.S_IFREG

    if s[1] == 'r':
        mode |= stat.S_IRUSR
    if s[2] == 'w':
        mode |= stat.S_IWUSR
    if s[3] == 'x':
        mode |= stat.S_IXUSR
    if s[4] == 'r':
        mode |= stat.S_IRGRP
    if s[5] == 'w':
        mode |= stat.S_IWGRP
    if s[6] == 'x':
        mode |= stat.S_IXGRP
    if s[7] == 'r':
        mode |= stat.S_IROTH
    if s[8] == 'w':
        mode |= stat.S_IWOTH
    if s[9] == 'x':
        mode |= stat.S_IXOTH

    return mode


def collect_process(client, process_info):
    result = client.run(['readlink', '/proc/%d/cwd' % process_info.pid])
    cwd = result.output.strip()

    process = model.ProcessResource(
        pid=process_info.pid,
        cmdline=process_info.command,
        cwd=cwd)
    process.listen_sockets = get_process_listen_sockets(client, process.pid)

    return process


def collect_file(driver, client, path, searchpath=[]):
    "collect_file(driver, client, path, searchpath=[]) - collect file resource."
    "path can be absolute path, absolute wildcard or relative path + searchpath"
    def _collect_file(path):
        ls = client.run(['ls', '-ld', '--time-style=full-iso', path])
        if ls.return_code != 0:
            return None

        line = ls.output.split("\n")[0]
        perm, links, owner, group, size, date, time, timezone, name = \
            line.split()
        permissions = permissions_string_to_mode(perm)

        with client.open(path) as f:
            contents = f.read()

        r = model.FileResource(path, contents, owner, group, permissions)
        r.host_id = get_host_id(client)
        return r

    if not path:
        return None

    if not os.path.isabs(path):
        for base_path in searchpath:
            f = _collect_file(os.path.join(base_path, path))
            if f:
                return f

        return None
    else:
        ls = client.run(['ls', path])
        if ls.return_code != 0:
            return None

        files = []
        for path in ls.output.split("\n"):
            f = _collect_file(path)
            if f:
                files.append(f)

        if len(files) == 1:
            return files[0]

        return files

    return None


def collect_directory(driver, client, path):
    if not path:
        return None

    if not path.endswith('/'):
        path += '/'

    ls = client.run(['ls', '-ld', '--time-style=full-iso', path])
    if ls.return_code != 0:
        return None

    line = ls.output.split("\n")[0]
    perm, links, owner, group, size, date, time, timezone, name = line.split()
    permissions = permissions_string_to_mode(perm)

    r = model.DirectoryResource(path, owner, group, permissions)
    r.host_id = get_host_id(client)
    return r


def collect_component_configs(driver, client, component,
                              command, default_config=None):
    config_files = []

    args = shlex.split(command)[1:]

    p = index(args, lambda s: s == '--config-file')
    if p != -1 and p + 1 < len(args):
        config_path = args[p + 1]
    else:
        config_path = default_config

    if config_path:
        r = driver.discover('file', client.host, path=config_path)
        if r:
            config_files.append(r)

    p = index(args, lambda s: s == '--config-dir')
    if p != -1 and p + 1 < len(args):
        files = driver.discover('file', client.host, path='%s/*.conf' % args[p + 1])
        if files:
            if not isinstance(files, list):
                files = [files]

            config_files.extend(files)

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
        self.items = []


class HostDiscovery(BaseDiscovery):
    item_type = 'host'

    def discover(self, driver, host, **data):
        item = find(self.items, lambda h: host in h.network_addresses)
        if item:
            return item

        client = driver.client(host)

        hostname = client.run(['hostname']).output.strip()

        item = model.HostResource(name=hostname)
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

        self.items.append(item)

        return item


class FileDiscovery(BaseDiscovery):
    item_type = 'file'

    def discover(self, driver, host, path=None, **data):
        client = driver.client(host)
        host_id = get_host_id(client)

        item = find(self.items,
                    lambda f: f.path == path and f.host_id == host_id)
        if item:
            return item

        item = collect_file(driver, client, path)
        if not item:
            return None

        self.items.append(item)

        driver.discover('directory', host, path=os.path.dirname(item.path))

        return item


class DirectoryDiscovery(BaseDiscovery):
    item_type = 'directory'

    logger = logging.getLogger('rubick.discovery.directory')

    def discover(self, driver, host, path=None, withBaseDirs=True, **data):
        client = driver.client(host)
        host_id = get_host_id(client)

        item = find(self.items,
                    lambda f: f.path == path and f.host_id == host_id)
        if item:
            return item

        self.logger.debug('Discovering directory %s' % path)

        if path == '/':
            return None

        item = collect_directory(driver, client, path)
        if not item:
            return None

        self.items.append(item)

        if withBaseDirs:
            path = os.path.dirname(path)
            while path != '/':
                self.discover(driver, host, path, withBaseDirs=False)
                path = os.path.dirname(path)

        return item


class ServiceDiscovery(BaseDiscovery):

    def find_item(self, driver, host, **data):
        if 'sockets' in data:
            item = find(self.items,
                        lambda s: data['sockets'] == s.process.listen_sockets)
        elif 'port' in data:
            item = find(self.items,
                        lambda s: (host, data['port']) in s.process.listen_sockets)
        else:
            client = driver.client(host)
            host_id = client.get_host_id()
            item = find(self.items, lambda s: host_id == s.host_id)

        return item is not None


class OpenstackComponentDiscovery(ServiceDiscovery):

    def __init__(self):
        super(OpenstackComponentDiscovery, self).__init__()
        assert self.item_type
        if not hasattr(self, 'python_process_name'):
            self.python_process_name = self.item_type
        if not hasattr(self, 'project'):
            self.project = self.item_type.split('-')[0]
        if not hasattr(self, 'model_class'):
            class_name = ''.join([p.capitalize()
                                  for p in self.item_type.split('-')
                                  ]) + 'Component'
            self.model_class = getattr(model, class_name)
        if not hasattr(self, 'default_config_path'):
            self.default_config_path = os.path.join('/etc', self.project,
                                                    self.project + '.conf')

    def discover(self, driver, host, **data):
        item = self.find_item(driver, host, **data)
        if item:
            return item

        client = driver.client(host)

        process = find_python_process(client, self.python_process_name)
        if not process:
            return None

        service = self.model_class()
        service.host_id = get_host_id(client)

        service.process = collect_process(client, process)

        service.version = find_python_package_version(client, self.project)

        collect_component_configs(
            driver, client, service, process.command,
            default_config=self.default_config_path)

        searchpaths = [
            service.process.cwd,
            os.path.join('/etc', self.project)
        ]

        if service.config and service.config.schema:
            for param in service.config.schema:
                if param.type == 'file':
                    path = service.config[param.name]
                    if path and path != '':
                        driver.enqueue('file', host=host, path=path,
                                       searchpath=searchpaths)
                elif param.type == 'directory':
                    path = service.config[param.name]
                    if path and path != '':
                        driver.enqueue('directory', host=host, path=path)

        self.items.append(service)

        return service


class KeystoneDiscovery(OpenstackComponentDiscovery):
    item_type = 'keystone'

    python_process_name = 'keystone-all'

    def discover(self, driver, host, **data):
        item = self.find_item(driver, host, **data)
        if item:
            return item

        keystone = super(KeystoneDiscovery, self).discover(driver, host, **data)
        if not keystone:
            return None

        client = driver.client(host)

        process = find_python_process(client, 'keystone-all')
        if not process:
            return None

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


class NovaApiDiscovery(OpenstackComponentDiscovery):
    item_type = 'nova-api'


class NovaComputeDiscovery(OpenstackComponentDiscovery):
    item_type = 'nova-compute'


class NovaSchedulerDiscovery(OpenstackComponentDiscovery):
    item_type = 'nova-scheduler'


class GlanceApiDiscovery(OpenstackComponentDiscovery):
    item_type = 'glance-api'


class GlanceRegistryDiscovery(OpenstackComponentDiscovery):
    item_type = 'glance-registry'


class CinderApiDiscovery(OpenstackComponentDiscovery):
    item_type = 'cinder-api'


class CinderVolumeDiscovery(OpenstackComponentDiscovery):
    item_type = 'cinder-volume'


class CinderSchedulerDiscovery(OpenstackComponentDiscovery):
    item_type = 'cinder-scheduler'


class MysqlDiscovery(ServiceDiscovery):
    item_type = 'mysql'

    def discover(self, driver, host, **data):
        item = self.find_item(driver, host, **data)
        if item:
            return item

        client = driver.client(host)

        process = find_process(client, name='mysqld')
        if not process:
            return None

        mysqld_version_re = re.compile('mysqld\s+Ver\s(\S+)\s')

        mysql = model.MysqlComponent()
        mysql.host_id = get_host_id(client)

        mysql.process = collect_process(client, process)

        version_result = client.run(['mysqld', '--version'])
        m = mysqld_version_re.match(version_result.output)
        mysql.version = m.group(1) if m else 'unknown'

        mysql.config_files = []
        config_locations_result = client.run(
            ['bash', '-c',
             'mysqld --help --verbose '
             '| grep "Default options are read from" -A 1'])
        config_locations = config_locations_result.output\
            .strip().split("\n")[-1].split()
        for path in config_locations:
            f = driver.discover('file', host, path=path)
            if f:
                mysql.config_files.append(f)

        self.items.append(mysql)

        return mysql


class RabbitmqDiscovery(ServiceDiscovery):
    item_type = 'rabbitmq'

    def discover(self, driver, host, **data):
        item = self.find_item(driver, host, **data)
        if item:
            return item

        client = driver.client(host)

        process = find_process(client, name='beam.smp')
        if not process:
            process = find_process(client, name='beam')
            if not process:
                return None

        if process.command.find('rabbit') == -1:
            return None

        rabbitmq = model.RabbitMqComponent()
        rabbitmq.host_id = get_host_id(client)

        rabbitmq.process = collect_process(client, process)

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

        self.items.append(rabbitmq)

        return rabbitmq


class SwiftProxyServerDiscovery(OpenstackComponentDiscovery):
    item_type = 'swift-proxy-server'


class SwiftContainerServerDiscovery(OpenstackComponentDiscovery):
    item_type = 'swift-container-server'
    default_config_path = '/etc/swift/container-server/1.conf'


class SwiftAccountServerDiscovery(OpenstackComponentDiscovery):
    item_type = 'swift-account-server'
    default_config_path = '/etc/swift/account-server/1.conf'


class SwiftObjectServerDiscovery(OpenstackComponentDiscovery):
    item_type = 'swift-object-server'
    default_config_path = '/etc/swift/object-server/1.conf'


class NeutronServerDiscovery(OpenstackComponentDiscovery):
    item_type = 'neutron-server'


class NeutronDhcpAgentDiscovery(OpenstackComponentDiscovery):
    item_type = 'neutron-dhcp-agent'
    default_config_path = '/etc/neutron/dhcp_agent.ini'


class NeutronL3AgentDiscovery(OpenstackComponentDiscovery):
    item_type = 'neutron-l3-agent'
    default_config_path = '/etc/neutron/l3_agent.ini'


class NeutronMetadataAgentDiscovery(OpenstackComponentDiscovery):
    item_type = 'neutron-metadata-agent'
    default_config_path = '/etc/neutron/metadata_agent.ini'


class NeutronOpenvswitchAgentDiscovery(OpenstackComponentDiscovery):
    item_type = 'neutron-openvswitch-agent'
    default_config_path = '/etc/neutron/plugins/ml2/ml2_conf.ini'


class DiscoveryDriver(object):
    Task = recordtype('Task', ['type', 'host', 'data'])

    logger = logging.getLogger('rubick.discovery')

    def __init__(self, defaultPrivateKey):
        self.queue = deque()
        self.defaultPrivateKey = defaultPrivateKey
        self.agents = dict([(c.item_type, c())
                            for c in all_subclasses(BaseDiscovery)
                            if hasattr(c, 'item_type')])
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

    def discover(self, type, host, **data):
        if type not in self.agents:
            self.logger.error('Request for discovery of unknown type "%s"' % type)
            return None

        self.logger.info('Processing item of type %s, host = %s, %s' %
                         (type, host, ', '.join(['%s=%s' % (k, v) for k, v in data.items()])))

        return self.agents[type].discover(self, host, **data)

    def enqueue(self, type, host, **data):
        self.queue.append(DiscoveryDriver.Task(type, host, data))


class OpenstackDiscovery(object):
    logger = logging.getLogger('rubick.discovery')

    def discover(self, initial_nodes, private_key):
        "Takes a list of node addresses "
        "and returns discovered openstack installation info"
        driver = DiscoveryDriver(private_key)

        # Set connection info and queue initial nodes
        for info in parse_nodes_info(initial_nodes, private_key):
            driver.setHostConnectionInfo(
                host=info['host'], port=info['port'],
                username=info['username'], password=info['password'],
                privateKey=info['private_key'])

            driver.enqueue('host', info['host'])

        while len(driver.queue) > 0:
            task = driver.queue.popleft()

            driver.discover(task.type, task.host, **task.data)

        items = sum([agent.items for agent in driver.agents.values()], [])

        # Rebuild model tree
        openstack = model.Openstack()

        for host in filter(lambda i: isinstance(i, model.HostResource), items):
            openstack.add_host(host)

        for service in filter(lambda i: isinstance(i, model.Service), items):
            host = find(openstack.hosts, lambda h: h.id == service.host_id)
            if not host:
                self.logger.error('Got resource "%s" '
                                  'that belong to non-existing host' % service)
                continue

            host.add_component(service)

        for fs_resource in filter(lambda f: isinstance(f, model.FileSystemResource), items):
            host = find(openstack.hosts, lambda h: h.id == fs_resource.host_id)
            if not host:
                self.logger.error('Got resource "%s" '
                                  'that belong to non-existing host' % fs_resource)
                continue

            host.add_fs_resource(fs_resource)

        return openstack
