import os.path
import re
import logging
from itertools import groupby

from ostack_validator.common import Mark, Issue, MarkedIssue, path_relative_to
from ostack_validator.schema import ConfigSchemaRegistry, TypeValidatorRegistry
from ostack_validator.config_model import Configuration
import ostack_validator.schemas
from ostack_validator.config_formats import IniConfigParser

class IssueReporter(object):
  def __init__(self):
    super(IssueReporter, self).__init__()
    self.issues = []

  def report(self, issue):
    self.issues.append(issue)

class Openstack(object):
  def __init__(self):
    super(Openstack, self).__init__()
    self.hosts = []
    self.issue_reporter = IssueReporter()

  def add_host(self, host):
    self.hosts.append(host)
    host.parent = self

  def report_issue(self, issue):
    self.issue_reporter.report(issue)

  @property
  def issues(self):
    return self.issue_reporter.issues

class Host(object):
  def __init__(self, name, metadata, client):
    super(Host, self).__init__()
    self.name = name
    self.metadata = metadata
    self.client = client
    self.components = []

  def add_component(self, component):
    self.components.append(component)
    component.parent = self

  @property
  def openstack(self):
    return self.parent

  @property
  def id(self):
    ether_re = re.compile('link/ether (([0-9a-f]{2}:){5}([0-9a-f]{2})) ')
    result = self.client.run(['bash', '-c', 'ip link | grep "link/ether "'])
    macs = []
    for match in ether_re.finditer(result.output):
      macs.append(match.group(1).replace(':', ''))
    return ''.join(macs)
    

  @property
  def network_addresses(self):
    ipaddr_re = re.compile('inet (\d+\.\d+\.\d+\.\d+)/\d+')
    addresses = []
    result = self.client.run(['bash', '-c', 'ip address list | grep "inet "'])
    for match in ipaddr_re.finditer(result.output):
      addresses.append(match.group(1))
    return addresses

  def __getstate__(self):
    return {
      'name': self.name,
      'metadata': self.metadata,
      'client': None,
      'components': self.components,
      'parent': self.parent
    }

class Service(object): pass

class OpenstackComponent(Service):
  logger = logging.getLogger('ostack_validator.model.openstack_component')
  component = None

  def __init__(self, config_path):
    super(OpenstackComponent, self).__init__()
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


  @property
  def version(self):
    if not hasattr(self, '_version'):
      result = self.host.client.run(['python', '-c', 'import pkg_resources; version = pkg_resources.get_provider(pkg_resources.Requirement.parse("%s")).version; print(version)' % self.component])
      
      s = result.output.strip()
      parts = []
      for p in s.split('.'):
        if not p[0].isdigit(): break

        parts.append(p)

      self._version = '.'.join(parts)

    return self._version
    

  def _parse_config_file(self, base_mark, config_contents, schema=None, issue_reporter=None):
    if issue_reporter:
      def report_issue(issue):
        issue_reporter.report_issue(issue)
    else:
      def report_issue(issue): pass

    _config = Configuration()

    # Apply defaults
    if schema:
      for parameter in filter(lambda p: p.default, schema.parameters):
        _config.set_default(parameter.section, parameter.name, parameter.default)
      
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
        unknown_section = False
        if schema:
          unknown_section = not schema.has_section(section.name.text)

        if unknown_section:
          report_issue(MarkedIssue(Issue.WARNING, 'Unknown section "%s"' % (section_name), section.start_mark))
          continue

        for parameter in section.parameters:
          parameter_schema = None
          if schema:
            parameter_schema = schema.get_parameter(name=parameter.name.text, section=section.name.text)
            if not (parameter_schema or unknown_section):
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

              _config.set(section_name, parameter.name.text, value)

              # if value == parameter_schema.default:
              #   report_issue(MarkedIssue(Issue.INFO, 'Explicit value equals default: section "%s" parameter "%s"' % (section_name, parameter.name.text), parameter.start_mark))
          else:
            _config.set(section_name, parameter.name.text, parameter.value.text)

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


