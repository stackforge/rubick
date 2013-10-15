# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo 'Hello, lets start deployment.'"

  config.vm.define "web" do |web|
    web.vm.box = "ubuntu12.04-server-amd64"
    web.vm.box_url = "http://goo.gl/8kWkm"
    web.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: '0.0.0.0'
    web.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
        vb.customize ["modifyvm", :id, "--cpus", "1"]
    end
    web.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = ["vagrant/cookbooks"]
      chef.add_recipe "openstack-validator"
    end
  end

  config.vm.define "dev" do |dev|
    dev.vm.box = "precise64"
    dev.vm.box_url = "http://files.vagrantup.com/precise64.box"
    dev.vm.network "forwarded_port", guest: 22, host: 2202, host_ip: '0.0.0.0'
    dev.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: '0.0.0.0'
    dev.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: '0.0.0.0'
    dev.vm.network "forwarded_port", guest: 35357, host: 35357, host_ip: '0.0.0.0'
    dev.vm.network :private_network, ip: "192.168.26.100"
    dev.vm.network :private_network, ip: "172.24.4.225", :netmask => "255.255.255.224", :auto_config => false
    dev.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
    end
    dev.vm.provision "ansible" do |ansible|
      ansible.host_key_checking = false
      ansible.playbook = "devstack.yaml"
      ansible.verbose = "vv"
    end
    dev.vm.provision :shell, :inline => "cd devstack; sudo -u vagrant env HOME=/home/vagrant ./stack.sh"
    dev.vm.provision :shell, :inline => "ovs-vsctl add-port br-ex eth2"
  end

end
