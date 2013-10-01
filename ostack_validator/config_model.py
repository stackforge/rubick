from ostack_validator.common import Mark

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

