import re

from six import StringIO

from rubick.common import Mark
from rubick.config_model import ComponentConfig, ConfigSection, \
    ConfigSectionName, ConfigParameter, ConfigParameterName, \
    ConfigParameterValue, TextElement
from rubick.config_formats.common import ParseError


class IniConfigParser:
    key_value_re = re.compile("^(\S+?)\s*([:=])\s*('.*'|\".*\"|.*)\s*$")

    def parse(self, name, base_mark, io):
        if not hasattr(io, 'readlines'):
            io = StringIO(io)

        def mark(line, column=0):
            return base_mark.merge(Mark('', line, column))

        errors = []
        current_section_name = ConfigSectionName(mark(0), mark(0), '')
        current_param_name = None
        current_param_value = None
        current_param_delimiter = None
        sections = []
        parameters = []

        line_number = -1
        for line in io.readlines():
            line = line.rstrip()

            line_number += 1

            if current_param_name \
                and (current_param_value.quotechar
                     or (line == '' or not line[0].isspace())):
                param = ConfigParameter(
                    current_param_name.start_mark,
                    current_param_value.end_mark,
                    current_param_name,
                    current_param_value,
                    current_param_delimiter)
                parameters.append(param)

                current_param_name = None
                current_param_value = None
                current_param_delimiter = None

            if line == '':
                continue

            if line[0] in '#;':
                continue

            if line[0].isspace():
                if current_param_name:
                    current_param_value.end_mark = mark(line_number, len(line))
                    current_param_value.text += line.lstrip()
                    continue
                else:
                    errors.append(
                        ParseError('Unexpected multiline value continuation',
                                   mark(line_number)))
                    continue

            if line[0] == '[':
                end_index = line.find(']')
                if end_index == -1:
                    errors.append(
                        ParseError('Unclosed section', mark(line_number,
                                                            len(line))))

                    end_index = len(line)
                    while line[end_index - 1].isspace():
                        end_index -= 1
                    if end_index <= 1:
                        errors.append(
                            ParseError('Missing section name',
                                       mark(line_number)))
                        continue
                else:
                    i = end_index + 1
                    while i < len(line):
                        if not line[i].isspace():
                            errors.append(
                                ParseError('Extra chars after section name',
                                           mark(line_number, i)))
                            break
                        i += 1

                if current_section_name.text != '' or len(parameters) > 0:
                    section = ConfigSection(
                        current_section_name.start_mark,
                        mark(line_number),
                        current_section_name,
                        parameters)
                    sections.append(section)
                    parameters = []

                current_section_name = ConfigSectionName(
                    mark(line_number, 0),
                    mark(line_number, end_index),
                    line[1:end_index]
                )
            else:
                m = self.key_value_re.match(line)
                if m:
                    current_param_name = ConfigParameterName(
                        mark(line_number, m.start(1)),
                        mark(line_number, m.end(1)),
                        m.group(1)
                    )
                    current_param_delimiter = TextElement(
                        mark(line_number, m.start(2)),
                        mark(line_number, m.end(2)),
                        m.group(2)
                    )

                    # Unquote value
                    value = m.group(3)
                    quotechar = None
                    if len(value) > 0 and (value[0] == value[-1]
                                           and value[0] in "\"'"):
                        quotechar = value[0]
                        value = value[1:-1]

                    current_param_value = ConfigParameterValue(
                        mark(line_number, m.start(3)),
                        mark(line_number, m.end(3)),
                        value,
                        quotechar=quotechar
                    )
                else:
                    errors.append(
                        ParseError('Syntax error in line "%s"' %
                                   line, mark(line_number)))

        if current_param_name:
            param = ConfigParameter(
                current_param_name.start_mark,
                current_param_value.end_mark,
                current_param_name,
                current_param_value,
                current_param_delimiter)
            parameters.append(param)

        if current_section_name.text != '' or len(parameters) > 0:
            section = ConfigSection(
                current_section_name.start_mark,
                mark(line_number),
                current_section_name,
                parameters)
            sections.append(section)
            parameters = []

        end_mark = base_mark
        if len(sections) > 0:
            end_mark = base_mark.merge(sections[-1].end_mark)

        config = ComponentConfig(base_mark, end_mark, name, sections, errors)

        return config
