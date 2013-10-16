import string
from lettuce import *

from ostack_validator.common import Issue, Version, find
from ostack_validator.model import *

def get_variable(name):
  if not hasattr(world, 'variables'):
    return None

  return world.variables.get(name)

def set_variable(name, value):
  if not hasattr(world, 'variables'):
    world.variables = {}

  world.variables[name] = value

def subst(template):
  if not hasattr(world, 'variables'):
    return template

  tmpl = string.Template(template)
  return tmpl.safe_substitute(world.variables)

def stop():
  assert False, "stop"

@step(r'I use OpenStack (\w+)')
def use_openstack_version(step, version):
  version = Version(version)
  for component in [c for c in world.openstack.components if isinstance(c, OpenstackComponent)]:
    if not Version(component.version) >= version: stop()

@step(r'Nova has "(.+)" equal to "(.*)"')
def nova_has_property(step, name, value):
  name = subst(name)
  value = subst(value)

  for nova in [c for c in world.openstack.components if c.name.startswith('nova')]:
    if not nova.config[name] == value: stop()
    
@step(r'Keystone addresses are @(\w+)')
def keystone_addresses(self, variable):
  keystone = find(world.openstack.components, lambda c: c.name == 'keystone')

  if keystone.config['bind_host'] == '0.0.0.0':
    addresses = filter(lambda ip: not ip.startswith('127.'), keystone.host.network_addresses)
  else:
    addresses = [keystone.config['bind_host']]

  set_variable(variable, addresses)

@step(r'Nova should have "(.+)" in "(.*)"')
def nova_property_assertion(self, name, values):
  name = subst(name)
  values = subst(values)

  if not values:
    return

  for nova in [c for c in world.openstack.components if c.name.startswith('nova')]:
    nova_value = nova.config[name]

    if not (nova_value and nova_value in values):
      nova.report_issue(Issue(Issue.ERROR, 'Nova should have "%s" in %s' % (name, values)))

