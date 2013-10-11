
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

    for nova in [c for c in components if c.name == 'nova-api']:
      if nova.config['DEFAULT']['auth_strategy'] != 'keystone':
        continue

      (authtoken_section,_) = find(
        nova.paste_config.items(),
        lambda (name, values): name.startswith('filter:') and values.get('paste.filter_factory') == KEYSTONE_AUTHTOKEN_FILTER_FACTORY
      )

      if not authtoken_section: continue

      authtoken_settings = nova.paste_config[authtoken_section]


      def get_value(name):
        return authtoken_settings[name] or nova.config['keystone_authtoken', name]

      auth_host = get_value('auth_host')
      auth_port = get_value('auth_port')
      auth_protocol = get_value('auth_protocol')
      admin_user = get_value('admin_user')
      admin_password = get_value('admin_password')
      admin_tenant_name = get_value('admin_tenant_name')
      admin_token = get_value('admin_token')

      msg_prefix = 'Service "%s" on host "%s"' % (nova.name, nova.host.name)

      if not auth_host:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' miss "auth_host" setting in keystone authtoken config'))
      elif not auth_host in keystone_addresses:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' has incorrect "auth_host" setting in keystone authtoken config'))

      if not auth_port:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' miss "auth_port" setting in keystone authtoken config'))
      elif auth_port != keystone.config['DEFAULT']['admin_port']:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' has incorrect "auth_port" setting in keystone authtoken config'))

      if not auth_protocol:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' miss "auth_protocol" setting in keystone authtoken config'))
      elif not auth_protocol in ['http', 'https']:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' has incorrect "auth_protocol" setting in keystone authtoken config'))

      if not admin_user:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' miss "admin_user" setting in keystone authtoken config'))
      else:
        user = find(keystone.db['users'], lambda u: u['name'] == admin_user)
        if not user:
          nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' has "admin_user" that is missing in Keystone catalog'))

      if not admin_tenant_name:
        nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' miss "admin_tenant_name" setting in keystone authtoken config'))
      else:
        tenant = find(keystone.db['tenants'], lambda t: t['name'] == admin_tenant_name)
        if not tenant:
          nova.report_issue(Issue(Issue.ERROR, msg_prefix + ' has "admin_tenant_name" that is missing in Keystone catalog'))

      if admin_token:
        nova.report_issue(Issue(Issue.WARNING, msg_prefix + ' uses insecure admin_token for authentication'))

