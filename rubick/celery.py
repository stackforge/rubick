from __future__ import absolute_import
import logging
import os
import traceback

from celery import Celery
from celery.utils.log import get_task_logger

from rubick.common import Issue, Inspection
from rubick.database import get_db, ObjectId, Cluster
from rubick.discovery import OpenstackDiscovery
import rubick.inspections
# Silence PEP8 "unused import"
assert rubick.inspections
import rubick.schemas
assert rubick.schemas
from rubick.json import openstack_for_json

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
backend_url = os.getenv('CELERY_RESULT_BACKEND', broker_url)

app = Celery('rubick', broker=broker_url, backend=backend_url)
app.conf.update(
    CELERY_TRACK_STARTED=True
)

logger = get_task_logger(__name__)


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
def ostack_discover_task(cluster_id):
    db = get_db()
    cluster_doc = db['clusters'].find_one({'_id': ObjectId(cluster_id)})
    if not cluster_doc:
        logger.error('Cluster with ID=%s was not found' % cluster_id)
        return

    cluster = Cluster.from_doc(cluster_doc)

    logger.info('Starting OpenStack discovery for cluster "%s" (id=%s)' %
                (cluster.name, cluster.id))

    discovery = OpenstackDiscovery()

    openstack = None
    try:
        openstack = discovery.discover(cluster.nodes,
                                       cluster.private_key)
    except:
        message = traceback.format_exc()
        logger.error(message)

    logger.info('Finished OpenStack discovery for cluster "%s" (id=%s)' %
                (cluster.name, cluster.id))

    cluster.data = openstack_for_json(openstack)

    db['clusters'].save(cluster.as_doc())


@app.task(max_retries=0)
def ostack_inspect_task(request):
    logger.info('Starting OpenStack inspection')

    discovery = OpenstackDiscovery()

    try:
        openstack = discovery.discover(request.nodes,
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

    logger.info('Finished OpenStack inspection')

    return InspectionResult(request, openstack)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('rubick').setLevel(logging.DEBUG)

    app.start()
