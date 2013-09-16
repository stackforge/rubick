from common import Error, MarkedError, Mark
from model import *

import unittest

from ostack_validator.common import Inspection
from ostack_validator.schema import ConfigSchemaRegistry

class MainConfigValidationInspection(Inspection):
  def inspect(self, openstack):
    results = []
    for host in openstack.hosts:
      for component in host.components:
        main_config = component.get_config()

        if not main_config:
          results.append(Error('Missing main configuration file for component "%s" at host "%s"' % (component.name, host.name)))
          continue

        schema = ConfigSchemaRegistry.get_schema(component.name, component.version, main_config.name)
        if not schema: continue

        for parameter in main_config.parameters:
          parameter_schema = schema.get_parameter(name=parameter.name, section=parameter.section)
          # TBD: should we report unknown config parameters?
          if not parameter_schema: continue

          type_descriptor = TypeDescriptorRepository.get_type(parameter_schema.type)
          type_validation_result = type_descriptor.validate(parameter.value)
          if type_validation_result:
            results.append(type_validation_result)

    return results

if __name__ == '__main__':
  unittest.main()

