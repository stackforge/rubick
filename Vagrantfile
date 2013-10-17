# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "web" do |web|
    web.vm.box = "ubuntu12.04-server-amd64"
    web.vm.box_url = "http://goo.gl/8kWkm"
    web.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: '0.0.0.0'
    web.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
        vb.customize ["modifyvm", :id, "--cpus", "1"]
    end
    web.vm.provision :chef_solo do |chef|
      chef.log_level = :debug
      chef.cookbooks_path = ["vagrant/cookbooks"]
      chef.add_recipe "openstack-validator"
    end
  end

end
