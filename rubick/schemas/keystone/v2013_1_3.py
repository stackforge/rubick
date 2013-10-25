from rubick.schema import ConfigSchemaRegistry

keystone = ConfigSchemaRegistry.register_schema(project='keystone')

with keystone.version('2013.1.3', checkpoint=True) as keystone_2013_1_3:

    keystone_2013_1_3.param(
        'admin_token',
        type='string',
        default='ADMIN',
        description="A 'shared secret' between keystone and other openstack "
                    "services")

    keystone_2013_1_3.param(
        'bind_host',
        type='host',
        default='0.0.0.0',
        description="The IP address of the network interface to listen on")

    keystone_2013_1_3.param(
        'public_port',
        type='port',
        default='5000',
        description="The port number which the public service listens on")

    keystone_2013_1_3.param(
        'admin_port',
        type='port',
        default='35357',
        description="The port number which the public admin listens on")

    keystone_2013_1_3.param(
        'public_endpoint',
        type='string',
        default='http://localhost:%(public_port)s/',
        description="The base endpoint URLs for keystone that are advertised to "
                    "clients (NOTE: this does NOT affect how keystone listens for "
                    "connections)")

    keystone_2013_1_3.param(
        'admin_endpoint',
        type='string',
        default='http://localhost:%(admin_port)s/',
        description="")

    keystone_2013_1_3.param(
        'compute_port',
        type='port',
        default='8774',
        description="The port number which the OpenStack Compute service "
                    "listens on")

    keystone_2013_1_3.param(
        'policy_file',
        type='string',
        default='policy.json',
        description="Path to your policy definition containing identity actions")

    keystone_2013_1_3.param(
        'policy_default_rule',
        type='string',
        default='admin_required',
        description="Rule to check if no matching policy definition is found "
                    "FIXME(dolph): This should really be defined as [policy] "
                    "default_rule")

    keystone_2013_1_3.param(
        'member_role_id',
        type='string',
        default='9fe2ff9ee4384b1894a90878d3e92bab',
        description="Role for migrating membership relationships During a SQL "
                    "upgrade, the following values will be used to create a new "
                    "role that will replace records in the user_tenant_membership "
                    "table with explicit role grants.  After migration, the "
                    "member_role_id will be used in the API add_user_to_project, "
                    "and member_role_name will be ignored.")

    keystone_2013_1_3.param(
        'member_role_name',
        type='string',
        default='_member_',
        description="")

    keystone_2013_1_3.param(
        'max_request_body_size',
        type='string',
        default='114688',
        description="enforced by optional sizelimit middleware "
                    "(keystone_2013_1_3.middleware:RequestBodySizeLimiter)")

    keystone_2013_1_3.param(
        'max_param_size',
        type='integer',
        default=64,
        description="limit the sizes of user & tenant ID/names")

    keystone_2013_1_3.param(
        'max_token_size',
        type='integer',
        default=8192,
        description="similar to max_param_size, but provides an exception for "
                    "token values")

    keystone_2013_1_3.param(
        'debug',
        type='boolean',
        default=False,
        description="=== Logging Options === Print debugging output (includes "
                    "plaintext request logging, potentially including passwords)")

    keystone_2013_1_3.param(
        'verbose',
        type='boolean',
        default=False,
        description="Print more verbose output")

    keystone_2013_1_3.param(
        'log_file',
        type='string',
        default='keystone_2013_1_3.log',
        description="Name of log file to output to. If not set, logging will go "
                    "to stdout.")

    keystone_2013_1_3.param(
        'log_dir',
        type='string',
        default='/var/log/keystone',
        description="The directory to keep log files in (will be prepended to "
                    "--logfile)")

    keystone_2013_1_3.param(
        'use_syslog',
        type='boolean',
        default=False,
        description="Use syslog for logging.")

    keystone_2013_1_3.param(
        'syslog_log_facility',
        type='string',
        default='LOG_USER',
        description="syslog facility to receive log lines")

    keystone_2013_1_3.param(
        'log_config',
        type='string',
        default='logging.conf',
        description="If this option is specified, the logging configuration file "
                    "specified is used and overrides any other logging options "
                    "specified. Please see the Python logging module documentation"
                    " for details on logging configuration files.")

    keystone_2013_1_3.param(
        'log_format',
        type='string',
        default='%(asctime)s %(levelname)8s [%(name)s] %(message)s',
        description="A logging.Formatter log message format string which may use "
                    "any of the available logging.LogRecord attributes.")

    keystone_2013_1_3.param(
        'log_date_format',
        type='string',
        default='%Y-%m-%d %H:%M:%S',
        description="Format string for %(asctime)s in log records.")

    keystone_2013_1_3.param(
        'onready',
        type='string',
        default='keystone_2013_1_3.common.systemd',
        description="onready allows you to send a notification when the process "
                    "is ready to serve For example, to have it notify using "
                    "systemd, one could set shell command: onready = "
                    "systemd-notify --ready or a module with notify() method:")

    keystone_2013_1_3.param(
        'default_notification_level',
        type='string',
        default='INFO',
        description="Default notification level for outgoing notifications")

    keystone_2013_1_3.param(
        'default_publisher_id',
        type='string',
        default='',
        description="Default publisher_id for outgoing notifications; included in "
                    "the payload.")

    keystone_2013_1_3.param(
        'rpc_backend',
        type='string',
        default='keystone_2013_1_3.openstack.common.rpc.impl_kombu',
        description="The messaging module to use, defaults to kombu.")

    keystone_2013_1_3.param(
        'rpc_thread_pool_size',
        type='integer',
        default=64,
        description="Size of RPC thread pool")

    keystone_2013_1_3.param(
        'rpc_conn_pool_size',
        type='integer',
        default=30,
        description="Size of RPC connection pool")

    keystone_2013_1_3.param(
        'rpc_response_timeout',
        type='integer',
        default=60,
        description="Seconds to wait for a response from call or multicall")

    keystone_2013_1_3.param(
        'rpc_cast_timeout',
        type='integer',
        default=30,
        description="Seconds to wait before a cast expires (TTL). Only supported "
                    "by impl_zmq.")

    keystone_2013_1_3.param(
        'fake_rabbit',
        type='boolean',
        default=False,
        description="If True, use a fake RabbitMQ provider")

    keystone_2013_1_3.param(
        'control_exchange',
        type='string',
        default='openstack',
        description="AMQP exchange to connect to if using RabbitMQ or Qpid")

    keystone_2013_1_3.section('sql')

    keystone_2013_1_3.param(
        'connection',
        type='string',
        default='sqlite:///keystone_2013_1_3.db',
        description="The SQLAlchemy connection string used to connect to the "
                    "database")

    keystone_2013_1_3.param(
        'idle_timeout',
        type='integer',
        default=200,
        description="the timeout before idle sql connections are reaped")

    keystone_2013_1_3.section('identity')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.identity.backends.sql.Identity',
        description="")

    keystone_2013_1_3.param(
        'default_domain_id',
        type='string',
        default='default',
        description="This references the domain to use for all Identity API v2 "
                    "requests (which are not aware of domains). A domain with "
                    "this ID will be created for you by keystone-manage db_sync "
                    "in migration 008.  The domain referenced by this ID cannot "
                    "be deleted on the v3 API, to prevent accidentally breaking "
                    "the v2 API. There is nothing special about this domain, "
                    "other than the fact that it must exist to order to "
                    "maintain support for your v2 clients.")

    keystone_2013_1_3.param(
        'domain_specific_drivers_enabled',
        type='boolean',
        default=False,
        description="A subset (or all) of domains can have their own identity "
                    "driver, each with their own partial configuration file in a "
                    "domain configuration directory. Only")

    keystone_2013_1_3.param(
        'domain_config_dir',
        type='string',
        default='/etc/keystone/domains',
        description="")

    keystone_2013_1_3.param(
        'max_password_length',
        type='integer',
        default=4096,
        description="Maximum supported length for user passwords; decrease to "
                    "improve performance.")

    keystone_2013_1_3.section('credential')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.credential.backends.sql.Credential',
        description="")

    keystone_2013_1_3.section('trust')

    keystone_2013_1_3.param(
        'enabled',
        type='boolean',
        default=True,
        description="delegation and impersonation features can be optionally "
                    "disabled")

    keystone_2013_1_3.section('os_inherit')

    keystone_2013_1_3.param(
        'enabled',
        type='boolean',
        default=False,
        description="role-assignment inheritance to projects from owning domain "
                    "can be optionally enabled")

    keystone_2013_1_3.section('catalog')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.catalog.backends.sql.Catalog',
        description="dynamic, sql-based backend (supports API/CLI-based "
                    "management commands)")

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.catalog.backends.templated.TemplatedCatalog',
        description="static, file-based backend (does *NOT* support any "
                    "management commands)")

    keystone_2013_1_3.param(
        'template_file',
        type='string',
        default='default_catalog.templates',
        description="")

    keystone_2013_1_3.section('endpoint_filter')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.contrib.endpoint_filter.backends.sql.EndpointFilter',
        description="extension for creating associations between project and "
                    "endpoints in order to provide a tailored catalog for "
                    "project-scoped token requests.")

    keystone_2013_1_3.param(
        'return_all_endpoints_if_no_filter',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.section('token')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.token.backends.sql.Token',
        description="Provides token persistence.")

    keystone_2013_1_3.param(
        'provider',
        type='string',
        default='',
        description="Controls the token construction, validation, and revocation "
                    "operations. Core providers are keystone_2013_1_3.token.providers."
                    "[pki|uuid].Provider")

    keystone_2013_1_3.param(
        'expiration',
        type='integer',
        default=86400,
        description="Amount of time a token should remain valid (in seconds)")

    keystone_2013_1_3.param(
        'bind',
        type='string',
        default='',
        description="External auth mechanisms that should add bind information to "
                    "token. eg kerberos, x509")

    keystone_2013_1_3.param(
        'enforce_token_bind',
        type='string',
        default='permissive',
        description="Enforcement policy on tokens presented to keystone with bind "
                    "information. One of disabled, permissive, strict, required "
                    "or a specifically required bind mode e.g. kerberos or x509 "
                    "to require binding to that authentication.")

    keystone_2013_1_3.param(
        'caching',
        type='boolean',
        default=True,
        description="Token specific caching toggle. This has no effect unless the "
                    "global caching option is set to True")

    keystone_2013_1_3.param(
        'cache_time',
        type='integer',
        default=0,
        description="Token specific cache time-to-live (TTL) in seconds.")

    keystone_2013_1_3.param(
        'revocation_cache_time',
        type='integer',
        default=3600,
        description="Revocation-List specific cache time-to-live (TTL) "
                    "in seconds.")

    keystone_2013_1_3.section('cache')

    keystone_2013_1_3.param(
        'enabled',
        type='boolean',
        default=False,
        description="Global cache functionality toggle.")

    keystone_2013_1_3.param(
        'config_prefix',
        type='string',
        default='cache.keystone',
        description="Prefix for building the configuration dictionary for the "
                    "cache region. This should not need to be changed unless there"
                    " is another dogpile.cache region with the same configuration "
                    "name")

    keystone_2013_1_3.param(
        'backend',
        type='string',
        default='keystone_2013_1_3.common.cache.noop',
        description="Dogpile.cache backend module. It is recommended that "
                    "Memcache (dogpile.cache.memcache) or Redis "
                    "(dogpile.cache.redis) be used in production deployments.  "
                    "Small workloads (single process) like devstack can use the "
                    "dogpile.cache.memory backend.")

    keystone_2013_1_3.param(
        'backend_argument',
        type='string',
        default='',
        description="Arguments supplied to the backend module. Specify this "
                    "option once per argument to be passed to the "
                    "dogpile.cache backend. Example format: <argname>:<value>")

    keystone_2013_1_3.param(
        'proxies',
        type='string',
        default='',
        description="Proxy Classes to import that will affect the way the "
                    "dogpile.cache backend functions.  See the dogpile.cache "
                    "documentation on changing-backend-behavior. Comma delimited "
                    "list e.g. my.dogpile.proxy.Class, my.dogpile.proxyClass2")

    keystone_2013_1_3.param(
        'use_key_mangler',
        type='boolean',
        default=True,
        description="Use a key-mangling function (sha1) to ensure fixed length "
                    "cache-keys. This is toggle-able for debugging purposes, "
                    "it is highly recommended to always leave this set to True.")

    keystone_2013_1_3.param(
        'debug_cache_backend',
        type='boolean',
        default=False,
        description="Extra debugging from the cache backend (cache keys, "
                    "get/set/delete/etc calls) This is only really useful if you "
                    "need to see the specific cache-backend get/set/delete calls "
                    "with the keys/values.  Typically this should be left set to "
                    "False.")

    keystone_2013_1_3.section('policy')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.policy.backends.sql.Policy',
        description="")

    keystone_2013_1_3.section('ec2')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.contrib.ec2.backends.kvs.Ec2',
        description="")

    keystone_2013_1_3.section('assignment')

    keystone_2013_1_3.param('driver', type='string', default='', description="")

    keystone_2013_1_3.param(
        'caching',
        type='boolean',
        default=True,
        description="Assignment specific caching toggle. This has no effect "
                    "unless the global caching option is set to True")

    keystone_2013_1_3.param(
        'cache_time',
        type='integer',
        default=0,
        description="Assignment specific cache time-to-live (TTL) in seconds.")

    keystone_2013_1_3.section('oauth1')

    keystone_2013_1_3.param(
        'driver',
        type='string',
        default='keystone_2013_1_3.contrib.oauth1.backends.sql.OAuth1',
        description="")

    keystone_2013_1_3.param(
        'request_token_duration',
        type='integer',
        default=28800,
        description="The Identity service may include expire attributes. If no "
                    "such attribute is included, then the token lasts "
                    "indefinitely. Specify how quickly the request token will "
                    "expire (in seconds)")

    keystone_2013_1_3.param(
        'access_token_duration',
        type='integer',
        default=86400,
        description="Specify how quickly the access token will expire "
                    "(in seconds)")

    keystone_2013_1_3.section('ssl')

    keystone_2013_1_3.param('enable', type='boolean', default=True, description="")

    keystone_2013_1_3.param(
        'certfile',
        type='string',
        default='/etc/keystone/pki/certs/ssl_cert.pem',
        description="")

    keystone_2013_1_3.param(
        'keyfile',
        type='string',
        default='/etc/keystone/pki/private/ssl_key.pem',
        description="")

    keystone_2013_1_3.param(
        'ca_certs',
        type='string',
        default='/etc/keystone/pki/certs/cacert.pem',
        description="")

    keystone_2013_1_3.param(
        'ca_key',
        type='string',
        default='/etc/keystone/pki/private/cakey.pem',
        description="")

    keystone_2013_1_3.param('key_size', type='integer', default=1024, description="")

    keystone_2013_1_3.param('valid_days', type='integer', default=3650, description="")

    keystone_2013_1_3.param('cert_required', type='boolean', default=False, description="")

    keystone_2013_1_3.param(
        'cert_subject',
        type='string',
        default='/CUS/STUnset/LUnset/OUnset/CNlocalhost',
        description="")

    keystone_2013_1_3.section('signing')

    keystone_2013_1_3.param(
        'token_format',
        type='string',
        default='',
        description="Deprecated in favor of provider in the [token] section "
                    "Allowed values are PKI or UUID")

    keystone_2013_1_3.param(
        'certfile',
        type='string',
        default='/etc/keystone/pki/certs/signing_cert.pem',
        description="")

    keystone_2013_1_3.param(
        'keyfile',
        type='string',
        default='/etc/keystone/pki/private/signing_key.pem',
        description="")

    keystone_2013_1_3.param(
        'ca_certs',
        type='string',
        default='/etc/keystone/pki/certs/cacert.pem',
        description="")

    keystone_2013_1_3.param(
        'ca_key',
        type='string',
        default='/etc/keystone/pki/private/cakey.pem',
        description="")

    keystone_2013_1_3.param('key_size', type='boolean', default=2048, description="")

    keystone_2013_1_3.param('valid_days', type='boolean', default=3650, description="")

    keystone_2013_1_3.param(
        'cert_subject',
        type='string',
        default='/CUS/STUnset/LUnset/OUnset/CNwww.example.com',
        description="")

    keystone_2013_1_3.section('ldap')

    keystone_2013_1_3.param(
        'url',
        type='string',
        default='ldap://localhost',
        description="")

    keystone_2013_1_3.param(
        'user',
        type='string',
        default='dcManager,dcexample,dccom',
        description="")

    keystone_2013_1_3.param('password', type='string', default=None, description="")

    keystone_2013_1_3.param(
        'suffix',
        type='string',
        default='cnexample,cncom',
        description="")

    keystone_2013_1_3.param(
        'use_dumb_member',
        type='boolean',
        default=False,
        description="")

    keystone_2013_1_3.param(
        'allow_subtree_delete',
        type='boolean',
        default=False,
        description="")

    keystone_2013_1_3.param(
        'dumb_member',
        type='string',
        default='cndumb,dcexample,dccom',
        description="")

    keystone_2013_1_3.param(
        'page_size',
        type='integer',
        default=0,
        description="Maximum results per page; a value of zero ('0') disables "
                    "paging (default)")

    keystone_2013_1_3.param(
        'alias_dereferencing',
        type='string',
        default='default',
        description="The LDAP dereferencing option for queries. This can be "
                    "either 'never', 'searching', 'always', 'finding' or "
                    "'default'. The 'default' option falls back to using "
                    "default dereferencing configured by your ldap.conf.")

    keystone_2013_1_3.param(
        'query_scope',
        type='string',
        default='one',
        description="The LDAP scope for queries, this can be either 'one' "
                    "(onelevel/singleLevel) or 'sub' (subtree/wholeSubtree)")

    keystone_2013_1_3.param(
        'user_tree_dn',
        type='string',
        default='ouUsers,dcexample,dccom',
        description="")

    keystone_2013_1_3.param('user_filter', type='string', default='', description="")

    keystone_2013_1_3.param(
        'user_objectclass',
        type='string',
        default='inetOrgPerson',
        description="")

    keystone_2013_1_3.param(
        'user_domain_id_attribute',
        type='string',
        default='businessCategory',
        description="")

    keystone_2013_1_3.param(
        'user_id_attribute',
        type='string',
        default='cn',
        description="")

    keystone_2013_1_3.param(
        'user_name_attribute',
        type='string',
        default='sn',
        description="")

    keystone_2013_1_3.param(
        'user_mail_attribute',
        type='string',
        default='email',
        description="")

    keystone_2013_1_3.param(
        'user_pass_attribute',
        type='string',
        default='userPassword',
        description="")

    keystone_2013_1_3.param(
        'user_enabled_attribute',
        type='string',
        default='enabled',
        description="")

    keystone_2013_1_3.param('user_enabled_mask', type='integer', default=0, description="")

    keystone_2013_1_3.param(
        'user_enabled_default',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'user_attribute_ignore',
        type='string',
        default='tenant_id,tenants',
        description="")

    keystone_2013_1_3.param(
        'user_allow_create',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'user_allow_update',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'user_allow_delete',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'user_enabled_emulation',
        type='boolean',
        default=False,
        description="")

    keystone_2013_1_3.param(
        'user_enabled_emulation_dn',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'tenant_tree_dn',
        type='string',
        default='ouProjects,dcexample,dccom',
        description="")

    keystone_2013_1_3.param('tenant_filter', type='string', default='', description="")

    keystone_2013_1_3.param(
        'tenant_objectclass',
        type='string',
        default='groupOfNames',
        description="")

    keystone_2013_1_3.param(
        'tenant_domain_id_attribute',
        type='string',
        default='businessCategory',
        description="")

    keystone_2013_1_3.param(
        'tenant_id_attribute',
        type='string',
        default='cn',
        description="")

    keystone_2013_1_3.param(
        'tenant_member_attribute',
        type='string',
        default='member',
        description="")

    keystone_2013_1_3.param(
        'tenant_name_attribute',
        type='string',
        default='ou',
        description="")

    keystone_2013_1_3.param(
        'tenant_desc_attribute',
        type='string',
        default='desc',
        description="")

    keystone_2013_1_3.param(
        'tenant_enabled_attribute',
        type='string',
        default='enabled',
        description="")

    keystone_2013_1_3.param(
        'tenant_attribute_ignore',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'tenant_allow_create',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'tenant_allow_update',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'tenant_allow_delete',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'tenant_enabled_emulation',
        type='boolean',
        default=False,
        description="")

    keystone_2013_1_3.param(
        'tenant_enabled_emulation_dn',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'role_tree_dn',
        type='string',
        default='ouRoles,dcexample,dccom',
        description="")

    keystone_2013_1_3.param('role_filter', type='string', default='', description="")

    keystone_2013_1_3.param(
        'role_objectclass',
        type='string',
        default='organizationalRole',
        description="")

    keystone_2013_1_3.param(
        'role_id_attribute',
        type='string',
        default='cn',
        description="")

    keystone_2013_1_3.param(
        'role_name_attribute',
        type='string',
        default='ou',
        description="")

    keystone_2013_1_3.param(
        'role_member_attribute',
        type='string',
        default='roleOccupant',
        description="")

    keystone_2013_1_3.param(
        'role_attribute_ignore',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'role_allow_create',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'role_allow_update',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'role_allow_delete',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param('group_tree_dn', type='string', default='', description="")

    keystone_2013_1_3.param('group_filter', type='string', default='', description="")

    keystone_2013_1_3.param(
        'group_objectclass',
        type='string',
        default='groupOfNames',
        description="")

    keystone_2013_1_3.param(
        'group_id_attribute',
        type='string',
        default='cn',
        description="")

    keystone_2013_1_3.param(
        'group_name_attribute',
        type='string',
        default='ou',
        description="")

    keystone_2013_1_3.param(
        'group_member_attribute',
        type='string',
        default='member',
        description="")

    keystone_2013_1_3.param(
        'group_desc_attribute',
        type='string',
        default='desc',
        description="")

    keystone_2013_1_3.param(
        'group_attribute_ignore',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'group_allow_create',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'group_allow_update',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'group_allow_delete',
        type='boolean',
        default=True,
        description="")

    keystone_2013_1_3.param(
        'use_tls',
        type='boolean',
        default=False,
        description="ldap TLS options if both tls_cacertfile and tls_cacertdir "
                    "are set then tls_cacertfile will be used and tls_cacertdir "
                    "is ignored valid options for tls_req_cert are demand, never, "
                    "and allow")

    keystone_2013_1_3.param('tls_cacertfile', type='string', default='', description="")

    keystone_2013_1_3.param('tls_cacertdir', type='string', default='', description="")

    keystone_2013_1_3.param('tls_req_cert', type='string', default='demand', description="")

    keystone_2013_1_3.param(
        'user_additional_attribute_mapping',
        type='string',
        default='description:name, gecos:name',
        description="Additional attribute mappings can be used to map ldap "
                    "attributes to internal keystone attributes. This allows "
                    "keystone to fulfill ldap objectclass requirements. An "
                    "example to map the description and gecos attributes to a "
                    "user's name would be:")

    keystone_2013_1_3.param(
        'domain_additional_attribute_mapping',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'group_additional_attribute_mapping',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'role_additional_attribute_mapping',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'project_additional_attribute_mapping',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.param(
        'user_additional_attribute_mapping',
        type='string',
        default='',
        description="")

    keystone_2013_1_3.section('auth')

    keystone_2013_1_3.param(
        'methods',
        type='string',
        default='external,password,token,oauth1',
        description="")

    keystone_2013_1_3.param(
        'external',
        type='string',
        default='keystone_2013_1_3.auth.plugins.external.ExternalDefault',
        description="")

    keystone_2013_1_3.param(
        'password',
        type='string',
        default='keystone_2013_1_3.auth.plugins.password.Password',
        description="")

    keystone_2013_1_3.param(
        'token',
        type='string',
        default='keystone_2013_1_3.auth.plugins.token.Token',
        description="")

    keystone_2013_1_3.param(
        'oauth1',
        type='string',
        default='keystone_2013_1_3.auth.plugins.oauth1.OAuth',
        description="")

    keystone_2013_1_3.section('paste_deploy')

    keystone_2013_1_3.param(
        'config_file',
        type='string',
        default='keystone-paste.ini',
        description="Name of the paste configuration file that defines the "
                    "available pipelines")
