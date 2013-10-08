# -*- mode: ruby -*-
# vi: set ft=ruby :
#require 'vagrant-ansible'
#Vagrant::Config.run do |config|
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo 'Hello, lets start deployment.'"

  config.vm.define "web" do |web|
    web.vm.box = "ubuntu12.04-server-amd64"
    web.vm.box_url = "http://goo.gl/8kWkm"
    web.vm.network "forwarded_port", guest: 8000, host: 8000
    web.vm.network "forwarded_port", guest: 5000, host: 5000
    web.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = ["vagrant/cookbooks"]
      chef.add_recipe "openstack-validator"
    end
  end

#  config.vm.define "dev" do |dev|
#    dev.vm.box = "precise64"
#    dev.vm.box_url = "http://files.vagrantup.com/precise64.box"
##    dev.vm.network "forwarded_port", guest: 22, host: 2022
#    dev.vm.network :private_network, ip: "192.168.27.100"
#    dev.vm.network :private_network, ip: "172.24.4.225", :netmask => "255.255.255.224", :auto_config => false
#    dev.vm.provider "virtualbox" do |vb|
#      vb.customize ["modifyvm", :id, "--memory", "2048"]
#      vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
#    end
#    dev.vm.provision "ansible" do |ansible|
#      ansible.playbook = "devstack.yaml"
#      ansible.verbose = "v"
#    end
#    dev.vm.provision :shell, :inline => "cd devstack; sudo -u vagrant env HOME=/home/vagrant ./stack.sh"
#    dev.vm.provision :shell, :inline => "ovs-vsctl add-port br-ex eth2"
##    dev.vm.provision :shell do |shell|
##      shell.inline = "apt-get update && apt-get -y install git vim-gtk libxml2-dev libxslt1-dev libpq-dev python-pip libsqlite3-dev && apt-get -y build-dep python-mysqldb && pip install git-review tox && git clone git://git.openstack.org/openstack-dev/devstack && chown -R vagrant:vagrant devstack && cd devstack && tools/create-stack-user.sh && ./stack.sh"
##    end
#  end
end
