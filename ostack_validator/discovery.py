import os.path
import re
import sys
import tempfile
import logging
from itertools import groupby

import spur

from ostack_validator.common import Issue, Mark, MarkedIssue, index
from ostack_validator.model import Openstack, Host
from ostack_validator.schema import ConfigSchemaRegistry, TypeValidatorRegistry
import ostack_validator.schemas
from ostack_validator.config_formats import IniConfigParser


def path_relative_to(path, base_path):
  if not path.startswith('/'):
    path = os.path.join(base_path, paste_config_path)

  return path


class NodeClient(object):
  def __init__(self, node_address, username, private_key_file):
    super(NodeClient, self).__init__()
    self.shell = spur.SshShell(hostname=node_address, username=username, private_key_file=private_key_file, missing_host_key=spur.ssh.MissingHostKey.accept)

  def run(self, command):
    return self.shell.run(command)

  def open(self, path, mode='r'):
    return self.shell.open(path, mode)

class Service(object): pass

class OpenstackComponent(Service):
  logger = logging.getLogger('ostack_validator.model.openstack_component')
  component = None

  def __init__(self, version, config_path):
    super(OpenstackComponent, self).__init__()
    self.version = version
    self.config_path = config_path
    self.config_dir = os.path.dirname(config_path)

  @property
  def host(self):
    return self.parent

  @property
  def openstack(self):
    return self.host.openstack

  @property
  def config(self):
    if not hasattr(self, '_config'):
      schema = ConfigSchemaRegistry.get_schema(self.component, self.version)
      if not schema:
        self.logger.debug('No schema for component "%s" main config version %s. Skipping it' % (self.component, self.version))
        self._config = None
      else:
        with self.host.client.open(self.config_path) as f:
          config_contents = f.read()

        self._config = self._parse_config_file(Mark('%s:%s' % (self.host.name, self.config_path)), config_contents, schema, self.openstack)

    return self._config
    

  def _parse_config_file(self, base_mark, config_contents, schema=None, issue_reporter=None):
    if issue_reporter:
      def report_issue(issue):
        issue_reporter.report_issue(issue)
    else:
      def report_issue(issue): pass

    _config = dict()

    # Apply defaults
    if schema:
      for parameter in schema.parameters:
        if not parameter.default: continue

        if not parameter.section in _config:
          _config[parameter.section] = {}

        if parameter.name in _config[parameter.section]: continue

        _config[parameter.section][parameter.name] = parameter.default
      
    # Parse config file

    config_parser = IniConfigParser()
    parsed_config = config_parser.parse('', base_mark, config_contents)
    for error in parsed_config.errors:
      report_issue(error)

    # Validate config parameters and store them
    section_name_text_f = lambda s: s.name.text
    sections_by_name = groupby(sorted(parsed_config.sections, key=section_name_text_f), key=section_name_text_f)

    for section_name, sections in sections_by_name:
      sections = list(sections)

      if len(sections) > 1:
        report_issue(Issue(Issue.INFO, 'Section "%s" appears multiple times' % section_name))

      seen_parameters = set()

      for section in sections:
        for parameter in section.parameters:
          parameter_schema = None
          if schema:
            parameter_schema = schema.get_parameter(name=parameter.name.text, section=section.name.text)
            if not parameter_schema:
              report_issue(MarkedIssue(Issue.WARNING, 'Unknown parameter: section "%s" name "%s"' % (section_name, parameter.name.text), parameter.start_mark))
              continue

          if parameter.name.text in seen_parameters:
            report_issue(MarkedIssue(Issue.WARNING, 'Parameter "%s" in section "%s" redeclared' % (parameter.name.text, section_name), parameter.start_mark))
          else:
            seen_parameters.add(parameter.name.text)

          if parameter_schema:
            type_validator = TypeValidatorRegistry.get_validator(parameter_schema.type)
            type_validation_result = type_validator.validate(parameter.value.text)
            if isinstance(type_validation_result, Issue):
              type_validation_result.mark = parameter.value.start_mark.merge(type_validation_result.mark)
              report_issue(type_validation_result)

            else:
              value = type_validation_result

              if not section_name in _config: _config[section_name] = {}
              _config[section_name][parameter.name.text] = value

              # if value == parameter_schema.default:
              #   report_issue(MarkedIssue(Issue.INFO, 'Explicit value equals default: section "%s" parameter "%s"' % (section_name, parameter.name.text), parameter.start_mark))
          else:
            if not section_name in _config: _config[section_name] = {}
            _config[section_name][parameter.name.text] = parameter.value.text

    return _config


class KeystoneComponent(OpenstackComponent):
  component = 'keystone'
  name = 'keystone'

class GlanceApiComponent(OpenstackComponent):
  component = 'glance'
  name = 'glance-api'

class NovaComputeComponent(OpenstackComponent):
  component = 'nova'
  name = 'nova-compute'

  @property
  def paste_config(self):
    if not hasattr(self, '_paste_config'): 
      paste_config_path = path_relative_to(self.config['DEFAULT']['api_paste_config'], self.config_dir)
      with self.host.client.open(paste_config_path) as f:
        paste_config_contents = f.read()

      self._paste_config = self._parse_config_file(
        Mark('%s:%s' % (self.host.name, paste_config_path)),
        paste_config_contents,
        issue_reporter=self.openstack
      )

    return self._paste_config


python_re = re.compile('(/?([^/]*/)*)python[0-9.]*')

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
        client = NodeClient(address, username=username, private_key_file=private_key_file.name)
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

    processes = [line.split() for line in client.run(['ps', 'axh', '-o', 'cmd']).output.split("\n")]

    keystone_process = self._find_python_process(processes, 'keystone-all')
    if keystone_process:
      p = index(keystone_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(keystone_process):
        config_file = keystone_process[p+1]
      else:
        config_file = '/etc/keystone/keystone.conf'

      # TODO: Implement me
      version = '2013.1.3'

      host.add_component(KeystoneComponent(version, config_file))

    glance_api_process = self._find_python_process(processes, 'glance-api')
    if glance_api_process:
      p = index(glance_api_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(glance_api_process):
        config_file = glance_api_process[p+1]
      else:
        config_file = '/etc/glance/glance-api.conf'

      # TODO: Implement me
      version = '2013.1.3'

      host.add_component(GlanceApiComponent(version, config_file))

    nova_compute_process = self._find_python_process(processes, 'nova-compute')
    if nova_compute_process:
      p = index(nova_compute_process, lambda s: s == '--config-file')
      if p != -1 and p+1 < len(nova_compute_process):
        config_file = nova_compute_process[p+1]
      else:
        config_file = '/etc/nova/nova.conf'

      # TODO: Implement me
      version = '2013.1.3'

      host.add_component(NovaComputeComponent(version, config_file))

    return host


  def _find_python_process(self, processes, name):
    for line in processes:
      if len(line) > 0 and (line[0] == name or line[0].endswith('/'+name)):
        return line
      if len(line) > 1 and python_re.match(line[0]) and (line[1] == name or line[1].endswith('/'+name)):
        return line

    return None

