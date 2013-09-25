from __future__ import absolute_import
import os
import time

from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
backend_url = os.getenv('CELERY_RESULT_BACKEND', broker_url)

app = Celery('ostack_validator', broker=broker_url, backend=backend_url)
app.conf.update(
  CELERY_TRACK_STARTED=True
)

@app.task
def ostack_inspect_task(nodes, username, password=None, private_key=None):
  time.sleep(10)
  return username[::-1]

if __name__ == '__main__':
  app.start()

