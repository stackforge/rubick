import re
from StringIO import StringIO

from ostack_validator.model import *
from ostack_validator.config_formats.common import *

class IniConfigParser:
  key_value_re = re.compile('^\s*(\w+)\s*=\s*(.*)$')

  def parse(self, name, io):
    if not hasattr(io, 'readlines'):
      io = StringIO(io)

    errors = []
    current_section_name = ConfigSectionName(Mark(name, 1, 1), Mark(name, 1, 1), '')
    sections = []
    parameters = []

    line_number = 0
    for line in io.readlines():
      line_number += 1

      if line.strip() == '': continue

      start_index = 0
      while line[start_index].isspace(): start_index+=1

      if line[start_index] == '#': continue

      if line[start_index] == '[':
        end_index = line.find(']', start_index)
        if end_index == -1:
          errors.append(ParseError('Unclosed section', Mark(name, line_number, len(line))))

          end_index = len(line)
          while line[end_index-1].isspace(): end_index -= 1
          if end_index <= start_index+1:
            errors.append(ParseError('Missing section name', Mark(name, line_number, start_index)))
            continue
        else:
          i = end_index+1
          while i < len(line):
            if not line[i].isspace():
              errors.append(ParseError('Extra chars after section name', Mark(name, line_number, i)))
              break
            i += 1

        if current_section_name.text != '' or len(parameters) > 0:
          section = ConfigSection(current_section_name.start_mark, Mark(name, line_number, start_index), current_section_name, parameters)
          sections.append(section)
          parameters = []

        current_section_name = ConfigSectionName(
          Mark(name, line_number, start_index),
          Mark(name, line_number, end_index),
          line[start_index+1:end_index]
        )
      else:
        m = self.key_value_re.match(line)
        if m:
          param_name = ConfigParameterName(
            Mark(name, line_number, m.start(1)),
            Mark(name, line_number, m.end(1)),
            m.group(1)
          )
          param_value = ConfigParameterValue(
            Mark(name, line_number, m.start(2)),
            Mark(name, line_number, m.end(2)),
            m.group(2)
          )
          param = ConfigParameter(param_name.start_mark, param_value.end_mark, param_name, param_value)
          parameters.append(param)
        else:
          errors.append(ParseError('Syntax error', Mark(name, line_number, 1)))

    if current_section_name.text != '' or len(parameters) > 0:
      section = ConfigSection(current_section_name.start_mark, Mark(name, line_number, start_index), current_section_name, parameters)
      sections.append(section)
      parameters = []

    if len(errors) > 0:
      return ParseResult(False, errors)
    
    if len(sections) > 0:
      config = ComponentConfig(name, sections)
    else:
      config = ComponentConfig(name, [])

    return ParseResult(True, config)

