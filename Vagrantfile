# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "ubuntu12.04-server-amd64"
  config.vm.box_url = "http://goo.gl/8kWkm"
  # config.vm.box_url = "http://domain.com/path/to/above.box"

  # config.vm.forward_port 80, 8080
  config.vm.forward_port 5000, 5000

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = ["vagrant/cookbooks"]
    chef.add_recipe "openstack-validator"
  end
end
