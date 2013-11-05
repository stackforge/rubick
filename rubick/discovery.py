import logging
from StringIO import StringIO
import tempfile
import traceback

import joker
import os.path
import paramiko
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException
import re
from rubick.common import Issue, index, path_relative_to
from rubick.exceptions import ValidatorException
from rubick.model import *
import spur


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
    logger = logging.getLogger('rubick.discovery.joker')

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
    logger = logging.getLogger('rubick.discovery.joker')

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
            self.logger.debug("Adding node to joker: %s" % node)
            j.addNode('node%d' % count,
                      host=node['host'],
                      port=node['port'],
                      user=node['username'])

        nodes = []
        for j_node_info in j.discover():
            node = dict(
                name=j_node_info['name'],
                host=j_node_info['ip'],
                port=j_node_info['port'],
                username=j_node_info['user'],
                private_key=j_node_info['key'],)
                # proxy_command=j_node_info['proxy_command'])
            node = dict((k, v) for k, v in node.iteritems() if v)
            nodes.append(node)

        return nodes


python_re = re.compile('(/?([^/]*/)*)python[0-9.]*')


class OpenstackDiscovery(object):
    logger = logging.getLogger('rubick.discovery')

    node_discovery_klass = JokerNodeDiscovery

    def test_connection(self, initial_nodes, private_key):
        d = self.node_discovery_klass()
        return d.test_connection(initial_nodes, private_key)

    def discover(self, initial_nodes, private_key):
        "Takes a list of node addresses "
        "and returns discovered openstack installation info"
        openstack = Openstack()

        node_discovery = self.node_discovery_klass()

        for node_info in node_discovery.discover(initial_nodes, private_key):
            self.logger.debug('Connecting to node %(host)s'
                              '(port %(port)d, username %(username)s' %
                              node_info)
            try:
                client = NodeClient(
                    host=node_info['host'],
                    port=node_info['port'],
                    username=node_info['username'],
                    password=node_info.get('password'),
                    private_key=node_info['private_key'])

                client.run(['echo', 'test'])
            except:
                self.logger.exception("Can't connect to host %s" %
                                      node_info['host'])
                openstack.report_issue(
                    Issue(Issue.WARNING, "Can't connect to node %s" %
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

        for component in ['keystone', 'nova_api', 'nova_compute',
                          'nova_scheduler', 'glance_api', 'glance_registry',
                          'cinder_api', 'cinder_volume', 'cinder_scheduler',
                          'mysql', 'rabbitmq', 'neutron_server',
                          'swift_proxy_server']:
            method = '_collect_%s_data' % component
            if hasattr(self, method):
                try:
                    host.add_component(getattr(self, method)(client))
                except:
                    traceback.print_exc()

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

    def _get_processes(self, client):
        return (
            [line.split()
             for line in client.run(['ps', '-Ao', 'cmd',
                                     '--no-headers']).output.split("\n")]
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

    def _collect_component_configs(self, client, component,
                                   args, default_config=None):
        config_files = []

        p = index(args, lambda s: s == '--config-file')
        if p != -1 and p + 1 < len(args):
            config_path = args[p + 1]
        else:
            config_path = '/etc/keystone/keystone.conf'

        if config_path:
            config_files.append(self._collect_file(client, config_path))

        p = index(args, lambda s: s == '--config-dir')
        if p != -1 and p + 1 < len(args):
            result = client.run(['ls', '%s/*.conf' % args[p + 1]])
            if result.return_code == 0:
                for config_path in result.output.split("\n"):
                    config_files.extend(
                        self._collect_file(client, config_path))

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
        process = self._find_python_process(client, 'keystone-all')
        if not process:
            return None

        keystone = KeystoneComponent()
        keystone.version = self._find_python_package_version(
            client, 'keystone')
        keystone.config_files = []

        self._collect_component_configs(
            client, keystone, process[1:],
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

        nova_api = NovaApiComponent()
        nova_api.version = self._find_python_package_version(client, 'nova')

        self._collect_component_configs(
            client, nova_api, process[1:],
            default_config='/etc/nova/nova.conf')

        config_dir = '/etc/nova'
        if len(nova_api.config_files) > 0:
            config_dir = os.path.dirname(nova_api.config_files[0].path)

        paste_config_path = path_relative_to(
            nova_api.config['api_paste_config'], config_dir)
        nova_api.paste_config_file = self._collect_file(
            client, paste_config_path)

        return nova_api

    def _collect_nova_compute_data(self, client):
        process = self._find_python_process(client, 'nova-compute')
        if not process:
            return None

        nova_compute = NovaComputeComponent()
        nova_compute.version = self._find_python_package_version(client,
                                                                 'nova')

        self._collect_component_configs(
            client, nova_compute, process[1:],
            default_config='/etc/nova/nova.conf')

        return nova_compute

    def _collect_nova_scheduler_data(self, client):
        process = self._find_python_process(client, 'nova-scheduler')
        if not process:
            return None

        nova_scheduler = NovaSchedulerComponent()
        nova_scheduler.version = self._find_python_package_version(client,
                                                                   'nova')

        self._collect_component_configs(
            client, nova_scheduler, process[1:],
            default_config='/etc/nova/nova.conf')

        return nova_scheduler

    def _collect_glance_api_data(self, client):
        process = self._find_python_process(client, 'glance-api')
        if not process:
            return None

        glance_api = GlanceApiComponent()
        glance_api.version = self._find_python_package_version(client,
                                                               'glance')

        self._collect_component_configs(
            client, glance_api, process[1:],
            default_config='/etc/glance/glance.conf')

        return glance_api

    def _collect_glance_registry_data(self, client):
        process = self._find_python_process(client, 'glance-registry')
        if not process:
            return None

        glance_registry = GlanceRegistryComponent()
        glance_registry.version = self._find_python_package_version(client,
                                                                    'glance')

        self._collect_component_configs(
            client, glance_registry, process[1:],
            default_config='/etc/glance/glance.conf')

        return glance_registry

    def _collect_cinder_api_data(self, client):
        process = self._find_python_process(client, 'cinder-api')
        if not process:
            return None

        cinder_api = CinderApiComponent()
        cinder_api.version = self._find_python_package_version(client,
                                                               'cinder')

        self._collect_component_configs(
            client, cinder_api, process[1:],
            default_config='/etc/cinder/cinder.conf')

        config_dir = '/etc/cinder'
        if len(cinder_api.config_files) > 0:
            config_dir = os.path.dirname(cinder_api.config_files[0].path)

        paste_config_path = path_relative_to(
            cinder_api.config['api_paste_config'], config_dir)
        cinder_api.paste_config_file = self._collect_file(
            client, paste_config_path)

        return cinder_api

    def _collect_cinder_volume_data(self, client):
        process = self._find_python_process(client, 'cinder-volume')
        if not process:
            return None

        cinder_volume = CinderVolumeComponent()
        cinder_volume.version = self._find_python_package_version(client,
                                                                  'cinder')

        self._collect_component_configs(
            client, cinder_volume, process[1:],
            default_config='/etc/cinder/cinder.conf')

        config_dir = '/etc/cinder'
        if len(cinder_volume.config_files) > 0:
            config_dir = os.path.dirname(cinder_volume.config_files[0].path)

        rootwrap_config_path = path_relative_to(
            cinder_volume.config['rootwrap_config'], config_dir)
        cinder_volume.rootwrap_config = self._collect_file(
            client, rootwrap_config_path)

        return cinder_volume

    def _collect_cinder_scheduler_data(self, client):
        process = self._find_python_process(client, 'cinder-scheduler')
        if not process:
            return None

        cinder_scheduler = CinderSchedulerComponent()
        cinder_scheduler.version = self._find_python_package_version(client,
                                                                     'cinder')

        self._collect_component_configs(
            client, cinder_scheduler, process[1:],
            default_config='/etc/cinder/cinder.conf')

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
             'mysqld --help --verbose '
             '| grep "Default options are read from" -A 1'])
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
            process = self._find_process(client, 'beam')
            if not process:
                return None

        if ' '.join(process).find('rabbit') == -1:
            return None

        rabbitmq = RabbitMqComponent()
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

        for i, s in enumerate(process):
            if s == '-rabbit' and i + 2 <= len(process):
                rabbitmq.config.set_cli(process[i + 1], process[i + 2])

        return rabbitmq

    def _collect_neutron_server_data(self, client):
        process = self._find_python_process(client, 'neutron-server')
        if not process:
            return None

        neutron_server = NeutronServerComponent()
        neutron_server.version = self._find_python_package_version(client,
                                                                   'neutron')

        self._collect_component_configs(
            client, neutron_server, process[1:],
            default_config='/etc/neutron/neutron.conf')

        return neutron_server

    def _collect_swift_proxy_server_data(self, client):
        process = self._find_python_process(client, 'swift-proxy-server')
        if not process:
            return None

        swift_proxy_server = SwiftProxyServerComponent()
        swift_proxy_server.version = self._find_python_package_version(client,
                                                                       'swift')

        self._collect_component_configs(
            client, swift_proxy_server, process[1:],
            default_config='/etc/swift/proxy-server.conf')

        return swift_proxy_server
