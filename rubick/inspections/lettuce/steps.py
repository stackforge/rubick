import string
from lettuce import step, world

from rubick.common import Issue, Version, find
from rubick.model import *


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


# Openstack general step description section
@step(r'I use OpenStack (\w+)')
def use_openstack_version(step, version):
    version = Version(version)
    for component in [c for c in world.openstack.components
                      if isinstance(c, OpenstackComponent)]:
        if not Version(component.version) >= version:
            stop()


@step(r'Controller addresses are @(\w+)')
def controller_addresses(self, variable):
    controller = find(world.openstack.components, lambda c: c.name == 'nova')

    if controller.config['s3_host'] == '0.0.0.0':
        addresses = filter(
            lambda ip: not ip.startswith('127.'),
            controller.host.network_addresses)
    else:
        addresses = [controller.config['s3_host']]

    set_variable(variable, addresses)


# Keystone steps section
@step(r'Keystone addresses are @(\w+)')
def keystone_addresses(self, variable):
    keystone = find(world.openstack.components, lambda c: c.name == 'keystone')

    if keystone.config['bind_host'] == '0.0.0.0':
        addresses = filter(
            lambda ip: not ip.startswith('127.'),
            keystone.host.network_addresses)
    else:
        addresses = [keystone.config['bind_host']]

    set_variable(variable, addresses)


# Nova steps section
@step(r'Nova has "(.+)" equal to "(.*)"')
def nova_has_property(step, name, value):
    name = subst(name)
    value = subst(value)

    for nova in [c for c in world.openstack.components
                 if c.name.startswith('nova')]:
        if not nova.config[name] == value:
            stop()


@step(r'Nova should have "(.+)" in "(.*)"')
def nova_property_assertion(self, name, values):
    name = subst(name)
    values = subst(values)

    if not values:
        return

    for nova in [c for c in world.openstack.components
                 if c.name.startswith('nova')]:
        nova_value = nova.config[name]

        if not (nova_value and nova_value in values):
            nova.report_issue(
                Issue(Issue.ERROR, 'Nova should have "%s" in %s' %
                                   (name, values)))


@step(r"Nova should have keystone authtoken filter's \"(.+)\" in \"(.*)\"")
def nova_authtoken_property_assertion(self, name, values):
    name = subst(name)
    values = subst(values)

    if not values:
        return

    for nova in [c for c in world.openstack.components
                 if c.name.startswith('nova')]:

        (authtoken_section, _) = find(
            nova.paste_config.items(),
            lambda name_values: name_values[0].startswith('filter:')
            and name_values[1].get('paste.filter_factory') ==
            AUTHTOKEN_FILTER_FACTORY
        )

        if not authtoken_section:
            nova.report_issue(
                Issue(Issue.ERROR, 'Nova has keystone "auth" strategy '
                                   'configured, but doesnt have authtoken '
                                   'paste filter'))
            continue

        authtoken_settings = nova.paste_config.section(authtoken_section)

        param_value = (authtoken_settings[name] or
                       nova.config['keystone_authtoken.%s' % name])

        if not (param_value and param_value in values):
            nova.report_issue(
                Issue(Issue.ERROR, 'Nova should have "%s" in %s, '
                                   'actual value is "%s"' % (
                                       name, values, param_value)))


# Common steps section
@step(r'"(.+)" component must have "(.+)" parameter')
def component_has_non_none_property(step, component_name, parameter_name):
    component_name = subst(component_name)
    parameter_name = subst(parameter_name)

    for component in [c for c in world.openstack.components
                      if c.name.startswith('%s' % component_name)]:
        component_value = component.config[parameter_name]

        if component_value is None:
            component.report_issue(
                Issue(Issue.ERROR,
                      '"%s" must have parameter "%s - version %s"' %
                      (c.name, parameter_name, component.version)))


@step(r'"(.+)" component have "(.+)" parameter equal to "(.*)"')
def component_has_property_with_value(step, component_name, parameter_name,
                                      value):
    component_name = subst(component_name)
    parameter_name = subst(parameter_name)
    value = subst(value)

    for component in [c for c in world.openstack.components
                      if c.component.startswith('%s' % component_name)]:
        component_value = component.config[parameter_name]

        if not component_value == value:
            component.report_issue(
                Issue(Issue.ERROR,
                      '"%s" should have parameter "%s" equals "%s"'
                      'now its "%s"' % (component_name, parameter_name,
                                        component_value, value)))


@step(r'Which package version do I use?')
def component_versions_list(self):
    for component in world.openstack.components:
        component.report_issue(Issue(Issue.INFO, "%s component has % version" %
                                                 (component.name,
                                                  component.version)))
