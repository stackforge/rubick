
from ostack_validator.common import Inspection, Issue, find

KEYSTONE_AUTHTOKEN_FILTER_FACTORY = 'keystoneclient.middleware.auth_token:filter_factory'

class KeystoneAuthtokenSettingsInspection(Inspection):
  name = 'Keystone auth'
  description = 'Validate correctness of keystone settings'

  def inspect(self, openstack):
    components = []
    for host in openstack.hosts:
      components.extend(host.components)

    keystones = [c for c in components if c.name == 'keystone']
    if len(keystones) == 0:
      openstack.report_issue(Issue(Issue.FATAL, 'No keystone service found'))
      return

    keystone = keystones[0]
    keystone_addresses = [keystone.config['DEFAULT']['bind_host']]
    if keystone_addresses == ['0.0.0.0']:
      keystone_addresses = keystone.host.network_addresses

    for nova in [c for c in components if c.name == 'nova-compute']:
      if nova.config['DEFAULT']['auth_strategy'] != 'keystone':
        continue

      (authtoken_section,_) = find(
        nova.paste_config.items(),
        lambda (name, values): name.startswith('filter:') and values.get('paste.filter_factory') == KEYSTONE_AUTHTOKEN_FILTER_FACTORY
      )

      if not authtoken_section: continue

      authtoken_settings = nova.paste_config[authtoken_section]
      if not 'auth_host' in authtoken_settings:
        openstack.report_issue(Issue(Issue.ERROR, 'Service "%s" on host "%s" miss "auth_host" setting in keystone authtoken config' % (nova.name, nova.host.name)))
      elif not authtoken_settings['auth_host'] in keystone_addresses:
        openstack.report_issue(Issue(Issue.ERROR, 'Service "%s" on host "%s" has incorrect "auth_host" setting in keystone authtoken config' % (nova.name, nova.host.name)))

      if not 'auth_port' in authtoken_settings:
        openstack.report_issue(Issue(Issue.ERROR, 'Service "%s" on host "%s" miss "auth_port" setting in keystone authtoken config' % (nova.name, nova.host.name)))
      elif authtoken_settings['auth_port'] != keystone.config['DEFAULT']['admin_port']:
        openstack.report_issue(Issue(Issue.ERROR, 'Service "%s" on host "%s" has incorrect "auth_port" setting in keystone authtoken config' % (nova.name, nova.host.name)))

