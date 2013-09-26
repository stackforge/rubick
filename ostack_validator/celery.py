from __future__ import absolute_import
import os
import time
import logging

from celery import Celery

from ostack_validator.common import Issue, MarkedIssue, Inspection
from ostack_validator.discovery import OpenstackDiscovery, OpenstackComponent
from ostack_validator.inspections import KeystoneAuthtokenSettingsInspection

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
backend_url = os.getenv('CELERY_RESULT_BACKEND', broker_url)

app = Celery('ostack_validator', broker=broker_url, backend=backend_url)
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
  def __init__(self, request, openstack):
    super(InspectionResult, self).__init__()
    self.request = request
    self.openstack = openstack

@app.task
def ostack_inspect_task(request):
  discovery = OpenstackDiscovery()

  openstack = discovery.discover(request.nodes, request.username, private_key=request.private_key)

  all_inspections = [KeystoneAuthtokenSettingsInspection]
  for inspection in all_inspections:
    x = inspection()
    x.inspect(openstack)

  # For dramatic effect! =)
  time.sleep(2)

  return InspectionResult(request, openstack)

if __name__ == '__main__':
  logging.basicConfig(level=logging.WARNING)
  logging.getLogger('ostack_validator').setLevel(logging.DEBUG)

  app.start()

