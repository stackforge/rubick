import logging

from ostack_validator.common import Version
from ostack_validator.model import *
from ostack_validator.resource import ConfigSnapshotResourceLocator
from ostack_validator.config_formats import IniConfigParser

OPENSTACK_COMPONENTS = ['nova', 'keystone', 'glance']

class ModelParser(object):
  logger = logging.getLogger('ostack_validator.ModelParser')

  def parse(self, path):
    resource_locator = ConfigSnapshotResourceLocator(path)

    hosts = []
    for host_name in resource_locator.find_hosts():
      components = []
      for component_name in resource_locator.find_host_components(host_name):
        if not component_name in OPENSTACK_COMPONENTS:
          self.logger.warn('Unknown component in config: %s', component_name)
          continue

        component_version = Version(1000000) # very latest version
        version_resource = resource_locator.find_resource(host_name, component_name, 'version')
        if version_resource:
          component_version = Version(version_resource.get_contents())

        components.append(OpenstackComponent(component_name, component_version))

      hosts.append(Host(host_name, {}, components))

    return Openstack(hosts, resource_locator, IniConfigParser())

