
class Openstack(object):
  def __init__(self, components):
    super(Openstack, self).__init__()
    self.components = components

class OpenstackComponent(object):
  def __init__(self, name, configs=[]):
    super(OpenstackComponent, self).__init__()
    self.name = name

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

class ConfigSection(Element):
  def __init__(self, start_mark, end_mark, name, parameters):
    super(ConfigSection, self).__init__(start_mark, end_mark)
    self.name = name
    self.parameters = parameters

class ConfigSectionName(Element):
  def __init__(self, start_mark, end_mark, text):
    super(ConfigSectionName, self).__init__(start_mark, end_mark)
    self.text = text

class ConfigParameter(Element):
  def __init__(self, start_mark, end_mark, name, value):
    super(ConfigParameter, self).__init__(start_mark, end_mark)
    self.name = name
    self.value = value

  def __eq__(self, other):
    return (self.name.text == other.name.text) and (self.value.text == other.value.text)

  def __ne__(self, other):
    return not self == other
    
  def __repr__(self):
    return "<ConfigParameter %s=%s>" % (self.name.text, self.value.text)


class ConfigParameterName(Element):
  def __init__(self, start_mark, end_mark, text):
    super(ConfigParameterName, self).__init__(start_mark, end_mark)
    self.text = text

class ConfigParameterValue(Element):
  def __init__(self, start_mark, end_mark, text):
    super(ConfigParameterValue, self).__init__(start_mark, end_mark)
    self.text = text


