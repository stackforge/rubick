openstack-config-validator
==========================

Thoughts
--------

Openstack consists of multiple projects each with it's own configuration schema.
Each project consists of multiple executables, each of which can have their custom config values in addition to project config.

Config file consists of groups, groups consist of parameters, parameter is key-value pair.

Schema checks:
* Ensure that all present parameters belong to correct section (group) and have proper values (according to parameter's type).
* Ensure that all required parameters are present.
* Warn if some parameter is present multiple times.
* Warn if there are extra (unknown) parameters.
* Info if parameter's value equals to default value.

Config parameters can reference additional files, which can have their own syntax and schema. E.g. logging.conf, api-paste config. Those files require a separate inspections procedures.

Some configuration parameters reference Python classes, so in order to validate that it is required to know versions of all components and have list of all classes in them with information about component versions when this class first appeared and when it disappears. The same applies to schema: each configuration option should have information on versions and when validating schema the most recent config option record should be used for schema validation.

Changes in schema can be small between build (maintanence) releases, so there is no need to store whole schema for those. It should be stored in a diff-like format: for each known version there should be records on configuration changes like added/changed option, removed option. To validate configuration for paritcular version a configuration schema snapshot for that version will need to be calculated. Major (and maybe minor) versions can have the whole schema to speed up schema snapshot calculus.

