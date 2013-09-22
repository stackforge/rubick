import logging

from ostack_validator.common import Version
from ostack_validator.model import *
from ostack_validator.resource import Resource, ConfigSnapshotResourceLocator
from ostack_validator.config_formats import IniConfigParser

OPENSTACK_COMPONENTS = ['nova', 'keystone', 'glance', 'cinder', 'horizon', 'quantum', 'swift']

class ModelParser(object):
  logger = logging.getLogger('ostack_validator.ModelParser')

  def parse(self, path):
    resource_locator = ConfigSnapshotResourceLocator(path)

    hosts = []
    for host in resource_locator.find_resource(Resource.HOST):
      components = []
      for service in host.find_resource(Resource.SERVICE):
        if not service.name in OPENSTACK_COMPONENTS:
          continue

        components.append(OpenstackComponent(service.name, service.version))

      hosts.append(Host(host.name, {}, components))

    return Openstack(hosts, resource_locator, IniConfigParser())

