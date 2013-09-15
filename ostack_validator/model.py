
class Openstack(object):
  def __init__(self, components):
    super(Openstack, self).__init__()
    self.components = components

class OpenstackComponent(object):
  def __init__(self, name, version, configs=[]):
    super(OpenstackComponent, self).__init__()
    self.name = name
    self.version = version

class ComponentConfig(object):
  def __init__(self, name, sections=[]):
    super(ComponentConfig, self).__init__()
    self.name = name
    self.sections = sections

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

class ConfigSectionName(TextElement): pass

class ConfigParameter(Element):
  def __init__(self, start_mark, end_mark, name, value, delimiter):
    super(ConfigParameter, self).__init__(start_mark, end_mark)
    self.name = name
    self.value = value
    self.delimiter = delimiter

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


