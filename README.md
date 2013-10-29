Rubick
==========================

Thoughts
--------

Openstack consists of multiple projects each with it's own configuration schema.
Each project consists of multiple executables, each of which can have their custom config values in addition to project config.

Config file consists of groups, groups consist of parameters, parameter is key-value pair.

Schema inspections:
* Ensure that all present parameters belong to correct section (group) and have proper values (according to parameter's type).
* Ensure that all required parameters are present.
* Warn if some parameter is present multiple times.
* Warn if there are extra (unknown) parameters.
* Info if parameter's value equals to default value.

Config parameters can reference additional files, which can have their own syntax and schema. E.g. logging.conf, api-paste config. Those files require a separate inspections procedures.

Some configuration parameters reference Python classes, so in order to validate that it is required to know versions of all components and have list of all classes in them with information about component versions when this class first appeared and when it disappears.

Config schema
-------------
Each configuration option should have information on versions. When validating schema, the most recent config option record should be used for schema validation.

Changes in schema can be small between build (maintanence) releases, so there is no need to store whole schema for those. It should be stored in a diff-like format: for each known version there should be records on configuration changes like added/changed option, removed option. To validate configuration for paritcular version a configuration schema snapshot for that version will need to be calculated. Major (and maybe minor) versions can have the whole schema to speed up schema snapshot calculus.

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
