from rubick.schema import ConfigSchemaRegistry

glance_registry = ConfigSchemaRegistry.register_schema(
    project='glance_registry')

with glance_registry.version('2013.2.1') as glance_registry_2013_2_1:

    glance_registry_2013_2_1.section('DEFAULT')

    glance_registry_2013_2_1.param('verbose', type='string', default='False',
                                   description="Show more verbose log output (sets INFO log level output)")

    glance_registry_2013_2_1.param('debug', type='string', default='False',
                                   description="Show debugging output in logs (sets DEBUG log level output)")

    glance_registry_2013_2_1.param(
        'bind_host', type='host', default='0.0.0.0', description="Address to bind the registry server")

    glance_registry_2013_2_1.param(
        'bind_port', type='string', default='9191', description="Port the bind the registry server to")

    glance_registry_2013_2_1.param(
        'log_file', type='string', default='/var/log/glance/registry.log',
        description="Log to this file. Make sure you do not set the same log file for both the API and registry servers!")

    glance_registry_2013_2_1.param(
        'backlog', type='string', default='4096', description="Backlog requests when creating socket")

    glance_registry_2013_2_1.param(
        'tcp_keepidle', type='string', default='600',
        description="TCP_KEEPIDLE value in seconds when creating socket. Not supported on OS X.")

    glance_registry_2013_2_1.param(
        'sql_connection', type='string', default='sqlite:///glance.sqlite',
        description="SQLAlchemy connection string for the reference implementation registry server. Any valid SQLAlchemy connection string is fine. See: http://www.sqlalchemy.org/docs/05/reference/sqlalchemy/connections.html#sqlalchemy.create_engine")

    glance_registry_2013_2_1.param(
        'sql_idle_timeout', type='string', default='3600',
        description="MySQL uses a default `wait_timeout` of 8 hours, after which it will drop idle connections. This can result in 'MySQL Gone Away' exceptions. If you notice this, you can lower this value to ensure that SQLAlchemy reconnects before MySQL can drop the connection.")

    glance_registry_2013_2_1.param(
        'api_limit_max', type='string', default='1000',
        description="Limit the api to return `param_limit_max` items in a call to a container. If a larger `limit` query param is provided, it will be reduced to this value.")

    glance_registry_2013_2_1.param(
        'limit_param_default', type='string', default='25',
        description="If a `limit` query param is not provided in an api request, it will default to `limit_param_default`")

    glance_registry_2013_2_1.param(
        'admin_role', type='string', default='admin',
        description="Role used to identify an authenticated user as administrator")

    glance_registry_2013_2_1.param(
        'db_auto_create', type='string', default='False',
        description="Whether to automatically create the database tables. Default: False")

    glance_registry_2013_2_1.param(
        'sqlalchemy_debug', type='string', default='True',
        description="Enable DEBUG log messages from sqlalchemy which prints every database query and response. Default: False")

    glance_registry_2013_2_1.param(
        'use_syslog', type='string', default='False',
        description="Send logs to syslog (/dev/log) instead of to file specified by `log_file`")

    glance_registry_2013_2_1.param('syslog_log_facility', type='string',
                                   default='LOG_LOCAL1', description="Facility to use. If unset defaults to LOG_USER.")

    glance_registry_2013_2_1.param(
        'cert_file', type='string', default='/path/to/certfile',
        description="Certificate file to use when starting registry server securely")

    glance_registry_2013_2_1.param(
        'key_file', type='string', default='/path/to/keyfile',
        description="Private key file to use when starting registry server securely")

    glance_registry_2013_2_1.param(
        'ca_file', type='string', default='/path/to/cafile',
        description="CA certificate file to use to verify connecting clients")

    glance_registry_2013_2_1.section('keystone_authtoken')

    glance_registry_2013_2_1.param(
        'auth_host', type='host', default='127.0.0.1')

    glance_registry_2013_2_1.param('auth_port', type='string', default='35357')

    glance_registry_2013_2_1.param(
        'auth_protocol', type='string', default='http')

    glance_registry_2013_2_1.param(
        'admin_tenant_name', type='string', default='%SERVICE_TENANT_NAME%')

    glance_registry_2013_2_1.param(
        'admin_user', type='string', default='%SERVICE_USER%')

    glance_registry_2013_2_1.param(
        'admin_password', type='string', default='%SERVICE_PASSWORD%')

    glance_registry_2013_2_1.section('paste_deploy')

    glance_registry_2013_2_1.param(
        'config_file', type='string', default='glance-registry-paste.ini',
        description="Name of the paste configuration file that defines the available pipelines")

    glance_registry_2013_2_1.param('flavor', type='string', default='',
                                   description="Partial name of a pipeline in your paste configuration file with the service name removed. For example, if your paste section name is [pipeline:glance-registry-keystone], you would configure the flavor below as 'keystone'.")
