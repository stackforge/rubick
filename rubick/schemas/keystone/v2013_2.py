from rubick.schema import ConfigSchemaRegistry

keystone = ConfigSchemaRegistry.register_schema(project='keystone')

with keystone.version('2013.2') as keystone_2013_2:

    keystone_2013_2.section('DEFAULT')

    keystone_2013_2.param('admin_token', type='string', default='ADMIN',
                          description="A 'shared secret' between keystone and other openstack services")

    keystone_2013_2.param('bind_host', type='host', default='0.0.0.0',
                          description="The IP address of the network interface to listen on")

    keystone_2013_2.param('public_port', type='string', default='5000',
                          description="The port number which the public service listens on")

    keystone_2013_2.param('admin_port', type='string', default='35357',
                          description="The port number which the public admin listens on")

    keystone_2013_2.param(
        'public_endpoint', type='string', default='http://localhost:%(public_port)s/',
        description="The base endpoint URLs for keystone that are advertised to clients (NOTE: this does NOT affect how keystone listens for connections)")

    keystone_2013_2.param(
        'admin_endpoint', type='string', default='http://localhost:%(admin_port)s/',
        description="The base endpoint URLs for keystone that are advertised to clients (NOTE: this does NOT affect how keystone listens for connections)")

    keystone_2013_2.param('compute_port', type='string', default='8774',
                          description="The port number which the OpenStack Compute service listens on")

    keystone_2013_2.param('policy_file', type='string', default='policy.json',
                          description="Path to your policy definition containing identity actions")

    keystone_2013_2.param(
        'policy_default_rule', type='string', default='admin_required',
        description="Rule to check if no matching policy definition is found FIXME(dolph): This should really be defined as [policy] default_rule")

    keystone_2013_2.param(
        'member_role_id', type='string', default='9fe2ff9ee4384b1894a90878d3e92bab',
        description="Role for migrating membership relationships During a SQL upgrade, the following values will be used to create a new role that will replace records in the user_tenant_membership table with explicit role grants.  After migration, the member_role_id will be used in the API add_user_to_project, and member_role_name will be ignored.")

    keystone_2013_2.param(
        'member_role_name', type='string', default='_member_',
        description="Role for migrating membership relationships During a SQL upgrade, the following values will be used to create a new role that will replace records in the user_tenant_membership table with explicit role grants.  After migration, the member_role_id will be used in the API add_user_to_project, and member_role_name will be ignored.")

    keystone_2013_2.param(
        'max_request_body_size', type='string', default='114688',
        description="enforced by optional sizelimit middleware (keystone.middleware:RequestBodySizeLimiter)")

    keystone_2013_2.param('max_param_size', type='string', default='64',
                          description="limit the sizes of user & tenant ID/names")

    keystone_2013_2.param('max_token_size', type='string', default='8192',
                          description="similar to max_param_size, but provides an exception for token values")

    keystone_2013_2.param('debug', type='string', default='False',
                          description="=== Logging Options === Print debugging output (includes plaintext request logging, potentially including passwords)")

    keystone_2013_2.param('verbose', type='string',
                          default='False', description="Print more verbose output")

    keystone_2013_2.param('log_file', type='string', default='keystone.log',
                          description="Name of log file to output to. If not set, logging will go to stdout.")

    keystone_2013_2.param(
        'log_dir', type='string', default='/var/log/keystone',
        description="The directory to keep log files in (will be prepended to --logfile)")

    keystone_2013_2.param('use_syslog', type='string',
                          default='False', description="Use syslog for logging.")

    keystone_2013_2.param('syslog_log_facility', type='string',
                          default='LOG_USER', description="syslog facility to receive log lines")

    keystone_2013_2.param('log_config', type='string', default='logging.conf',
                          description="If this option is specified, the logging configuration file specified is used and overrides any other logging options specified. Please see the Python logging module documentation for details on logging configuration files.")

    keystone_2013_2.param('log_format', type='string',
                          default='%(asctime)s %(levelname)8s [%(name)s] %(message)s', description="A logging.Formatter log message format string which may use any of the available logging.LogRecord attributes.")

    keystone_2013_2.param(
        'log_date_format', type='string', default='%Y-%m-%d %H:%M:%S',
        description="Format string for %(asctime)s in log records.")

    keystone_2013_2.param(
        'onready', type='string', default='keystone.common.systemd',
        description="onready allows you to send a notification when the process is ready to serve For example, to have it notify using systemd, one could set shell command: onready = systemd-notify --ready or a module with notify() method:")

    keystone_2013_2.param(
        'notification_driver', type='string', default='keystone.openstack.common.notifier.rpc_notifier',
        description="notification_driver can be defined multiple times Do nothing driver (the default) notification_driver = keystone.openstack.common.notifier.no_op_notifier Logging driver example (not enabled by default) notification_driver = keystone.openstack.common.notifier.log_notifier RPC driver example (not enabled by default)")

    keystone_2013_2.param(
        'default_notification_level', type='string', default='INFO',
        description="Default notification level for outgoing notifications")

    keystone_2013_2.param('default_publisher_id', type='string', default='',
                          description="Default publisher_id for outgoing notifications; included in the payload.")

    keystone_2013_2.param(
        'notification_topics', type='string', default='notifications',
        description="AMQP topics to publish to when using the RPC notification driver. Multiple values can be specified by separating with commas. The actual topic names will be %s.%(default_notification_level)s")

    keystone_2013_2.param(
        'rpc_backend', type='string', default='keystone.openstack.common.rpc.impl_kombu',
        description="The messaging module to use, defaults to kombu.")

    keystone_2013_2.param('rpc_thread_pool_size', type='string',
                          default='64', description="Size of RPC thread pool")

    keystone_2013_2.param('rpc_conn_pool_size', type='string',
                          default='30', description="Size of RPC connection pool")

    keystone_2013_2.param('rpc_response_timeout', type='string', default='60',
                          description="Seconds to wait for a response from call or multicall")

    keystone_2013_2.param('rpc_cast_timeout', type='string', default='30',
                          description="Seconds to wait before a cast expires (TTL). Only supported by impl_zmq.")

    keystone_2013_2.param(
        'allowed_rpc_exception_modules', type='string', default='keystone.openstack.common.exception,nova.exception,cinder.exception,exceptions',
        description="Modules of exceptions that are permitted to be recreated upon receiving exception data from an rpc call.")

    keystone_2013_2.param('fake_rabbit', type='string', default='False',
                          description="If True, use a fake RabbitMQ provider")

    keystone_2013_2.param(
        'control_exchange', type='string', default='openstack',
        description="AMQP exchange to connect to if using RabbitMQ or Qpid")

    keystone_2013_2.section('sql')

    keystone_2013_2.param(
        'connection', type='string', default='sqlite:///keystone.db',
        description="The SQLAlchemy connection string used to connect to the database")

    keystone_2013_2.param('idle_timeout', type='string', default='200',
                          description="the timeout before idle sql connections are reaped")

    keystone_2013_2.section('identity')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.identity.backends.sql.Identity', description="")

    keystone_2013_2.param(
        'default_domain_id', type='string', default='default',
        description="This references the domain to use for all Identity API v2 requests (which are not aware of domains). A domain with this ID will be created for you by keystone-manage db_sync in migration 008.  The domain referenced by this ID cannot be deleted on the v3 API, to prevent accidentally breaking the v2 API. There is nothing special about this domain, other than the fact that it must exist to order to maintain support for your v2 clients.")

    keystone_2013_2.param(
        'domain_specific_drivers_enabled', type='string', default='False',
        description="A subset (or all) of domains can have their own identity driver, each with their own partial configuration file in a domain configuration directory. Only values specific to the domain need to be placed in the domain specific configuration file. This feature is disabled by default; set domain_specific_drivers_enabled to True to enable.")

    keystone_2013_2.param(
        'domain_config_dir', type='string', default='/etc/keystone/domains',
        description="A subset (or all) of domains can have their own identity driver, each with their own partial configuration file in a domain configuration directory. Only values specific to the domain need to be placed in the domain specific configuration file. This feature is disabled by default; set domain_specific_drivers_enabled to True to enable.")

    keystone_2013_2.param('max_password_length', type='string', default='4096',
                          description="Maximum supported length for user passwords; decrease to improve performance.")

    keystone_2013_2.section('credential')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.credential.backends.sql.Credential', description="")

    keystone_2013_2.section('trust')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.trust.backends.sql.Trust', description="")

    keystone_2013_2.param('enabled', type='string', default='True',
                          description="delegation and impersonation features can be optionally disabled")

    keystone_2013_2.section('os_inherit')

    keystone_2013_2.param('enabled', type='string', default='False',
                          description="role-assignment inheritance to projects from owning domain can be optionally enabled")

    keystone_2013_2.section('catalog')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.catalog.backends.sql.Catalog',
        description="dynamic, sql-based backend (supports API/CLI-based management commands)")

    keystone_2013_2.param(
        'driver', type='string', default='keystone.catalog.backends.templated.TemplatedCatalog',
        description="static, file-based backend (does *NOT* support any management commands)")

    keystone_2013_2.param('template_file', type='string',
                          default='default_catalog.templates', description="")

    keystone_2013_2.section('endpoint_filter')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.contrib.endpoint_filter.backends.sql.EndpointFilter',
        description="extension for creating associations between project and endpoints in order to provide a tailored catalog for project-scoped token requests.")

    keystone_2013_2.param(
        'return_all_endpoints_if_no_filter', type='string', default='True',
        description="extension for creating associations between project and endpoints in order to provide a tailored catalog for project-scoped token requests.")

    keystone_2013_2.section('token')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.token.backends.sql.Token', description="Provides token persistence.")

    keystone_2013_2.param('provider', type='string', default='',
                          description="Controls the token construction, validation, and revocation operations. Core providers are keystone.token.providers.[pki|uuid].Provider")

    keystone_2013_2.param('expiration', type='string', default='86400',
                          description="Amount of time a token should remain valid (in seconds)")

    keystone_2013_2.param('bind', type='string', default='',
                          description="External auth mechanisms that should add bind information to token. eg kerberos, x509")

    keystone_2013_2.param(
        'enforce_token_bind', type='string', default='permissive',
        description="Enforcement policy on tokens presented to keystone with bind information. One of disabled, permissive, strict, required or a specifically required bind mode e.g. kerberos or x509 to require binding to that authentication.")

    keystone_2013_2.param('caching', type='string', default='True',
                          description="Token specific caching toggle. This has no effect unless the global caching option is set to True")

    keystone_2013_2.param('cache_time', type='string', default='',
                          description="Token specific cache time-to-live (TTL) in seconds.")

    keystone_2013_2.param(
        'revocation_cache_time', type='string', default='3600',
        description="Revocation-List specific cache time-to-live (TTL) in seconds.")

    keystone_2013_2.section('cache')

    keystone_2013_2.param('enabled', type='string', default='False',
                          description="Global cache functionality toggle.")

    keystone_2013_2.param(
        'config_prefix', type='string', default='cache.keystone',
        description="Prefix for building the configuration dictionary for the cache region. This should not need to be changed unless there is another dogpile.cache region with the same configuration name")

    keystone_2013_2.param('expiration_time', type='string', default='600',
                          description="Default TTL, in seconds, for any cached item in the dogpile.cache region. This applies to any cached method that doesn't have an explicit cache expiration time defined for it.")

    keystone_2013_2.param(
        'backend', type='string', default='keystone.common.cache.noop',
        description="Dogpile.cache backend module. It is recommended that Memcache (dogpile.cache.memcache) or Redis (dogpile.cache.redis) be used in production deployments.  Small workloads (single process) like devstack can use the dogpile.cache.memory backend.")

    keystone_2013_2.param('backend_argument', type='string', default='',
                          description="Arguments supplied to the backend module. Specify this option once per argument to be passed to the dogpile.cache backend. Example format: <argname>:<value>")

    keystone_2013_2.param('proxies', type='string', default='',
                          description="Proxy Classes to import that will affect the way the dogpile.cache backend functions.  See the dogpile.cache documentation on changing-backend-behavior. Comma delimited list e.g. my.dogpile.proxy.Class, my.dogpile.proxyClass2")

    keystone_2013_2.param('use_key_mangler', type='string', default='True',
                          description="Use a key-mangling function (sha1) to ensure fixed length cache-keys. This is toggle-able for debugging purposes, it is highly recommended to always leave this set to True.")

    keystone_2013_2.param(
        'debug_cache_backend', type='string', default='False',
        description="Extra debugging from the cache backend (cache keys, get/set/delete/etc calls) This is only really useful if you need to see the specific cache-backend get/set/delete calls with the keys/values.  Typically this should be left set to False.")

    keystone_2013_2.section('policy')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.policy.backends.sql.Policy', description="")

    keystone_2013_2.section('ec2')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.contrib.ec2.backends.kvs.Ec2', description="")

    keystone_2013_2.section('assignment')

    keystone_2013_2.param('driver', type='string', default='', description="")

    keystone_2013_2.param('caching', type='string', default='True',
                          description="Assignment specific caching toggle. This has no effect unless the global caching option is set to True")

    keystone_2013_2.param('cache_time', type='string', default='',
                          description="Assignment specific cache time-to-live (TTL) in seconds.")

    keystone_2013_2.section('oauth1')

    keystone_2013_2.param(
        'driver', type='string', default='keystone.contrib.oauth1.backends.sql.OAuth1', description="")

    keystone_2013_2.param(
        'request_token_duration', type='string', default='28800',
        description="The Identity service may include expire attributes. If no such attribute is included, then the token lasts indefinitely. Specify how quickly the request token will expire (in seconds)")

    keystone_2013_2.param(
        'access_token_duration', type='string', default='86400',
        description="The Identity service may include expire attributes. If no such attribute is included, then the token lasts indefinitely. Specify how quickly the request token will expire (in seconds) Specify how quickly the access token will expire (in seconds)")

    keystone_2013_2.section('ssl')

    keystone_2013_2.param(
        'enable', type='string', default='True', description="")

    keystone_2013_2.param('certfile', type='string',
                          default='/etc/keystone/pki/certs/ssl_cert.pem', description="")

    keystone_2013_2.param(
        'keyfile', type='string', default='/etc/keystone/pki/private/ssl_key.pem', description="")

    keystone_2013_2.param('ca_certs', type='string',
                          default='/etc/keystone/pki/certs/cacert.pem', description="")

    keystone_2013_2.param(
        'ca_key', type='string', default='/etc/keystone/pki/private/cakey.pem', description="")

    keystone_2013_2.param(
        'key_size', type='string', default='1024', description="")

    keystone_2013_2.param(
        'valid_days', type='string', default='3650', description="")

    keystone_2013_2.param(
        'cert_required', type='string', default='False', description="")

    keystone_2013_2.param('cert_subject', type='string',
                          default='/C=US/ST=Unset/L=Unset/O=Unset/CN=localhost', description="")

    keystone_2013_2.section('signing')

    keystone_2013_2.param('token_format', type='string', default='',
                          description="Deprecated in favor of provider in the [token] section Allowed values are PKI or UUID")

    keystone_2013_2.param('certfile', type='string',
                          default='/etc/keystone/pki/certs/signing_cert.pem', description="")

    keystone_2013_2.param(
        'keyfile', type='string', default='/etc/keystone/pki/private/signing_key.pem', description="")

    keystone_2013_2.param('ca_certs', type='string',
                          default='/etc/keystone/pki/certs/cacert.pem', description="")

    keystone_2013_2.param(
        'ca_key', type='string', default='/etc/keystone/pki/private/cakey.pem', description="")

    keystone_2013_2.param(
        'key_size', type='string', default='2048', description="")

    keystone_2013_2.param(
        'valid_days', type='string', default='3650', description="")

    keystone_2013_2.param('cert_subject', type='string',
                          default='/C=US/ST=Unset/L=Unset/O=Unset/CN=www.example.com', description="")

    keystone_2013_2.section('ldap')

    keystone_2013_2.section('auth')

    keystone_2013_2.param(
        'methods', type='string', default='external,password,token,oauth1', description="")

    keystone_2013_2.param('external', type='string',
                          default='keystone.auth.plugins.external.ExternalDefault', description="")

    keystone_2013_2.param('password', type='string',
                          default='keystone.auth.plugins.password.Password', description="")

    keystone_2013_2.param(
        'token', type='string', default='keystone.auth.plugins.token.Token', description="")

    keystone_2013_2.param(
        'oauth1', type='string', default='keystone.auth.plugins.oauth1.OAuth', description="")

    keystone_2013_2.section('paste_deploy')

    keystone_2013_2.param(
        'config_file', type='string', default='keystone-paste.ini',
        description="Name of the paste configuration file that defines the available pipelines")
