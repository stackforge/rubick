import logging

from ostack_validator.common import Error, Mark, Issue, Inspection
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

        schema = ConfigSchemaRegistry.get_schema(component.name, component.version, main_config.name)
        if not schema:
          self.logger.debug('No schema for component "%s" main config version %s. Skipping it' % (component.name, component.version))
          continue

        for section in main_config.sections:
          for parameter in section.parameters:
            parameter_schema = schema.get_parameter(name=parameter.name.text, section=section.name.text)
            # TBD: should we report unknown config parameters?
            if not parameter_schema:
              self.logger.debug('No schema for parameter "%s" in section "%s". Skipping it' % (parameter.name.text, section.name.text))
              continue

            type_validator = TypeValidatorRegistry.get_validator(parameter_schema.type)
            type_validation_result = type_validator.validate(parameter.value.text)
            if isinstance(type_validation_result, Issue):
              self.logger.debug('Got issue for parameter "%s" with value "%s"' % (parameter.name.text, parameter.value.text))
              type_validation_result.mark = main_config.mark.merge(parameter.value.start_mark.merge(type_validation_result.mark))
              results.append(type_validation_result)

    return results

if __name__ == '__main__':
  unittest.main()

