from ostack_validator.common import Inspection, MarkedError, Mark, find, index

class Version:
  def __init__(self, major, minor=0, maintenance=0):
    "Create Version object by either passing 3 integers, one string or an another Version object"
    if isinstance(major, str):
      self.parts = [int(x) for x in major.split('.', 3)]
    elif isinstance(major, Version):
      self.parts = major.parts
    else:
      self.parts = [int(major), int(minor), int(maintenance)]

  @property
  def major(self):
    return self.parts[0]

  @major.setter
  def major(self, value):
    self.parts[0] = int(value)

  @property
  def minor(self):
    return self.parts[1]

  @minor.setter
  def minor(self, value):
    self.parts[1] = int(value)

  @property
  def maintenance(self):
    return self.parts[2]

  @maintenance.setter
  def maintenance(self, value):
    self.parts[2] = value

  def __str__(self):
    return '.'.join([str(p) for p in self.parts])

  def __repr__(self):
    return '<Version %s>' % str(self)

  def __cmp__(self, other):
    for i in xrange(0, 3):
      x = self.parts[i] - other.parts[i]
      if x != 0:
        return -1 if x < 0 else 1

    return 0

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

class SchemaBuilder(object):
  def __init__(self, data):
    super(SchemaBuilder, self).__init__()
    self.data = data

    self.current_version = None
    self.current_section = None
    self.adds = []
    self.removals = []

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
    if not 'section' in kwargs and self.current_section:
      kwargs['section'] = self.current_section

    self.adds.append(ConfigParameterSchema(*args, **kwargs))

  def remove_param(self, name):
    self.removals.append(name)

  def commit(self):
    "Finalize schema building"
    if len(self.removals) > 0:
      self.data.append(SchemaUpdateRecord(self.current_version, 'remove', self.removals))
      self.removals = []
    if len(self.adds) > 0:
      self.data.append(SchemaUpdateRecord(self.current_version, 'add', self.adds))
      self.adds = []

class ConfigSchemaRegistry:
  __schemas = {}
  @classmethod
  def register_schema(self, project, configname=None):
    if not configname:
      configname = '%s.conf' % project
    fullname = '%s/%s' % (project, configname)
    self.__schemas[fullname] = []
    return SchemaBuilder(self.__schemas[fullname])

  @classmethod
  def get_schema(self, project, version, configname=None):
    if not configname:
      configname = '%s.conf' % project
    fullname = '%s/%s' % (project, configname)
    version = Version(version)

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

  def get_parameter(name, section=None):
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


class InvalidValueError(MarkedError):
  def __init__(self, message, mark=Mark('', 1, 1)):
    super(InvalidValueError, self).__init__(message, mark)

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

@type_validator('boolean', values=['True', 'False'])
def validate_enum(s, values=[]):
  if s in values:
    return None
  return InvalidValueError('Invalid value: valid values are: %s' % ', '.join(values))

@type_validator('string')
def validate_string(s):
  return None

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

  return None


