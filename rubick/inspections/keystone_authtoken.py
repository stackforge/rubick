
from rubick.common import Inspection, Issue, find

AUTHTOKEN_FILTER_FACTORY = ('keystoneclient.middleware.auth_token:'
                            'filter_factory')


class KeystoneAuthtokenSettingsInspection(Inspection):
    name = 'Keystone auth'
    description = 'Validate correctness of keystone settings'

    def inspect(self, openstack):
        components = []
        for host in openstack.hosts:
            components.extend(host.components)

        keystones = [c for c in components if c.name == 'keystone']
        if len(keystones) == 0:
            openstack.report_issue(
                Issue(Issue.FATAL, 'No keystone service found'))
            return

        keystone = keystones[0]
        keystone_addresses = [keystone.config['bind_host']]
        if keystone_addresses == ['0.0.0.0']:
            keystone_addresses = keystone.host.network_addresses

        for nova in [c for c in components if c.name == 'nova-api']:
            if nova.config['auth_strategy'] != 'keystone':
                continue

            (authtoken_section, _) = find(
                nova.paste_config.items(),
                lambda name_values: name_values[0].startswith('filter:') and
                name_values[1].get(
                    'paste.filter_factory') == AUTHTOKEN_FILTER_FACTORY
            )

            if not authtoken_section:
                continue

            authtoken_settings = nova.paste_config.section(authtoken_section)

            def get_value(name):
                return (
                    authtoken_settings[
                        name] or nova.config[
                        'keystone_authtoken.%s' %
                        name]
                )

            auth_host = get_value('auth_host')
            auth_port = get_value('auth_port')
            auth_protocol = get_value('auth_protocol')
            admin_user = get_value('admin_user')
            # admin_password = get_value('admin_password')
            admin_tenant_name = get_value('admin_tenant_name')
            admin_token = get_value('admin_token')

            msg = 'Keystone authtoken config %s'

            def missing_param_issue(param):
                return Issue(Issue.ERROR,
                             msg % (' miss "%s" setting' % param))

            def incorrect_param_issue(param):
                return Issue(Issue.ERROR,
                             msg % (' has incorrect "%s" setting' % param))

            if not auth_host:
                nova.report_issue(missing_param_issue('auth_host'))
            elif not auth_host in keystone_addresses:
                nova.report_issue(incorrect_param_issue('auth_host'))

            if not auth_port:
                nova.report_issue(missing_param_issue('auth_port'))
            elif auth_port != keystone.config['admin_port']:
                nova.report_issue(incorrect_param_issue('auth_port'))

            if not auth_protocol:
                nova.report_issue(missing_param_issue('auth_protocol'))
            elif not auth_protocol in ['http', 'https']:
                nova.report_issue(incorrect_param_issue('auth_protocol'))

            if not admin_user:
                nova.report_issue(missing_param_issue('admin_user'))
            else:
                user = find(
                    keystone.db['users'],
                    lambda u: u['name'] == admin_user)
                if not user:
                    nova.report_issue(
                        Issue(Issue.ERROR, msg %
                              ' has "admin_user" that is missing'))

            if not admin_tenant_name:
                nova.report_issue(missing_param_issue('admin_tenant_name'))
            else:
                tenant = find(keystone.db['tenants'],
                              lambda t: t['name'] == admin_tenant_name)
                if not tenant:
                    nova.report_issue(
                        Issue(Issue.ERROR, msg %
                              ' has "admin_tenant_name" that is missing'))

            if admin_token:
                nova.report_issue(
                    Issue(
                        Issue.WARNING,
                        msg % ' uses insecure admin_token method'
                        'for authentication'))
