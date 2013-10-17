package 'build-essential'
package 'mongodb-server'
package 'redis-server'
package 'python-pip'
package 'tmux'

bash 'Install python dependencies' do
  code 'pip install -r requirements.txt'
  cwd '/vagrant'
end

bash 'Run application' do
  code <<-EOS
    echo "webui: python webui.py" > ProcfileHonchoLocal
    echo "worker: celery worker --app=ostack_validator.celery:app" >> ProcfileHonchoLocal
    if ! tmux has-session -t dev; then
      tmux new-session -d -s dev "honcho -f ProcfileHonchoLocal start"
    fi
  EOS
  user 'vagrant'
  cwd '/vagrant'
end

