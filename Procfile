webui: gunicorn --error-logfile - --log-level info ostack_validator.webui:app --bind 0.0.0.0:8000
worker: celery worker --app=ostack_validator.celery:app

