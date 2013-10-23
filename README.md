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

Deployment
-------------

### Development environment in vbox via vagrant
1. Install vagrant(MacOS, Windows, Ubuntu) - http://downloads.vagrantup.com/tags/v1.3.3
2. ./run_vagrant_provision.sh
3. After that you can access application on http://<host_machine_ip>:8000/

### Heroku deployment
1. This steps is already depricated, because of mongo-db usage in application. But if you really want to deploy on Heroku - use their paid plugin MongoHQ.
2. $ git clone git@github.com:MirantisLabs/rubick.git
3. $ cd rubick
4. $ heroku git:remote -a <name_of_the_heroku_app>
5. $ git push heroku master
 
### Manual deployment 
1. Install python dependencies: $ pip install -r requirements.txt
2. Install system dependencies: mongodb-server, redis-server
3. To run webui: $ PYTHONPATH=joker: python webui.py
4. To run main worker: $ PYTHONPATH=joker: celery worker --app=rubick.celery:app
5. All steps for manual deployment and running the app you can find here: ```/vagrant/cookbooks/openstack-validator/recipes/default.rb```

Hacking
-------

To check project on compliance to PEP8 run command use tox.
