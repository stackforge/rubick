from ostack_validator.common import Mark

class Openstack(object):
  def __init__(self, hosts, resource_locator, config_parser):
    super(Openstack, self).__init__()
    self.hosts = hosts
    self.resource_locator = resource_locator
    self.config_parser = config_parser
    for host in self.hosts:
      host.parent = self

class Host(object):
  def __init__(self, name, metadata, components):
    super(Host, self).__init__()
    self.name = name
    self.metadata = metadata
    self.components = components
    for component in self.components:
      component.parent = self

class OpenstackComponent(object):
  def __init__(self, name, version):
    super(OpenstackComponent, self).__init__()
    self.name = name
    self.version = version
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
      resource = self.openstack.resource_locator.find_resource(self.host.name, self.name, config_name)
      if resource:
        config = self.openstack.config_parser.parse(config_name, resource.get_contents())
        config.mark = Mark(resource.name)
        self.configs[config_name] = config
      else:
        self.configs[config_name] = None

    return self.configs[config_name]

class ComponentConfig(object):
  def __init__(self, name, mark, sections=[], errors=[]):
    super(ComponentConfig, self).__init__()
    self.name = name
    self.mark = mark
    self.sections = sections
    for section in self.sections:
      section.parent = self

    self.errors = errors

class Element(object):
  def __init__(self, start_mark, end_mark):
    self.start_mark = start_mark
    self.end_mark = end_mark

  def __eq__(self, other):
    return (self.__class__ == other.__class__) and (self.start_mark == other.start_mark) and (self.end_mark == other.end_mark)

  def __ne__(self, other):
    return not self == other

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
  def __init__(self, start_mark, end_mark, text, quotechar=None):
    super(ConfigParameterValue, self).__init__(start_mark, end_mark, text)
    self.quotechar = quotechar


