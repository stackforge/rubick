from __future__ import absolute_import
import logging
import os
import traceback

from celery import Celery

from rubick.common import Issue, Inspection
from rubick.discovery import OpenstackDiscovery
import rubick.inspections
# Silence PEP8 "unused import"
assert rubick.inspections

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
backend_url = os.getenv('CELERY_RESULT_BACKEND', broker_url)

app = Celery('rubick', broker=broker_url, backend=backend_url)
app.conf.update(
    CELERY_TRACK_STARTED=True
)


class InspectionRequest(object):

    def __init__(self, nodes, username, password=None, private_key=None):
        super(InspectionRequest, self).__init__()
        self.nodes = nodes
        self.username = username
        self.password = password
        self.private_key = private_key


class InspectionResult(object):

    def __init__(self, request, value):
        super(InspectionResult, self).__init__()
        self.request = request
        self.value = value


@app.task(max_retries=0)
def ostack_inspect_task(request):
    logger = logging.getLogger('rubick.task.inspect')

    discovery = OpenstackDiscovery()

    try:
        openstack = discovery.discover(request.nodes, request.username,
                                       private_key=request.private_key)
    except:
        message = traceback.format_exc()
        logger.error(message)
        return InspectionResult(request, message)

    all_inspections = Inspection.all_inspections()
    for inspection in all_inspections:
        try:
            x = inspection()
            x.inspect(openstack)
        except:
            message = traceback.format_exc()
            logger.error(message)
            openstack.report_issue(
                Issue(
                    Issue.ERROR,
                    'Unexpected error running inspection "%s". See log for '
                    'details' %
                    inspection.name))

    return InspectionResult(request, openstack)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('rubick').setLevel(logging.DEBUG)

    app.start()
