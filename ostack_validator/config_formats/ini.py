import re
from StringIO import StringIO

from ostack_validator.model import *
from ostack_validator.config_formats.common import *

class IniConfigParser:
  key_value_re = re.compile("^(\w+)\s*([:=])\s*('.*'|\".*\"|.*)\s*$")

  def parse(self, name, io):
    if not hasattr(io, 'readlines'):
      io = StringIO(io)

    errors = []
    current_section_name = ConfigSectionName(Mark(name, 0, 0), Mark(name, 0, 0), '')
    current_param_name = None
    current_param_value = None
    current_param_delimiter = None
    sections = []
    parameters = []

    line_number = 0
    for line in io.readlines():
      line = line.rstrip()

      if current_param_name and (current_param_value.quotechar or (line == '' or not line[0].isspace())):
        param = ConfigParameter(current_param_name.start_mark, current_param_value.end_mark, current_param_name, current_param_value, current_param_delimiter)
        parameters.append(param)

        current_param_name = None
        current_param_value = None
        current_param_delimiter = None

      if line == '': continue

      if line[0] in '#;': continue

      if line[0].isspace():
        if current_param_name:
          current_param_value.end_mark = Mark(name, line_number, len(line))
          current_param_value.text += line.lstrip()
          continue
        else:
          errors.append(ParseError('Unexpected multiline value continuation', Mark(name, line_number, 0)))
          continue

      if line[0] == '[':
        end_index = line.find(']')
        if end_index == -1:
          errors.append(ParseError('Unclosed section', Mark(name, line_number, len(line))))

          end_index = len(line)
          while line[end_index-1].isspace(): end_index -= 1
          if end_index <= 1:
            errors.append(ParseError('Missing section name', Mark(name, line_number, 0)))
            continue
        else:
          i = end_index+1
          while i < len(line):
            if not line[i].isspace():
              errors.append(ParseError('Extra chars after section name', Mark(name, line_number, i)))
              break
            i += 1

        if current_section_name.text != '' or len(parameters) > 0:
          section = ConfigSection(current_section_name.start_mark, Mark(name, line_number, 0), current_section_name, parameters)
          sections.append(section)
          parameters = []

        current_section_name = ConfigSectionName(
          Mark(name, line_number, 0),
          Mark(name, line_number, end_index),
          line[1:end_index]
        )
      else:
        m = self.key_value_re.match(line)
        if m:
          current_param_name = ConfigParameterName(
            Mark(name, line_number, m.start(1)),
            Mark(name, line_number, m.end(1)),
            m.group(1)
          )
          current_param_delimiter = TextElement(
            Mark(name, line_number, m.start(2)),
            Mark(name, line_number, m.end(2)),
            m.group(2)
          )

          # Unquote value
          value = m.group(3)
          quotechar = None
          if (value[0] == value[-1] and value[0] in "\"'"):
            quotechar = value[0]
            value = value[1:-1]

          current_param_value = ConfigParameterValue(
            Mark(name, line_number, m.start(3)),
            Mark(name, line_number, m.end(3)),
            value,
            quotechar
          )
        else:
          errors.append(ParseError('Syntax error', Mark(name, line_number, 0)))

      line_number += 1

    if current_param_name:
      param = ConfigParameter(current_param_name.start_mark, current_param_value.end_mark, current_param_name, current_param_value, current_param_delimiter)
      parameters.append(param)

    if current_section_name.text != '' or len(parameters) > 0:
      section = ConfigSection(current_section_name.start_mark, Mark(name, line_number, 0), current_section_name, parameters)
      sections.append(section)
      parameters = []

    config = ComponentConfig(name, sections, errors)

    return config

