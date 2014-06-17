# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
from six.moves.urllib.parse import urlparse

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
