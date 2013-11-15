from urlparse import urlparse

from rubick.common import Inspection, Issue, find

SERVICE_WITH_NO_ENDPOINT_MSG = """
Keystone catalog contains service "%s" that has no defined endpoints
""".strip()
SERVICE_ENDPOINT_MSG = """
Keystone catalog has endpoint for service "%s" (id %s) that has "%s"
""".strip()
UNKNOWN_HOST_ENDPOINT_MSG = (SERVICE_ENDPOINT_MSG +
                             ' set pointing to unknown host')
UNKNOWN_SERVICE_ENDPOINT_MSG = (SERVICE_ENDPOINT_MSG +
                                ' set pointing to no service')


class KeystoneEndpointsInspection(Inspection):
    name = 'Keystone endpoints'
    description = """
        Validate that each keystone endpoint leads to proper service
    """.strip()

    def inspect(self, openstack):
        keystone = find(openstack.components, lambda c: c.name == 'keystone')
        if not keystone:
            return

        for service in keystone.db['services']:
            if service['type'] == 'compute':
                endpoint = find(
                    keystone.db['endpoints'],
                    lambda e: e['service_id'] == service['id'])
                if not endpoint:
                    keystone.report_issue(
                        Issue(
                            Issue.WARNING, SERVICE_WITH_NO_ENDPOINT_MSG %
                            service['name']))
                    continue

                for url_attr in ['adminurl', 'publicurl', 'internalurl']:
                    url = urlparse(endpoint[url_attr])

                    # TODO(someone): resolve endpoint url host address
                    host = find(
                        openstack.hosts,
                        lambda h: url.hostname in h.network_addresses)
                    if not host:
                        keystone.report_issue(
                            Issue(Issue.ERROR, UNKNOWN_HOST_ENDPOINT_MSG %
                                  (service['name'], service['id'], url_attr)))
                        continue

                    nova_api = None
                    for c in host.components:
                        if c.name != 'nova-api':
                            continue

                        listen_address = c.config['osapi_compute_listen']
                        listen_port = c.config['osapi_compute_listen_port']

                        if (listen_address in ['0.0.0.0', url.hostname] and
                                listen_port == url.port):
                            nova_api = c
                            break

                    if not nova_api:
                        keystone.report_issue(
                            Issue(Issue.ERROR, UNKNOWN_SERVICE_ENDPOINT_MSG %
                                  (service['name'], service['id'], url_attr)))
