package 'redis-server'
package 'python-pip'

bash 'Install python dependencies' do
  code 'pip install -r requirements.txt'
  cwd '/vagrant'
end

