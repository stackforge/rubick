import logging
from itertools import groupby

from ostack_validator.common import Error, Mark, Issue, MarkedIssue, Inspection
from ostack_validator.schema import ConfigSchemaRegistry, TypeValidatorRegistry
import ostack_validator.schemas

class MainConfigValidationInspection(Inspection):
  logger = logging.getLogger('ostack_validator.inspections.main_config_validation')

  def inspect(self, openstack):
    results = []
    for host in openstack.hosts:
      for component in host.components:
        main_config = component.get_config()

        if not main_config:
          schema.logger.debug('No main config for component "%s"' % (component.name))
          results.append(Error('Missing main configuration file for component "%s" at host "%s"' % (component.name, host.name)))
          continue

        results.extend(main_config.errors)

        schema = ConfigSchemaRegistry.get_schema(component.name, component.version, main_config.name)
        if not schema:
          self.logger.debug('No schema for component "%s" main config version %s. Skipping it' % (component.name, component.version))
          continue

        section_name_text_f = lambda s: s.name.text
        sections_by_name = groupby(sorted(main_config.sections, key=section_name_text_f), key=section_name_text_f)

        for section_name, sections in sections_by_name:
          sections = list(sections)

          if len(sections) > 1:
            results.append(Issue(Issue.INFO, 'Section "%s" appears multiple times' % section_name))

          seen_parameters = set()

          for section in sections:
            for parameter in section.parameters:
              parameter_schema = schema.get_parameter(name=parameter.name.text, section=section.name.text)
              if not parameter_schema:
                results.append(MarkedIssue(Issue.WARNING, 'Unknown parameter "%s"' % parameter.name.text, parameter.start_mark))
                continue

              if parameter.name.text in seen_parameters:
                results.append(MarkedIssue(Issue.WARNING, 'Parameter "%s" in section "%s" redeclared' % (parameter.name.text, section_name), parameter.start_mark))
              else:
                seen_parameters.add(parameter.name.text)

              type_validator = TypeValidatorRegistry.get_validator(parameter_schema.type)
              type_validation_result = type_validator.validate(parameter.value.text)
              if isinstance(type_validation_result, Issue):
                self.logger.debug('Got issue for parameter "%s" with value "%s"' % (parameter.name.text, parameter.value.text))
                type_validation_result.mark = parameter.value.start_mark.merge(type_validation_result.mark)
                results.append(type_validation_result)

              else:
                value = type_validation_result
                if value == parameter_schema.default:
                  results.append(MarkedIssue(Issue.INFO, 'Parameter "%s" value equals default' % parameter.name.text, parameter.start_mark))

    return results

if __name__ == '__main__':
  unittest.main()

