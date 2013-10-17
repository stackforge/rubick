package 'redis-server'
package 'python-pip'

bash 'Install python dependencies' do
  code 'pip install -r requirements.txt'
  cwd '/vagrant'
end

bash 'Run application' do
  code 'killall /usr/bin/python'
  code 'echo "webui: gunicorn --error-logfile /tmp/webui.log --log-level debug ostack_validator.webui:app --bind 0.0.0.0:8000" > ProcfileHonchoLocal'
  code 'echo "worker: celery worker --app=ostack_validator.celery:app" >> ProcfileHonchoLocal'
  code 'honcho -f ProcfileHonchoLocal start &'
  cwd '/vagrant'
end

