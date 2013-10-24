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
    if ! tmux has-session -t dev; then
      tmux new-session -d -s dev "honcho start"
    fi
  EOS
  user 'vagrant'
  cwd '/vagrant'
end

