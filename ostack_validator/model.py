import os.path
import re

from ostack_validator.common import Mark

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
  def network_addresses(self):
    ipaddr_re = re.compile('inet (\d+\.\d+\.\d+\.\d+)/\d+')
    addresses = []
    result = self.client.run(['bash', '-c', 'ip address list | grep "inet "'])
    for match in ipaddr_re.finditer(result.output):
      addresses.append(match.group(1))
    return addresses

class OpenstackComponent(object):
  def __init__(self, name, version, base_path=None):
    super(OpenstackComponent, self).__init__()
    self.name = name
    self.version = version
    self.base_path = base_path or '/etc/%s' % self.name
    self.configs = {}

  @property
  def host(self):
    return self.parent

  @property
  def openstack(self):
    return self.host.parent

  def get_config(self, config_name=None):
    if config_name is None:
      config_name = '%s.conf' % self.name

    if not config_name in self.configs:
      resource = self.openstack.resource_locator.find_resource('file', name=os.path.join(self.base_path, config_name), host=self.host.name)
      if resource:
        config = self.openstack.config_parser.parse(config_name, Mark(resource.name), resource.get_contents())
        self.configs[config_name] = config
      else:
        self.configs[config_name] = None

    return self.configs[config_name]

class Element(object):
  def __init__(self, start_mark, end_mark):
    self.start_mark = start_mark
    self.end_mark = end_mark

  def __eq__(self, other):
    return (self.__class__ == other.__class__) and (self.start_mark == other.start_mark) and (self.end_mark == other.end_mark)

  def __ne__(self, other):
    return not self == other

class ComponentConfig(Element):
  def __init__(self, start_mark, end_mark, name, sections=[], errors=[]):
    super(ComponentConfig, self).__init__(start_mark, end_mark)
    self.name = name
    self.sections = sections
    for section in self.sections:
      section.parent = self

    self.errors = errors

class TextElement(Element):
  def __init__(self, start_mark, end_mark, text):
    super(TextElement, self).__init__(start_mark, end_mark)
    self.text = text

class ConfigSection(Element):
  def __init__(self, start_mark, end_mark, name, parameters):
    super(ConfigSection, self).__init__(start_mark, end_mark)
    self.name = name
    self.parameters = parameters
    for parameter in self.parameters:
      parameter.parent = self

class ConfigSectionName(TextElement): pass

class ConfigParameter(Element):
  def __init__(self, start_mark, end_mark, name, value, delimiter):
    super(ConfigParameter, self).__init__(start_mark, end_mark)
    self.name = name
    self.name.parent = self

    self.value = value
    self.value.parent = self

    self.delimiter = delimiter
    self.delimiter.parent = self

  def __eq__(self, other):
    return (self.name.text == other.name.text) and (self.value.text == other.value.text)

  def __ne__(self, other):
    return not self == other
    
  def __repr__(self):
    return "<ConfigParameter %s=%s delimiter=%s>" % (self.name.text, self.value.text, self.delimiter.text)


class ConfigParameterName(TextElement): pass

class ConfigParameterValue(TextElement):
  def __init__(self, start_mark, end_mark, text, value=None, quotechar=None):
    super(ConfigParameterValue, self).__init__(start_mark, end_mark, text)
    self.value = value
    self.quotechar = quotechar

