import sys

from rubick.common import Issue, MarkedIssue, Mark, Version, find, index


class SchemaUpdateRecord(object):
    # checkpoint's data is version number

    def __init__(self, version, operation, data=None):
        super(SchemaUpdateRecord, self).__init__()
        if not operation in ['checkpoint', 'add', 'remove']:
            raise Error('Unknown operation "%s"' % operation)
        version = Version(version)
        self.version = version
        self.operation = operation
        self.data = data

    def __repr__(self):
        return (
            '<SchemaUpdateRecord %s %s %s' % (
                self.version,
                self.operation,
                self.data)
        )


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
            sys.stderr.write(
                "WARNING: Uncommitted config schema \"%s\" version %s\n" %
                (self.name, self.current_version))

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
            self.data.append(
                SchemaUpdateRecord(
                    self.current_version,
                    'remove',
                    self.removals))
            self.removals = []
        if len(self.adds) > 0:
            self.data.append(
                SchemaUpdateRecord(
                    self.current_version,
                    'add',
                    self.adds))
            self.adds = []

    def _ensure_version(self):
        if not self.current_version:
            raise Error(
                'Schema version is not specified. Please call version() '
                'method first')


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
        i = len(records) - 1
        # Find latest checkpoint prior given version
        while i >= 0 and not (records[i].operation == 'checkpoint'
                              and records[i].version <= version):
            i -= 1

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
                        old_param_index = index(
                            parameters,
                            lambda p: p.name == param.name)
                        if old_param_index != -1:
                            parameters[old_param_index] = param
                    else:
                        parameters.append(param)
                        seen_parameters.add(param.name)
            elif records[i].operation == 'remove':
                for param_name in records[i].data:
                    param_index = index(
                        parameters,
                        lambda p: p.name == param_name)
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

    def has_section(self, section):
        return (
            find(self.parameters, lambda p: p.section == section) is not None
        )

    def get_parameter(self, name, section=None):
        # TODO: optimize this
        return (
            find(
                self.parameters,
                lambda p: p.name == name and p.section == section)
        )

    def __repr__(self):
        return (
            '<ConfigSchema name=%s version=%s format=%s parameters=%s>' % (
                self.name, self.version, self.format, self.parameters)
        )


class ConfigParameterSchema:

    def __init__(
        self,
        name,
        type,
        section=None,
        description=None,
        default=None,
        required=False,
            deprecation_message=None):
        self.section = section
        self.name = name
        self.type = type
        self.description = description
        self.default = default
        self.required = required
        self.deprecation_message = deprecation_message

    def __repr__(self):
        return (
            '<ConfigParameterSchema %s>' % ' '.join(
                ['%s=%s' % (attr, getattr(self, attr))
                                                    for attr in ['section',
                                                                 'name',
                                                                 'type',
                                                                 'description',
                                                                 'default',
                                                                 'required']])
        )


class TypeValidatorRegistry:
    __validators = {}

    @classmethod
    def register_validator(self, type_name, type_validator):
        self.__validators[type_name] = type_validator

    @classmethod
    def get_validator(self, name):
        return self.__validators[name]


class SchemaError(Issue):

    def __init__(self, message):
        super(SchemaError, self).__init__(Issue.ERROR, message)


class InvalidValueError(MarkedIssue):

    def __init__(self, message, mark=Mark('', 0, 0)):
        super(
            InvalidValueError,
            self).__init__(
            Issue.ERROR,
            'Invalid value: ' +
            message,
            mark)


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


def isissue(o):
    return isinstance(o, Issue)


@type_validator('boolean')
def validate_boolean(s):
    s = s.lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        return InvalidValueError('Value should be "true" or "false"')


def validate_enum(s, values=[]):
    if s in values:
        return None
    if len(values) == 0:
        message = 'There should be no value'
    elif len(values) == 1:
        message = 'The only valid value is %s' % values[0]
    else:
        message = 'Valid values are %s and %s' % (
            ', '.join(values[:-1]), values[-1])
    return InvalidValueError('%s' % message)


def validate_ipv4_address(s):
    s = s.strip()
    parts = s.split('.')
    if len(parts) == 4:
        if all([all([c.isdigit() for c in part]) for part in parts]):
            parts = [int(part) for part in parts]
            if all([part < 256 for part in parts]):
                return '.'.join([str(part) for part in parts])

    return InvalidValueError('Value should be ipv4 address')


def validate_ipv4_network(s):
    s = s.strip()
    parts = s.split('/')
    if len(parts) != 2:
        return (
            InvalidValueError(
                'Should have "/" character separating address and prefix '
                'length')
        )

    address, prefix = parts
    prefix = prefix.strip()

    if prefix.strip() == '':
        return InvalidValueError('Prefix length is required')

    address = validate_ipv4_address(address)
    if isissue(address):
        return address

    if not all([c.isdigit() for c in prefix]):
        return InvalidValueError('Prefix length should be an integer')

    prefix = int(prefix)
    if prefix > 32:
        return (
            InvalidValueError(
                'Prefix length should be less than or equal to 32')
        )

    return '%s/%d' % (address, prefix)


def validate_host_label(s):
    if len(s) == 0:
        return (
            InvalidValueError('Host label should have at least one character')
        )

    if not s[0].isalpha():
        return (
            InvalidValueError(
                'Host label should start with a letter, but it starts with '
                '"%s"' % s[0])
        )

    if len(s) == 1:
        return s

    if not (s[-1].isdigit() or s[-1].isalpha()):
        return (
            InvalidValueError(
                'Host label should end with letter or digit, but it ends '
                'with "%s"' %
                s[-1], Mark('', 0, len(s) - 1))
        )

    if len(s) == 2:
        return s

    for i, c in enumerate(s[1:-1]):
        if not (c.isalpha() or c.isdigit() or c == '-'):
            return (
                InvalidValueError(
                    'Host label should contain only letters, digits or hypens,'
                    ' but it contains "%s"' %
                    c, Mark('', 0, i + 1))
            )

    return s


@type_validator('host')
@type_validator('host_address')
def validate_host_address(s):
    result = validate_ipv4_address(s)
    if not isissue(result):
        return result

    offset = len(s) - len(s.lstrip())

    parts = s.strip().split('.')
    part_offset = offset
    labels = []
    for part in parts:
        host_label = validate_host_label(part)
        if isissue(host_label):
            return host_label.offset_by(Mark('', 0, part_offset))

        part_offset += len(part) + 1
        labels.append(host_label)

    return '.'.join(labels)


@type_validator('network')
@type_validator('network_address')
def validate_network_address(s):
    return validate_ipv4_network(s)


@type_validator('host_and_port')
def validate_host_and_port(s, default_port=None):
    parts = s.strip().split(':', 2)

    host_address = validate_host_address(parts[0])
    if isissue(host_address):
        return host_address

    if len(parts) == 2:
        port = validate_port(parts[1])
        if isissue(port):
            return port
    elif default_port:
        port = default_port
    else:
        return InvalidValueError('No port specified')

    return (host_address, port)


@type_validator('string')
@type_validator('list')
@type_validator('multi')
def validate_string(s):
    return s


@type_validator('integer')
def validate_integer(s, min=None, max=None):
    leading_whitespace_len = 0
    while leading_whitespace_len < len(s) \
        and s[leading_whitespace_len].isspace():
        leading_whitespace_len += 1

    s = s.strip()
    if s == '':
        return InvalidValueError('Should not be empty')

    for i, c in enumerate(s):
        if not c.isdigit() and not ((c == '-') and (i == 0)):
            return (
                InvalidValueError(
                    'Only digits are allowed, but found char "%s"' %
                    c, Mark('', 1, i + 1 + leading_whitespace_len))
            )

    v = int(s)
    if min and v < min:
        return (
            InvalidValueError(
                'Should be greater than or equal to %d' %
                min, Mark('', 1, leading_whitespace_len))
        )
    if max and v > max:
        return (
            InvalidValueError(
                'Should be less than or equal to %d' %
                max, Mark('', 1, leading_whitespace_len))
        )

    return v


@type_validator('float')
def validate_float(s):
    # TODO: Implement proper validation
    return float(s)


@type_validator('port')
def validate_port(s, min=1, max=65535):
    return validate_integer(s, min=min, max=max)


@type_validator('string_list')
def validate_list(s, element_type='string'):
    element_type_validator = TypeValidatorRegistry.get_validator(element_type)
    if not element_type_validator:
        return SchemaError('Invalid element type "%s"' % element_type)

    result = []
    s = s.strip()

    if s == '':
        return result

    values = s.split(',')
    for value in values:
        validated_value = element_type_validator.validate(value.strip())
        if isinstance(validated_value, Issue):
            # TODO: provide better position reporting
            return validated_value
        result.append(validated_value)

    return result


@type_validator('string_dict')
def validate_dict(s, element_type='string'):
    element_type_validator = TypeValidatorRegistry.get_validator(element_type)
    if not element_type_validator:
        return SchemaError('Invalid element type "%s"' % element_type)

    result = {}
    s = s.strip()

    if s == '':
        return result

    pairs = s.split(',')
    for pair in pairs:
        key_value = pair.split(':', 2)
        if len(key_value) < 2:
            return (
                InvalidValueError(
                    'Value should be NAME:VALUE pairs separated by ","')
            )

        key, value = key_value
        key = key.strip()
        value = value.strip()

        if key == '':
            # TODO: provide better position reporting
            return InvalidValueError('Key name should not be empty')

        validated_value = element_type_validator.validate(value)
        if isinstance(validated_value, Issue):
            # TODO: provide better position reporting
            return validated_value
        result[key] = validated_value
    return result
