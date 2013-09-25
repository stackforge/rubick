webui: gunicorn --error-logfile - --log-level info ostack_validator.webui:app
redis: redis-server
worker: celery worker --app=ostack_validator.celery:app

