import sys

from ostack_validator.common import Inspection, Issue, MarkedIssue, Mark, Version, find, index

class SchemaUpdateRecord(object):
  # checkpoint's data is version number
  def __init__(self, version, operation, data=None):
    super(SchemaUpdateRecord, self).__init__()
    if not operation in ['checkpoint', 'add', 'remove']:
      raise Error, 'Unknown operation "%s"' % operation
    version = Version(version)
    self.version = version
    self.operation = operation
    self.data = data

  def __repr__(self):
    return '<SchemaUpdateRecord %s %s %s' % (self.version, self.operation, self.data)

class SchemaBuilder(object):
  def __init__(self, name, data):
    super(SchemaBuilder, self).__init__()
    self.name = name
    self.data = data

    self.current_version = None
    self.current_section = None
    self.adds = []
    self.removals = []

  def __del__(self):
    if len(self.adds) > 0 or len(self.removals) > 0:
      sys.stderr.write("WARNING: Uncommitted config schema \"%s\" version %s\n" % (self.name, self.current_version))

  def version(self, version, checkpoint=False):
    version = Version(version)

    if self.current_version and self.current_version != version:
      self.commit()

    if checkpoint or self.data == []:
      self.data.append(SchemaUpdateRecord(version, 'checkpoint'))

    self.current_version = version

  def section(self, name):
    self.current_section = name

  def param(self, *args, **kwargs):
    self._ensure_version()

    if not 'section' in kwargs and self.current_section:
      kwargs['section'] = self.current_section

    self.adds.append(ConfigParameterSchema(*args, **kwargs))

  def remove_param(self, name):
    self._ensure_version()

    self.removals.append(name)

  def commit(self):
    "Finalize schema building"
    self._ensure_version()

    if len(self.removals) > 0:
      self.data.append(SchemaUpdateRecord(self.current_version, 'remove', self.removals))
      self.removals = []
    if len(self.adds) > 0:
      self.data.append(SchemaUpdateRecord(self.current_version, 'add', self.adds))
      self.adds = []

  def _ensure_version(self):
    if not self.current_version:
      raise Error, 'Schema version is not specified. Please call version() method first'

class ConfigSchemaRegistry:
  __schemas = {}
  @classmethod
  def register_schema(self, project, configname=None):
    if not configname:
      configname = '%s.conf' % project
    fullname = '%s/%s' % (project, configname)
    self.__schemas[fullname] = []
    return SchemaBuilder(fullname, self.__schemas[fullname])

  @classmethod
  def get_schema(self, project, version, configname=None):
    if not configname:
      configname = '%s.conf' % project
    fullname = '%s/%s' % (project, configname)
    version = Version(version)

    if not fullname in self.__schemas:
      return None

    records = self.__schemas[fullname]
    i = len(records)-1
    # Find latest checkpoint prior given version
    while i>=0 and not (records[i].operation == 'checkpoint' and records[i].version <= version): i-=1

    if i < 0:
      return None

    parameters = []
    seen_parameters = set()
    last_version = None

    while i < len(records) and records[i].version <= version:
      last_version = records[i].version
      if records[i].operation == 'add':
        for param in records[i].data:
          if param.name in seen_parameters:
            old_param_index = index(parameters, lambda p: p.name == param.name)
            if old_param_index != -1:
              parameters[old_param_index] = param
          else:
            parameters.append(param)
            seen_parameters.add(param.name)
      elif records[i].operation == 'remove':
        for param_name in records[i].data:
          param_index = index(parameters, lambda p: p.name == param_name)
          if index != -1:
            parameters.pop(param_index)
            seen_parameters.remove(param_name)
      i += 1

    return ConfigSchema(fullname, last_version, 'ini', parameters)


class ConfigSchema:
  def __init__(self, name, version, format, parameters):
    self.name = name
    self.version = Version(version)
    self.format = format
    self.parameters = parameters

  def get_parameter(self, name, section=None):
    # TODO: optimize this
    return find(self.parameters, lambda p: p.name == name and p.section == section)

  def __repr__(self):
    return '<ConfigSchema name=%s version=%s format=%s parameters=%s>' % (self.name, self.version, self.format, self.parameters)
    
class ConfigParameterSchema:
  def __init__(self, name, type, section=None, description=None, default=None, required=False):
    self.section = section
    self.name = name
    self.type = type
    self.description = description
    self.default = default
    self.required = required

  def __repr__(self):
    return '<ConfigParameterSchema %s>' % ' '.join(['%s=%s' % (attr, getattr(self, attr)) for attr in ['section', 'name', 'type', 'description', 'default', 'required']])


class TypeValidatorRegistry:
  __validators = {}
  @classmethod
  def register_validator(self, type_name, type_validator):
    self.__validators[type_name] = type_validator

  @classmethod
  def get_validator(self, name):
    return self.__validators[name]


class InvalidValueError(MarkedIssue):
  def __init__(self, message, mark=Mark('', 1, 1)):
    super(InvalidValueError, self).__init__(Issue.ERROR, message, mark)

class TypeValidator(object):
  def __init__(self, f):
    super(TypeValidator, self).__init__()
    self.f = f

  def validate(self, value):
    return getattr(self, 'f')(value)


def type_validator(name, **kwargs):
  def wrap(fn):
    def wrapped(s):
      return fn(s, **kwargs)
    o = TypeValidator(wrapped)
    TypeValidatorRegistry.register_validator(name, o)
    return fn
  return wrap

@type_validator('boolean')
def validate_boolean(s):
  s = s.lower()
  if s == 'true':
    return True
  elif s == 'false':
    return False
  else:
    return InvalidValueError('Invalid value: value should be "true" or "false"')

def validate_enum(s, values=[]):
  if s in values:
    return None
  if len(values) == 0:
    message = 'there should be no value'
  elif len(values) == 1:
    message = 'the only valid value is %s' % values[0]
  else:
    message = 'valid values are %s and %s' % (', '.join(values[:-1]), values[-1])
  return InvalidValueError('Invalid value: %s' % message)

@type_validator('host')
@type_validator('string')
@type_validator('stringlist')
def validate_string(s):
  return s

@type_validator('integer')
@type_validator('port', min=1, max=65535)
def validate_integer(s, min=None, max=None):
  leading_whitespace_len = 0
  while s[leading_whitespace_len].isspace(): leading_whitespace_len += 1

  s = s.strip()
  for i, c in enumerate(s):
    if not c.isdigit() and not ((c == '-') and (i == 0)):
      return InvalidValueError('Invalid value: only digits are allowed, but found char "%s"' % c, Mark('', 1, i+1+leading_whitespace_len))

  v = int(s)
  if min and v < min:
    return InvalidValueError('Invalid value: should be greater than or equal to %d' % min, Mark('', 1, leading_whitespace_len))
  if max and v > max:
    return InvalidValueError('Invalid value: should be less than or equal to %d' % max, Mark('', 1, leading_whitespace_len))

  return v


