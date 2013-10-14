from urlparse import urlparse

from ostack_validator.common import Inspection, Issue, find

class KeystoneEndpointsInspection(Inspection):
  name = 'Keystone endpoints'
  description = 'Validate that each keystone endpoint leads to proper service'

  def inspect(self, openstack):
    keystone = find(openstack.components, lambda c: c.name == 'keystone')
    if not keystone:
      return

    for service in keystone.db['services']:
      if service['type'] == 'compute':
        endpoint = find(keystone.db['endpoints'], lambda e: e['service_id'] == service['id'])
        if not endpoint:
          keystone.report_issue(Issue(Issue.WARNING, 'Keystone catalog contains service "%s" that has no defined endpoints' % service['name']))
          continue

        for url_attr in ['adminurl', 'publicurl', 'internalurl']:
          url = urlparse(endpoint[url_attr])

          # TODO: resolve endpoint url host address
          host = find(openstack.hosts, lambda h: url.hostname in h.network_addresses)
          if not host:
            keystone.report_issue(Issue(Issue.ERROR, 'Keystone catalog has endpoint for service "%s" (id %s) that has "%s" set pointing to unknown host' % (service['name'], service['id'], url_attr)))
            continue

          nova_compute = None
          for c in host.components:
            if c.name != 'nova-compute': continue

            if c.config['osapi_compute_listen'] in ['0.0.0.0', url.hostname] and c.config['osapi_compute_listen_port'] == url.port:
              nova_compute = c
              break

          if not nova_compute:
            keystone.report_issue(Issue(Issue.ERROR, 'Keystone catalog has endpoint for service "%s" (id %s) that has "%s" set pointing to no service' % (service['name'], service['id'], url_attr)))


