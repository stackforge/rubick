import os.path
import re
import sys
import tempfile
import logging

import spur

from ostack_validator.common import Issue, Mark, MarkedIssue, index, path_relative_to
from ostack_validator.model import Openstack, Host, OpenstackComponent, KeystoneComponent, NovaComputeComponent, GlanceApiComponent



class NodeClient(object):
  def __init__(self, node_address, username, private_key_file, ssh_port=22):
    super(NodeClient, self).__init__()
    self.shell = spur.SshShell(hostname=node_address, port=ssh_port, username=username, private_key_file=private_key_file, missing_host_key=spur.ssh.MissingHostKey.accept)

  def run(self, command, *args, **kwargs):
    return self.shell.run(command, *args, **kwargs)

  def open(self, path, mode='r'):
    return self.shell.open(path, mode)

python_re = re.compile('(/?([^/]*/)*)python[0-9.]*')
host_port_re = re.compile('(\d+\.\d+\.\d+\.\d+):(\d+)')

class OpenstackDiscovery(object):
  def discover(self, initial_nodes, username, private_key):
    "Takes a list of node addresses and returns discovered openstack installation info"
    openstack = Openstack()

    private_key_file = None
    if private_key:
      private_key_file = tempfile.NamedTemporaryFile(suffix='.key')
      private_key_file.write(private_key)
      private_key_file.flush()

    for address in initial_nodes:
      try:
        m = host_port_re.match(address)
        if m:
          host = m.group(1)
          port = int(m.group(2))
        else:
          host = address
          port = 22
        client = NodeClient(host, ssh_port=port, username=username, private_key_file=private_key_file.name)
        client.run(['echo', 'test'])
      except:
        openstack.report_issue(Issue(Issue.WARNING, "Can't connect to node %s" % address))
        continue

      host = self._discover_node(client)

      if len(host.components) == 0:
        continue

      openstack.add_host(host)

    if len(openstack.hosts) == 0:
      openstack.report_issue(Issue(Issue.FATAL, "No OpenStack nodes were discovered"))

    if private_key_file:
      private_key_file.close()

    return openstack

  def _discover_node(self, client):
    hostname = client.run(['hostname']).output.strip()

    host = Host(name=hostname)
    host.id = self._collect_host_id(client)
    host.network_addresses = self._collect_host_network_addresses(client)

    keystone = self._collect_keystone_data(client)
    if keystone:
      host.add_component(keystone)

    nova_compute = self._collect_nova_data(client)
    if nova_compute:
      host.add_component(nova_compute)

    return host


  def _find_python_process(self, client, name):
    processes = self._get_processes(client)
    for line in processes:
      if len(line) > 0 and (line[0] == name or line[0].endswith('/'+name)):
        return line
      if len(line) > 1 and python_re.match(line[0]) and (line[1] == name or line[1].endswith('/'+name)):
        return line

    return None

  def _find_python_package_version(self, client, package):
    result = client.run(['python', '-c', 'import pkg_resources; version = pkg_resources.get_provider(pkg_resources.Requirement.parse("%s")).version; print(version)' % package])
    
    s = result.output.strip()
    parts = []
    for p in s.split('.'):
      if not p[0].isdigit(): break

      parts.append(p)

    version = '.'.join(parts)

    return version

  def _get_processes(self, client):
    return [line.split() for line in client.run(['ps', '-Ao', 'cmd', '--no-headers']).output.split("\n")]

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

  def _get_keystone_db_data(self, client, command, env={}):
    result = client.run(['keystone', command], update_env=env)
    if result.return_code != 0:
      return []

    lines = result.output.strip().split("\n")

    columns = []
    last_pos = 0
    l = lines[0]
    while True:
      pos = l.find('+', last_pos+1)
      if pos == -1:
        break

      columns.append({'start': last_pos+1, 'end': pos-1})

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
    if p != -1 and p+1 < len(keystone_process):
      config_path = keystone_process[p+1]
    else:
      config_path = '/etc/keystone/keystone.conf'

    keystone = KeystoneComponent(config_path)
    keystone.version = self._find_python_package_version(client, 'keystone')
    with client.open(config_path) as f:
      keystone.config_contents = f.read()

    token = keystone.config['DEFAULT']['admin_token']
    host = keystone.config['DEFAULT']['bind_host']
    if host == '0.0.0.0':
      host = '127.0.0.1'
    port = int(keystone.config['DEFAULT']['admin_port'])

    keystone_env = {
      'OS_SERVICE_TOKEN': token,
      'OS_SERVICE_ENDPOINT': 'http://%s:%d/v2.0' % (host, port)
    }

    keystone.db = dict()
    keystone.db['tenants'] = self._get_keystone_db_data(client, 'tenant-list', env=keystone_env)
    keystone.db['users'] = self._get_keystone_db_data(client, 'user-list', env=keystone_env)
    keystone.db['services'] = self._get_keystone_db_data(client, 'service-list', env=keystone_env)
    keystone.db['endpoints'] = self._get_keystone_db_data(client, 'endpoint-list', env=keystone_env)

    return keystone

  def _collect_nova_data(self, client):
    keystone_process = self._find_python_process(client, 'nova-compute')
    if not keystone_process:
      return None

    p = index(keystone_process, lambda s: s == '--config-file')
    if p != -1 and p+1 < len(keystone_process):
      config_path = keystone_process[p+1]
    else:
      config_path = '/etc/nova/nova.conf'

    nova_compute = NovaComputeComponent(config_path)
    nova_compute.version = self._find_python_package_version(client, 'nova')
    with client.open(config_path) as f:
      nova_compute.config_contents = f.read()

    nova_compute.paste_config_path = path_relative_to(nova_compute.config['DEFAULT']['api_paste_config'], os.path.dirname(config_path))
    with client.open(nova_compute.paste_config_path) as f:
      nova_compute.paste_config_contents = f.read()

    return nova_compute

