import string

from ostack_validator.common import Mark


class ConfigurationSection(object):

    def __init__(self, config, section):
        super(ConfigurationSection, self).__init__()
        self.config = config
        self.section = section

    def _combine_names(self, section, param):
        if section == 'DEFAULT':
            return param

        return '%s.%s' % (section, param)

    def get(self, name, *args, **kwargs):
        return (
            self.config.get(
                self._combine_names(
                    self.section,
                    name),
                *args,
                **kwargs)
        )

    def set(self, name, *args, **kwargs):
        self.config.set(
            self._combine_names(
                self.section,
                name),
            *args,
            **kwargs)

    def set_default(self, name, *args, **kwargs):
        self.config.set_default(
            self._combine_names(
                self.section,
                name),
            *args,
            **kwargs)

    def contains(self, name, *args, **kwargs):
        return (
            self.config.contains(
                self._combine_names(
                    self.section,
                    name),
                *args,
                **kwargs)
        )

    def is_default(self, name, *args, **kwargs):
        return (
            self.config.is_default(
                self._combine_names(
                    self.section,
                    name),
                *args,
                **kwargs)
        )

    def __getitem__(self, key):
        return self.config.get(self._combine_names(self.section, key))

    def __setitem__(self, key, value):
        return self.config.set(self._combine_names(self.section, key), value)

    def __contains__(self, key):
        return self.config.contains(self._combine_names(self.section, key))

    def keys(self):
        return self.config.keys(self.section)

    def items(self, *args, **kwargs):
        return self.config.items(self.section, *args, **kwargs)


class ConfigurationWrapper(object):

    def __init__(self, config, state):
        super(ConfigurationWrapper, self).__init__()
        self.config = config
        self.state = state

    def __getitem__(self, key):
        if key in self.state:
            return ''

        return self.config.get(key, _state=self.state)


class Configuration(object):

    def __init__(self):
        super(Configuration, self).__init__()
        self._defaults = dict()
        self._normal = dict()

    def _normalize_name(self, name):
        if name.find('.') == -1:
            section = 'DEFAULT'
        else:
            section, name = name.split('.', 1)

        return (section, name)

    def _combine_names(self, section, param):
        if section == 'DEFAULT':
            return param

        return '%s.%s' % (section, param)

    def get(self, name, default=None, raw=False, _state=[]):
        section, name = self._normalize_name(name)

        if section in self._normal and name in self._normal[section]:
            value = self._normal[section][name]
        elif section in self._defaults and name in self._defaults[section]:
            value = self._defaults[section][name]
        else:
            value = default

        if not isinstance(value, str):
            return value

        if raw:
            return value

        tmpl = string.Template(value)
        return (
            tmpl.safe_substitute(ConfigurationWrapper(self, _state + [name]))
        )

    def contains(self, name, ignoreDefault=False):
        section, name = self._normalize_name(name)

        if section in self._normal and name in self._normal[section]:
            return True

        if not ignoreDefault and section in self._defaults \
            and name in self._defaults[section]:
            return True

        return False

    def is_default(self, name):
        section, name = self._normalize_name(name)

        return (
            not (section in self._normal and name in self._normal[section])
            and (section in self._defaults and name in self._defaults[section])
        )

    def set_default(self, name, value):
        section, name = self._normalize_name(name)

        if not section in self._defaults:
            self._defaults[section] = dict()

        self._defaults[section][name] = value

    def set(self, name, value):
        section, name = self._normalize_name(name)

        if not section in self._normal:
            self._normal[section] = dict()

        self._normal[section][name] = value

    def section(self, section):
        return ConfigurationSection(self, section)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, section):
        return (section in self._defaults) or (section in self._normal)

    def keys(self, section=None):
        if section:
            names = set()
            if section in self._defaults:
                for param in self._defaults[section].keys():
                    names.add(param)
            if section in self._normal:
                for param in self._normal[section].keys():
                    names.add(param)

            return list(names)
        else:
            sections = set()
            for section in self._defaults.keys():
                sections.add(section)

            for section in self._normal.keys():
                sections.add(section)

            return list(sections)

    def items(self, section=None):
        if section:
            return (
                [(name, self.get(self._combine_names(section, name)))
                 for name in self.keys(section)]
            )
        else:
            return (
                [(name, ConfigurationSection(self, name))
                 for name in self.keys()]
            )


class Element(object):

    def __init__(self, start_mark, end_mark):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __eq__(self, other):
        return (
            (self.__class__ == other.__class__)
            and (self.start_mark == other.start_mark)
            and (self.end_mark == other.end_mark)
        )

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


class ConfigSectionName(TextElement):
    pass


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
        return (
            (self.name.text == other.name.text) and (
                self.value.text == other.value.text)
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            "<ConfigParameter %s=%s delimiter=%s>" % (
                self.name.text,
                self.value.text,
                self.delimiter.text)
        )


class ConfigParameterName(TextElement):
    pass


class ConfigParameterValue(TextElement):

    def __init__(self, start_mark, end_mark, text, value=None, quotechar=None):
        super(ConfigParameterValue, self).__init__(start_mark, end_mark, text)
        self.value = value
        self.quotechar = quotechar
