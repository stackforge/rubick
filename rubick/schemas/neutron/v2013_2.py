from rubick.schema import ConfigSchemaRegistry

neutron = ConfigSchemaRegistry.register_schema(project='neutron')

with neutron.version('2013.2') as neutron_2013_2:

    neutron_2013_2.section('DEFAULT')

    neutron_2013_2.param('debug', type='string', default='False',
                         description="Default log level is INFO verbose and debug has the same result. One of them will set DEBUG log level output")

    neutron_2013_2.param('verbose', type='string', default='False',
                         description="Default log level is INFO verbose and debug has the same result. One of them will set DEBUG log level output")

    neutron_2013_2.param(
        'state_path', type='string', default='/var/lib/neutron',
        description="Where to store Neutron state files.  This directory must be writable by the user executing the agent.")

    neutron_2013_2.param('lock_path', type='string',
                         default='$state_path/lock', description="Where to store lock files")

    neutron_2013_2.param('log_format', type='string',
                         default='%(asctime)s %(levelname)8s [%(name)s] %(message)s', description="")

    neutron_2013_2.param(
        'log_date_format', type='string', default='%Y-%m-%d %H:%M:%S', description="")

    neutron_2013_2.param(
        'use_syslog', type='string', default='False', description="")

    neutron_2013_2.param(
        'syslog_log_facility', type='string', default='LOG_USER', description="")

    neutron_2013_2.param(
        'use_stderr', type='string', default='True', description="")

    neutron_2013_2.param(
        'publish_errors', type='string', default='False', description="")

    neutron_2013_2.param('bind_host', type='host',
                         default='0.0.0.0', description="Address to bind the API server")

    neutron_2013_2.param('bind_port', type='string',
                         default='9696', description="Port the bind the API server to")

    neutron_2013_2.param('api_extensions_path', type='string', default='',
                         description="Path to the extensions.  Note that this can be a colon-separated list of paths.  For example: api_extensions_path = extensions:/path/to/more/extensions:/even/more/extensions The __path__ of neutron.extensions is appended to this, so if your extensions are in there you don't need to specify them here")

    neutron_2013_2.param('core_plugin', type='string',
                         default='', description="Neutron plugin provider module")

    neutron_2013_2.param('service_plugins', type='string',
                         default='', description="Advanced service modules")

    neutron_2013_2.param('api_paste_config', type='string',
                         default='api-paste.ini', description="Paste configuration file")

    neutron_2013_2.param('auth_strategy', type='string', default='keystone',
                         description="The strategy to be used for auth. Supported values are 'keystone'(default), 'noauth'.")

    neutron_2013_2.param('mac_generation_retries', type='string', default='16',
                         description="Maximum amount of retries to generate a unique MAC address")

    neutron_2013_2.param('dhcp_lease_duration', type='string',
                         default='86400', description="DHCP Lease duration (in seconds)")

    neutron_2013_2.param(
        'dhcp_agent_notification', type='string', default='True',
        description="Allow sending resource operation notification to DHCP agent")

    neutron_2013_2.param('allow_bulk', type='string', default='True',
                         description="Enable or disable bulk create/update/delete operations")

    neutron_2013_2.param('allow_pagination', type='string', default='False',
                         description="Enable or disable bulk create/update/delete operations Enable or disable pagination")

    neutron_2013_2.param('allow_sorting', type='string', default='False',
                         description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting")

    neutron_2013_2.param(
        'allow_overlapping_ips', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting Enable or disable overlapping IPs for subnets Attention: the following parameter MUST be set to False if Neutron is being used in conjunction with nova security groups")

    neutron_2013_2.param(
        'force_gateway_on_subnet', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting Enable or disable overlapping IPs for subnets Attention: the following parameter MUST be set to False if Neutron is being used in conjunction with nova security groups Ensure that configured gateway is on subnet")

    neutron_2013_2.param('rpc_thread_pool_size', type='string', default='64',
                         description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. rpc_backend = neutron.openstack.common.rpc.impl_kombu Size of RPC thread pool")

    neutron_2013_2.param('rpc_conn_pool_size', type='string', default='30',
                         description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. rpc_backend = neutron.openstack.common.rpc.impl_kombu Size of RPC thread pool Size of RPC connection pool")

    neutron_2013_2.param('rpc_response_timeout', type='string', default='60',
                         description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. rpc_backend = neutron.openstack.common.rpc.impl_kombu Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall")

    neutron_2013_2.param('rpc_cast_timeout', type='string', default='30',
                         description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. rpc_backend = neutron.openstack.common.rpc.impl_kombu Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall Seconds to wait before a cast expires (TTL). Only supported by impl_zmq.")

    neutron_2013_2.param('control_exchange', type='string', default='neutron',
                         description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. rpc_backend = neutron.openstack.common.rpc.impl_kombu Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall Seconds to wait before a cast expires (TTL). Only supported by impl_zmq. Modules of exceptions that are permitted to be recreated upon receiving exception data from an rpc call. allowed_rpc_exception_modules = neutron.openstack.common.exception, nova.exception AMQP exchange to connect to if using RabbitMQ or QPID")

    neutron_2013_2.param('fake_rabbit', type='string', default='False',
                         description="If passed, use a fake RabbitMQ provider")

    neutron_2013_2.param(
        'notification_driver', type='string', default='neutron.openstack.common.notifier.rpc_notifier',
        description="Notification_driver can be defined multiple times Do nothing driver notification_driver = neutron.openstack.common.notifier.no_op_notifier Logging driver notification_driver = neutron.openstack.common.notifier.log_notifier RPC driver. DHCP agents needs it.")

    neutron_2013_2.param(
        'default_notification_level', type='string', default='INFO',
        description="default_notification_level is used to form actual topic name(s) or to set logging level")

    neutron_2013_2.param('pagination_max_limit', type='string', default='-1',
                         description="Default maximum number of items returned in a single response, value == infinite and value < 0 means no max limit, and value must greater than 0. If the number of items requested is greater than pagination_max_limit, server will just return pagination_max_limit of number of items.")

    neutron_2013_2.param('max_dns_nameservers', type='string', default='5',
                         description="Maximum number of DNS nameservers per subnet")

    neutron_2013_2.param('max_subnet_host_routes', type='string',
                         default='20', description="Maximum number of host routes per subnet")

    neutron_2013_2.param('max_fixed_ips_per_port', type='string',
                         default='5', description="Maximum number of fixed ips per port")

    neutron_2013_2.param('agent_down_time', type='string', default='5',
                         description="=========== items for agent management extension ============= Seconds to regard the agent as down.")

    neutron_2013_2.param(
        'network_scheduler_driver', type='string', default='neutron.scheduler.dhcp_agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent")

    neutron_2013_2.param(
        'router_scheduler_driver', type='string', default='neutron.scheduler.l3_agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent Driver to use for scheduling router to a default L3 agent")

    neutron_2013_2.param(
        'loadbalancer_pool_scheduler_driver', type='string', default='neutron.services.loadbalancer.agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent Driver to use for scheduling router to a default L3 agent Driver to use for scheduling a loadbalancer pool to an lbaas agent")

    neutron_2013_2.param(
        'network_auto_schedule', type='string', default='True',
        description="Allow auto scheduling networks to DHCP agent. It will schedule non-hosted networks to first DHCP agent which sends get_active_networks message to neutron server")

    neutron_2013_2.param('router_auto_schedule', type='string', default='True',
                         description="Allow auto scheduling routers to L3 agent. It will schedule non-hosted routers to first L3 agent which sends sync_routers message to neutron server")

    neutron_2013_2.param('dhcp_agents_per_network', type='string', default='1',
                         description="Number of DHCP agents scheduled to host a network. This enables redundant DHCP agents for configured networks.")

    neutron_2013_2.param('tcp_keepidle', type='string', default='600',
                         description="=========== WSGI parameters related to the API server ============== Sets the value of TCP_KEEPIDLE in seconds to use for each server socket when starting API server. Not supported on OS X.")

    neutron_2013_2.param('retry_until_window', type='string', default='30',
                         description="Number of seconds to keep retrying to listen")

    neutron_2013_2.param('backlog', type='string', default='4096',
                         description="Number of backlog requests to configure the socket with.")

    neutron_2013_2.param('use_ssl', type='string',
                         default='False', description="Enable SSL on the API server")

    neutron_2013_2.param(
        'ssl_cert_file', type='string', default='/path/to/certfile',
        description="Certificate file to use when starting API server securely")

    neutron_2013_2.param(
        'ssl_key_file', type='string', default='/path/to/keyfile',
        description="Private key file to use when starting API server securely")

    neutron_2013_2.param(
        'ssl_ca_file', type='string', default='/path/to/cafile',
        description="CA certificate file to use when starting API server securely to verify connecting clients. This is an optional parameter only required if API clients need to authenticate to the API server using SSL certificates signed by a trusted CA")

    neutron_2013_2.section('quotas')

    neutron_2013_2.param(
        'quota_items', type='string', default='network,subnet,port',
        description="resource name(s) that are supported in quota features")

    neutron_2013_2.param('default_quota', type='string', default='-1',
                         description="default number of resource allowed per tenant, minus for unlimited")

    neutron_2013_2.param('quota_network', type='string', default='10',
                         description="number of networks allowed per tenant, and minus means unlimited")

    neutron_2013_2.param('quota_subnet', type='string', default='10',
                         description="number of subnets allowed per tenant, and minus means unlimited")

    neutron_2013_2.param('quota_port', type='string', default='50',
                         description="number of ports allowed per tenant, and minus means unlimited")

    neutron_2013_2.param('quota_security_group', type='string', default='10',
                         description="number of security groups allowed per tenant, and minus means unlimited")

    neutron_2013_2.param(
        'quota_security_group_rule', type='string', default='100',
        description="number of security group rules allowed per tenant, and minus means unlimited")

    neutron_2013_2.param(
        'quota_driver', type='string', default='neutron.db.quota_db.DbQuotaDriver',
        description="default driver to use for quota checks")

    neutron_2013_2.section('agent')

    neutron_2013_2.param('root_helper', type='string', default='sudo',
                         description="Use 'sudo neutron-rootwrap /etc/neutron/rootwrap.conf' to use the real root filter facility. Change to 'sudo' to skip the filtering and just run the comand directly")

    neutron_2013_2.param('report_interval', type='string', default='4',
                         description="=========== items for agent management extension ============= seconds between nodes reporting state to server, should be less than agent_down_time")

    neutron_2013_2.section('keystone_authtoken')

    neutron_2013_2.param(
        'auth_host', type='host', default='127.0.0.1', description="")

    neutron_2013_2.param(
        'auth_port', type='string', default='35357', description="")

    neutron_2013_2.param(
        'auth_protocol', type='string', default='http', description="")

    neutron_2013_2.param('admin_tenant_name', type='string',
                         default='%SERVICE_TENANT_NAME%', description="")

    neutron_2013_2.param(
        'admin_user', type='string', default='%SERVICE_USER%', description="")

    neutron_2013_2.param(
        'admin_password', type='string', default='%SERVICE_PASSWORD%', description="")

    neutron_2013_2.param('signing_dir', type='string',
                         default='$state_path/keystone-signing', description="")

    neutron_2013_2.section('database')

    neutron_2013_2.param(
        'connection', type='string', default='mysql://root:pass@127.0.0.1:3306/neutron',
        description="This line MUST be changed to actually run the plugin. Example:")

    neutron_2013_2.param('slave_connection', type='string', default='',
                         description="The SQLAlchemy connection string used to connect to the slave database")

    neutron_2013_2.param('max_retries', type='string', default='10',
                         description="Database reconnection retry times - in event connectivity is lost set to -1 implies an infinite retry count")

    neutron_2013_2.param('retry_interval', type='string', default='10',
                         description="Database reconnection interval in seconds - if the initial connection to the database fails")

    neutron_2013_2.param('min_pool_size', type='string', default='1',
                         description="Minimum number of SQL connections to keep open in a pool")

    neutron_2013_2.param('max_pool_size', type='string', default='10',
                         description="Maximum number of SQL connections to keep open in a pool")

    neutron_2013_2.param('idle_timeout', type='string', default='3600',
                         description="Timeout in seconds before idle sql connections are reaped")

    neutron_2013_2.param('max_overflow', type='string', default='20',
                         description="If set, use this value for max_overflow with sqlalchemy")

    neutron_2013_2.param('connection_debug', type='string', default='0',
                         description="Verbosity of SQL debugging information. 0=None, 100=Everything")

    neutron_2013_2.param('connection_trace', type='string', default='False',
                         description="Add python stack traces to SQL as comment strings")

    neutron_2013_2.param('pool_timeout', type='string', default='10',
                         description="If set, use this value for pool_timeout with sqlalchemy")

    neutron_2013_2.section('service_providers')

    neutron_2013_2.param(
        'service_provider', type='string', default='LOADBALANCER:name:lbaas_plugin_driver_path:default',
        description="Specify service providers (drivers) for advanced services like loadbalancer, VPN, Firewall. Must be in form: service_provider=<service_type>:<name>:<driver>[:default] List of allowed service type include LOADBALANCER, FIREWALL, VPN Combination of <service type> and <name> must be unique; <driver> must also be unique this is multiline option, example for default provider:")

    neutron_2013_2.param(
        'service_provider', type='string', default='LOADBALANCER:Haproxy:neutron.services.loadbalancer.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default',
        description="Specify service providers (drivers) for advanced services like loadbalancer, VPN, Firewall. Must be in form: service_provider=<service_type>:<name>:<driver>[:default] List of allowed service type include LOADBALANCER, FIREWALL, VPN Combination of <service type> and <name> must be unique; <driver> must also be unique this is multiline option, example for default provider: example of non-default provider: service_provider=FIREWALL:name2:firewall_driver_path --- Reference implementations ---")

    neutron_2013_2.param(
        'service_provider', type='string', default='LOADBALANCER:Radware:neutron.services.loadbalancer.drivers.radware.driver.LoadBalancerDriver:default',
        description="Specify service providers (drivers) for advanced services like loadbalancer, VPN, Firewall. Must be in form: service_provider=<service_type>:<name>:<driver>[:default] List of allowed service type include LOADBALANCER, FIREWALL, VPN Combination of <service type> and <name> must be unique; <driver> must also be unique this is multiline option, example for default provider: example of non-default provider: service_provider=FIREWALL:name2:firewall_driver_path --- Reference implementations --- In order to activate Radware's lbaas driver you need to uncomment the next line. If you want to keep the HA Proxy as the default lbaas driver, remove the attribute default from the line below. Otherwise comment the HA Proxy line")
