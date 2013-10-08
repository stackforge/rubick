import os.path
import re
import sys
import tempfile
import logging

import spur

from ostack_validator.common import Issue, Mark, MarkedIssue, index
from ostack_validator.model import Openstack, Host, OpenstackComponent, KeystoneComponent, NovaComputeComponent, GlanceApiComponent



class NodeClient(object):
  def __init__(self, node_address, username, private_key_file, ssh_port=22):
    super(NodeClient, self).__init__()
    self.shell = spur.SshShell(hostname=node_address, port=ssh_port, username=username, private_key_file=private_key_file, missing_host_key=spur.ssh.MissingHostKey.accept)

  def run(self, command):
    return self.shell.run(command)

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
    metadata = {}

    host = Host(name=hostname, metadata=metadata, client=client)

    processes = [line.split() for line in client.run(['ps', '-Ao', 'cmd', '--no-headers']).output.split("\n")]

    keystone_process = self._find_python_process(processes, 'keystone-all')
    if keystone_process:
      p = index(keystone_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(keystone_process):
        config_file = keystone_process[p+1]
      else:
        config_file = '/etc/keystone/keystone.conf'

      host.add_component(KeystoneComponent(config_file))

    glance_api_process = self._find_python_process(processes, 'glance-api')
    if glance_api_process:
      p = index(glance_api_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(glance_api_process):
        config_file = glance_api_process[p+1]
      else:
        config_file = '/etc/glance/glance-api.conf'

      host.add_component(GlanceApiComponent(config_file))

    nova_compute_process = self._find_python_process(processes, 'nova-compute')
    if nova_compute_process:
      p = index(nova_compute_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(nova_compute_process):
        config_file = nova_compute_process[p+1]
      else:
        config_file = '/etc/nova/nova.conf'

      host.add_component(NovaComputeComponent(config_file))

    return host


  def _find_python_process(self, processes, name):
    for line in processes:
      if len(line) > 0 and (line[0] == name or line[0].endswith('/'+name)):
        return line
      if len(line) > 1 and python_re.match(line[0]) and (line[1] == name or line[1].endswith('/'+name)):
        return line

    return None

