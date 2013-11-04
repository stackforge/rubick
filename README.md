Rubick
==========================

Rubick is a tool to analyze OpenStack installation for possible problems. It consists of two processes:
1. Discovery - find all OpenStack components and collect information about them.
2. Analyze - perform various checks of discovered data to ensure consistency and conformance to best practices.

Installation
-------------

### Completely environment in VirtualBox via Vagrant
1. Install vagrant(MacOS, Windows, Ubuntu) - http://downloads.vagrantup.com/tags/v1.3.3 and latest version of Virtualbox
2. ```$ vagrant up && vagrant provision```
3. After that you can access application on http://host_machine_ip:8000/
4. For testing purposes of your application you can install latest-devstack installation via vagrant. We strongly recommend you to use this repo: https://github.com/lorin/devstack-vm. There are a lot of choices for devstack installation for Rubick to validate: with or without neutron\swift\security_groups\tempest etc.
5. After that you’ll get full worked environment with Rubick and OpenStack.

### Manual installation and running

```shell
$ sudo apt-get install build-essential mongodb-server redis-server python-pip
$ sudo pip install -r requirements.txt
$ python webui.py &
$ celery worker --app=rubick.celery:app &
```
All steps for manual deployment and running the app you can find here: /vagrant/cookbooks/openstack-validator/recipes/default.rb

Rubick usage
-------------

Open http://host_machine_ip:8000/ with web-browser, host_machine_ip - address  your application is installed.
Add new cluster by pushing the button “Add cluster” and fill the fields:

1. “Cluster name” - with name of your cluster (e.g. local_devstack )
2. “Description” - with description (e.g. VBox installation of devstack)
3. “Ip Address“ - with username@host:port (e.g. vagrant@192.168.27.100)
4. “SSH key“ - with ssh-key to access the virual machine (e.g. can be find in the directory ~/.vagrant.d/insecure_private_key for Vagrant nodes)
5. Press “Create”
 
After that you can select your cluster to run validations or select the rulest before validation.

Hacking
-------

To check project on compliance to PEP8 run command use: tox -v.
