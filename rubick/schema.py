# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import os.path
import re
import yaml

from rubick.common import Issue, MarkedIssue, Mark, Version, find, index
from rubick.exceptions import RubickException


class SchemaError(RubickException):
    pass


class ConfigSchemaLoader(object):
    db_path = os.path.join(os.path.dirname(__file__), 'schemas')

    def load(self, project, configname):
        path = os.path.join(self.db_path, project, configname + '.yml')
        if not os.path.exists(path):
            return None

        with open(path) as f:
            records = yaml.load(f.read())

        return records


class ConfigSchemaRegistry:
    @classmethod
    def get_schema(self, project, version, configname=None, schema_loader=ConfigSchemaLoader()):
        if not configname:
            configname = '%s.conf' % project
        fullname = '%s/%s' % (project, configname)
        version = Version(version)

        records = schema_loader.load(project, configname)
        if not records:
            return None

        i = len(records) - 1
        # Find latest checkpoint prior given version
        while i >= 0 and not (records[i].get('checkpoint', False)
                              and Version(records[i]['version']) <= version):
            i -= 1

        if i < 0:
            if Version(records[0]['version']) > version:
                # Reached the earliest record yet haven't found version
                return None

            # Haven't found checkpoint but yearliest version is less than given
            # Assuming first record is checkpoint
            i = 0

        parameters = []
        seen_parameters = set()
        last_version = None

        while i < len(records) and Version(records[i]['version']) <= version:
            last_version = records[i]['version']
            for param_data in records[i].get('added', []):
                name = param_data['name']
                section = None
                if '.' in name:
                    section, name = name.split('.', 1)

                param = ConfigParameterSchema(
                    name, param_data['type'], section=section,
                    type_args=param_data.get('type_args', {}),
                    default=param_data.get('default', None),
                    description=param_data.get('help', None),
                    required=param_data.get('required', False),
                    deprecation_message=param_data.get('deprecated', None))

                if param.name in seen_parameters:
                    old_param_index = index(
                        parameters,
                        lambda p: p.name == param.name)
                    if old_param_index != -1:
                        parameters[old_param_index] = param
                else:
                    parameters.append(param)
                    seen_parameters.add(param.name)
            for param_name in records[i].get('removed', []):
                param_index = index(
                    parameters,
                    lambda p: p.name == param_name)
                if index != -1:
                    parameters.pop(param_index)
                    seen_parameters.discard(param_name)
            i += 1

        return ConfigSchema(fullname, last_version, 'ini', parameters)


def param_fullname(name, section=None):
    fullname = name
    if section and section != 'DEFAULT':
        fullname = '%s.%s' % (section, name)

    return fullname


class ConfigSchema:

    def __init__(self, name, version, format, parameters):
        self.name = name
        self.version = Version(version)
        self.format = format
        self.parameters = parameters
        self._parameterByName = {}
        for param in self.parameters:
            self._parameterByName[param.fullname] = param

    def has_section(self, section):
        return (
            find(self.parameters, lambda p: p.section == section) is not None
        )

    def get_parameter(self, name, section=None):
        fullname = param_fullname(name, section)

        return self._parameterByName.get(fullname, None)

    def __len__(self):
        return len(self.parameters)

    def __iter__(self):
        for param in self.parameters:
            yield param

    def __getitem__(self, key):
        return self.get_parameter(key)

    def __contains__(self, item):
        return item in self._parameterByName

    def __repr__(self):
        return ('<ConfigSchema name=%s version=%s format=%s parameters=%s>' %
                (self.name, self.version, self.format, self.parameters))


class ConfigParameterSchema:

    def __init__(self, name, type, type_args={}, section=None, description=None,
                 default=None, required=False, deprecation_message=None):
        self.section = section or 'DEFAULT'
        self.name = name
        self.type = type
        self.type_args = type_args
        self.fullname = param_fullname(name, section)
        self.description = description
        self.default = default
        self.required = required
        self.deprecation_message = deprecation_message

    def __repr__(self):
        return (
            '<ConfigParameterSchema %s>' % ' '.join(
                ['%s=%s' % (attr, getattr(self, attr))
                    for attr in ['section', 'name', 'type', 'description',
                                 'default', 'required']])
        )


class TypeValidatorRegistry:
    __validators = {}
    __default_validator = None

    @classmethod
    def register_validator(self, type_name, type_validator, default=False):
        self.__validators[type_name] = type_validator
        if default:
            self.__default_validator = type_name

    @classmethod
    def get_validator(self, name):
        return self.__validators.get(
            name, self.__validators[self.__default_validator])


class SchemaIssue(Issue):

    def __init__(self, message):
        super(SchemaIssue, self).__init__(Issue.ERROR, message)


class InvalidValueError(MarkedIssue):

    def __init__(self, message, mark=Mark('', 0, 0)):
        super(InvalidValueError, self).__init__(
            Issue.ERROR, 'Invalid value: ' + message, mark)


class TypeValidator(object):

    def __init__(self, base_type, f):
        super(TypeValidator, self).__init__()
        self.base_type = base_type
        self.f = f

    def validate(self, value, **kwargs):
        if value is None:
            return value
        return getattr(self, 'f')(value, **kwargs)


def type_validator(name, base_type=None, default=False, **kwargs):
    if not base_type:
        base_type = name

    def wrap(fn):
        def wrapped(s, **immediate_kwargs):
            return fn(s, **dict(kwargs, **immediate_kwargs))
        o = TypeValidator(base_type, wrapped)
        TypeValidatorRegistry.register_validator(name, o, default=default)
        return fn

    return wrap


def isissue(o):
    return isinstance(o, Issue)


@type_validator('boolean')
def validate_boolean(s):
    if isinstance(s, bool):
        return s

    s = s.lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        return InvalidValueError('Value should be "true" or "false"')


@type_validator('enum')
def validate_enum(s, values=[]):
    if s in values:
        return None
    if len(values) == 0:
        message = 'There should be no value, but found %s' % repr(s)
    elif len(values) == 1:
        message = 'The only valid value is "%s", but found "%s"' % (
            repr(values[0]), repr(s))
    else:
        message = 'Valid values are %s and %s, but found %s' % (
            ', '.join([repr(v) for v in values[:-1]]),
            repr(values[-1]), repr(s))
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
        return InvalidValueError(
            'Host label should have at least one character')

    if not s[0].isalpha():
        return InvalidValueError(
            'Host label should start with a letter, but it starts with '
            '"%s"' % s[0])

    if len(s) == 1:
        return s

    if not (s[-1].isdigit() or s[-1].isalpha()):
        return InvalidValueError(
            'Host label should end with letter or digit, but it ends '
            'with "%s"' %
            s[-1], Mark('', 0, len(s) - 1))

    if len(s) == 2:
        return s

    for i, c in enumerate(s[1:-1]):
        if not (c.isalpha() or c.isdigit() or c == '-'):
            return InvalidValueError(
                'Host label should contain only letters, digits or hypens,'
                ' but it contains "%s"' %
                c, Mark('', 0, i + 1))

    return s


@type_validator('host', base_type='string')
@type_validator('host_address', base_type='string')
@type_validator('old_network', base_type='string')
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


@type_validator('network', base_type='string')
@type_validator('network_address', base_type='string')
def validate_network_address(s):
    return validate_ipv4_network(s)


@type_validator('network_mask', base_type='string')
def validate_network_mask(s):
    # TODO(someone): implement proper checking
    result = validate_ipv4_address(s)
    if isissue(result):
        return result

    parts = [int(p) for p in result.split('.', 3)]

    x = index(parts, lambda p: p != 255)
    if x == -1:
        return result

    if parts[x] not in [0, 128, 192, 224, 240, 248, 252, 254]:
        return InvalidValueError('Invalid netmask')

    x += 1
    while x < 4:
        if parts[x] != 0:
            return InvalidValueError('Invalid netmask')

    return result


@type_validator('host_and_port', base_type='string')
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


@type_validator('string', base_type='string', default=True)
@type_validator('list', base_type='list')
@type_validator('multi', base_type='multi')
@type_validator('file', base_type='string')
@type_validator('directory', base_type='string')
@type_validator('host_v6', base_type='string')
def validate_string(s):
    return s


@type_validator('regex', base_type='string')
@type_validator('regexp', base_type='string')
def validate_regex(s):
    try:
        re.compile(s)
    except re.error as e:
        return InvalidValueError(str(e))

    return s


@type_validator('integer')
def validate_integer(s, min=None, max=None):
    if isinstance(s, int):
        return s

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


@type_validator('file_mode')
def validate_file_mode(s):
    return validate_integer(s)


@type_validator('float')
def validate_float(s):
    if isinstance(s, float):
        return s

    # TODO(someone): Implement proper validation
    return float(s)


@type_validator('port', base_type='integer')
def validate_port(s, min=1, max=65535):
    return validate_integer(s, min=min, max=max)


def validate_list(s, element_type):
    if isinstance(s, list):
        return s

    element_type_validator = TypeValidatorRegistry.get_validator(element_type)
    if not element_type_validator:
        return SchemaIssue('Invalid element type "%s"' % element_type)

    result = []
    s = s.strip()

    if s == '':
        return result

    values = s.split(',')
    while len(values) > 0:
        value = values.pop(0)
        while True:
            validated_value = element_type_validator.validate(value.strip())
            if not isinstance(validated_value, Issue):
                break

            if len(values) == 0:
                # TODO(someone): provide better position reporting
                return validated_value

            value += ',' + values.pop()

        result.append(validated_value)

    return result


@type_validator('string_list', base_type='list')
def validate_string_list(s):
    return validate_list(s, element_type='string')


@type_validator('string_dict', base_type='multi')
def validate_dict(s, element_type='string'):
    if isinstance(s, dict):
        return s

    element_type_validator = TypeValidatorRegistry.get_validator(element_type)
    if not element_type_validator:
        return SchemaIssue('Invalid element type "%s"' % element_type)

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
            # TODO(someone): provide better position reporting
            return InvalidValueError('Key name should not be empty')

        validated_value = element_type_validator.validate(value)
        if isinstance(validated_value, Issue):
            # TODO(someone): provide better position reporting
            return validated_value
        result[key] = validated_value
    return result


@type_validator('rabbitmq_bind', base_type='string')
def validate_rabbitmq_bind(s):
    m = re.match('\d+', s)
    if m:
        port = validate_port(s)
        if isinstance(port, Issue):
            return port

        return ('0.0.0.0', port)

    m = re.match('{\s*\"(.+)\"\s*,\s*(\d+)\s*}', s)
    if m:
        host = validate_host_address(m.group(1))
        port = validate_port(m.group(2))

        if isinstance(host, Issue):
            return host

        if isinstance(port, Issue):
            return port

        return (host, port)

    return SchemaIssue("Unrecognized bind format")


def validate_rabbitmq_list(s, element_type):
    if isinstance(s, list):
        return s

    if not (s.startswith('[') and s.endswith(']')):
        return SchemaIssue('List should be surrounded by [ and ]')

    return validate_list(s[1:-1], element_type=element_type)


@type_validator('rabbitmq_bind_list', base_type='list')
def validate_rabbitmq_bind_list(s):
    return validate_rabbitmq_list(s, element_type='rabbitmq_bind')
