from rubick.schema import ConfigSchemaRegistry

neutron_server = ConfigSchemaRegistry.register_schema(
    project='neutron_server')

with neutron_server.version('2013.2.1') as neutron_server_2013_2_1:

    neutron_server_2013_2_1.section('DEFAULT')

    neutron_server_2013_2_1.param('verbose', type='string', default='False',
                                     description="Default log level is INFO verbose and debug has the same result. One of them will set DEBUG log level output")

    neutron_server_2013_2_1.param(
        'state_path', type='string', default='/var/lib/neutron',
        description="Where to store Neutron state files.  This directory must be writable by the user executing the agent.")

    neutron_server_2013_2_1.param(
        'lock_path', type='string', default='$state_path/lock', description="Where to store lock files")

    neutron_server_2013_2_1.param(
        'log_format', type='string', default='%(asctime)s %(levelname)8s [%(name)s] %(message)s')

    neutron_server_2013_2_1.param(
        'log_date_format', type='string', default='%Y-%m-%d %H:%M:%S')

    neutron_server_2013_2_1.param(
        'use_syslog', type='string', default='False')

    neutron_server_2013_2_1.param(
        'syslog_log_facility', type='string', default='LOG_USER')

    neutron_server_2013_2_1.param(
        'use_stderr', type='string', default='True')

    neutron_server_2013_2_1.param(
        'publish_errors', type='string', default='False')

    neutron_server_2013_2_1.param(
        'bind_host', type='host', default='0.0.0.0', description="Address to bind the API server")

    neutron_server_2013_2_1.param(
        'bind_port', type='string', default='9696', description="Port the bind the API server to")

    neutron_server_2013_2_1.param(
        'api_extensions_path', type='string', default='',
        description="Path to the extensions.  Note that this can be a colon-separated list of paths.  For example: api_extensions_path = extensions:/path/to/more/extensions:/even/more/extensions The __path__ of neutron.extensions is appended to this, so if your extensions are in there you don't need to specify them here")

    neutron_server_2013_2_1.param(
        'core_plugin', type='string', default='', description="Neutron plugin provider module")

    neutron_server_2013_2_1.param(
        'service_plugins', type='string', default='', description="Advanced service modules")

    neutron_server_2013_2_1.param(
        'api_paste_config', type='string', default='api-paste.ini', description="Paste configuration file")

    neutron_server_2013_2_1.param(
        'auth_strategy', type='string', default='keystone',
        description="The strategy to be used for auth. Supported values are 'keystone'(default), 'noauth'.")

    neutron_server_2013_2_1.param(
        'mac_generation_retries', type='string', default='16',
        description="Maximum amount of retries to generate a unique MAC address")

    neutron_server_2013_2_1.param(
        'dhcp_lease_duration', type='string', default='86400', description="DHCP Lease duration (in seconds)")

    neutron_server_2013_2_1.param('dhcp_agent_notification', type='string',
                                     default='True', description="Allow sending resource operation notification to DHCP agent")

    neutron_server_2013_2_1.param(
        'allow_bulk', type='string', default='True', description="Enable or disable bulk create/update/delete operations")

    neutron_server_2013_2_1.param(
        'allow_pagination', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination")

    neutron_server_2013_2_1.param(
        'allow_sorting', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting")

    neutron_server_2013_2_1.param(
        'allow_overlapping_ips', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting Enable or disable overlapping IPs for subnets Attention: the following parameter MUST be set to False if Neutron is being used in conjunction with nova security groups")

    neutron_server_2013_2_1.param(
        'force_gateway_on_subnet', type='string', default='False',
        description="Enable or disable bulk create/update/delete operations Enable or disable pagination Enable or disable sorting Enable or disable overlapping IPs for subnets Attention: the following parameter MUST be set to False if Neutron is being used in conjunction with nova security groups Ensure that configured gateway is on subnet")

    neutron_server_2013_2_1.param(
        'rpc_backend', type='string', default='neutron.openstack.common.rpc.impl_kombu',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu.")

    neutron_server_2013_2_1.param(
        'rpc_thread_pool_size', type='string', default='64',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool")

    neutron_server_2013_2_1.param(
        'rpc_conn_pool_size', type='string', default='30',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool Size of RPC connection pool")

    neutron_server_2013_2_1.param(
        'rpc_response_timeout', type='string', default='60',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall")

    neutron_server_2013_2_1.param(
        'rpc_cast_timeout', type='string', default='30',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall Seconds to wait before a cast expires (TTL). Only supported by impl_zmq.")

    neutron_server_2013_2_1.param(
        'allowed_rpc_exception_modules', type='string', default='neutron.openstack.common.exception, nova.exception',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall Seconds to wait before a cast expires (TTL). Only supported by impl_zmq. Modules of exceptions that are permitted to be recreated upon receiving exception data from an rpc call.")

    neutron_server_2013_2_1.param(
        'control_exchange', type='string', default='neutron',
        description="RPC configuration options. Defined in rpc __init__ The messaging module to use, defaults to kombu. Size of RPC thread pool Size of RPC connection pool Seconds to wait for a response from call or multicall Seconds to wait before a cast expires (TTL). Only supported by impl_zmq. Modules of exceptions that are permitted to be recreated upon receiving exception data from an rpc call. AMQP exchange to connect to if using RabbitMQ or QPID")

    neutron_server_2013_2_1.param(
        'fake_rabbit', type='string', default='False', description="If passed, use a fake RabbitMQ provider")

    neutron_server_2013_2_1.param(
        'kombu_ssl_version', type='string', default='',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled)")

    neutron_server_2013_2_1.param(
        'kombu_ssl_keyfile', type='string', default='',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled)")

    neutron_server_2013_2_1.param(
        'kombu_ssl_certfile', type='string', default='',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled)")

    neutron_server_2013_2_1.param(
        'kombu_ssl_ca_certs', type='string', default='',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)'")

    neutron_server_2013_2_1.param(
        'rabbit_host', type='host', default='localhost',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation")

    neutron_server_2013_2_1.param(
        'rabbit_password', type='string', default='guest',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server")

    neutron_server_2013_2_1.param(
        'rabbit_port', type='string', default='5672',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening")

    neutron_server_2013_2_1.param(
        'rabbit_hosts', type='string', default='localhost:5672',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port'")

    neutron_server_2013_2_1.param(
        'rabbit_userid', type='string', default='guest',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port' User ID used for RabbitMQ connections")

    neutron_server_2013_2_1.param(
        'rabbit_virtual_host', type='string', default='/',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port' User ID used for RabbitMQ connections Location of a virtual RabbitMQ installation.")

    neutron_server_2013_2_1.param(
        'rabbit_max_retries', type='string', default='0',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port' User ID used for RabbitMQ connections Location of a virtual RabbitMQ installation. Maximum retries with trying to connect to RabbitMQ (the default of 0 implies an infinite retry count)")

    neutron_server_2013_2_1.param(
        'rabbit_retry_interval', type='string', default='1',
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port' User ID used for RabbitMQ connections Location of a virtual RabbitMQ installation. Maximum retries with trying to connect to RabbitMQ (the default of 0 implies an infinite retry count) RabbitMQ connection retry interval")

    neutron_server_2013_2_1.param(
        'rabbit_ha_queues', type='boolean', default=False,
        description="Configuration options if sending notifications via kombu rpc (these are the defaults) SSL version to use (valid only if SSL enabled) SSL key file (valid only if SSL enabled) SSL cert file (valid only if SSL enabled) SSL certification authority file (valid only if SSL enabled)' IP address of the RabbitMQ installation Password of the RabbitMQ server Port where RabbitMQ server is running/listening RabbitMQ single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) rabbit_hosts is defaulted to '$rabbit_host:$rabbit_port' User ID used for RabbitMQ connections Location of a virtual RabbitMQ installation. Maximum retries with trying to connect to RabbitMQ (the default of 0 implies an infinite retry count) RabbitMQ connection retry interval Use HA queues in RabbitMQ (x-ha-policy: all).You need to wipe RabbitMQ database when changing this option. ")

    neutron_server_2013_2_1.param(
        'rpc_backend', type='string', default='neutron.openstack.common.rpc.impl_qpid', description="QPID")

    neutron_server_2013_2_1.param(
        'qpid_hostname', type='string', default='localhost', description="QPID Qpid broker hostname")

    neutron_server_2013_2_1.param(
        'qpid_port', type='string', default='5672', description="QPID Qpid broker hostname Qpid broker port")

    neutron_server_2013_2_1.param(
        'qpid_hosts', type='string', default='localhost:5672',
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port'")

    neutron_server_2013_2_1.param(
        'qpid_username', type='string', default="''",
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection")

    neutron_server_2013_2_1.param(
        'qpid_password', type='string', default="''",
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection Password for qpid connection")

    neutron_server_2013_2_1.param(
        'qpid_sasl_mechanisms', type='string', default="''",
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection Password for qpid connection Space separated list of SASL mechanisms to use for auth")

    neutron_server_2013_2_1.param(
        'qpid_heartbeat', type='string', default='60',
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection Password for qpid connection Space separated list of SASL mechanisms to use for auth Seconds between connection keepalive heartbeats")

    neutron_server_2013_2_1.param(
        'qpid_protocol', type='string', default='tcp',
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection Password for qpid connection Space separated list of SASL mechanisms to use for auth Seconds between connection keepalive heartbeats Transport to use, either 'tcp' or 'ssl'")

    neutron_server_2013_2_1.param(
        'qpid_tcp_nodelay', type='string', default='True',
        description="QPID Qpid broker hostname Qpid broker port Qpid single or HA cluster (host:port pairs i.e: host1:5672, host2:5672) qpid_hosts is defaulted to '$qpid_hostname:$qpid_port' Username for qpid connection Password for qpid connection Space separated list of SASL mechanisms to use for auth Seconds between connection keepalive heartbeats Transport to use, either 'tcp' or 'ssl' Disable Nagle algorithm")

    neutron_server_2013_2_1.param(
        'rpc_backend', type='string', default='neutron.openstack.common.rpc.impl_zmq', description="ZMQ")

    neutron_server_2013_2_1.param(
        'rpc_zmq_bind_address', type='string', default='*',
        description="ZMQ ZeroMQ bind address. Should be a wildcard (*), an ethernet interface, or IP. The 'host' option should point or resolve to this address.")

    neutron_server_2013_2_1.param(
        'notification_driver', type='string', default='neutron.openstack.common.notifier.rpc_notifier',
        description="Notification_driver can be defined multiple times Do nothing driver notification_driver = neutron.openstack.common.notifier.no_op_notifier Logging driver notification_driver = neutron.openstack.common.notifier.log_notifier RPC driver. DHCP agents needs it.")

    neutron_server_2013_2_1.param(
        'default_notification_level', type='string', default='INFO',
        description="default_notification_level is used to form actual topic name(s) or to set logging level")

    neutron_server_2013_2_1.param(
        'host', type='string', default='myhost.com',
        description="default_publisher_id is a part of the notification payload")

    neutron_server_2013_2_1.param(
        'default_publisher_id', type='string', default='$host',
        description="default_publisher_id is a part of the notification payload")

    neutron_server_2013_2_1.param(
        'notification_topics', type='string', default='notifications',
        description="Defined in rpc_notifier, can be comma separated values. The actual topic names will be %s.%(default_notification_level)s")

    neutron_server_2013_2_1.param(
        'pagination_max_limit', type='string', default='-1',
        description="Default maximum number of items returned in a single response, value == infinite and value < 0 means no max limit, and value must greater than 0. If the number of items requested is greater than pagination_max_limit, server will just return pagination_max_limit of number of items.")

    neutron_server_2013_2_1.param('max_dns_nameservers', type='string',
                                     default='5', description="Maximum number of DNS nameservers per subnet")

    neutron_server_2013_2_1.param('max_subnet_host_routes', type='string',
                                     default='20', description="Maximum number of host routes per subnet")

    neutron_server_2013_2_1.param(
        'max_fixed_ips_per_port', type='string', default='5', description="Maximum number of fixed ips per port")

    neutron_server_2013_2_1.param(
        'agent_down_time', type='string', default='5',
        description="=========== items for agent management extension ============= Seconds to regard the agent as down.")

    neutron_server_2013_2_1.param(
        'network_scheduler_driver', type='string', default='neutron.scheduler.dhcp_agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent")

    neutron_server_2013_2_1.param(
        'router_scheduler_driver', type='string', default='neutron.scheduler.l3_agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent Driver to use for scheduling router to a default L3 agent")

    neutron_server_2013_2_1.param(
        'loadbalancer_pool_scheduler_driver', type='string', default='neutron.services.loadbalancer.agent_scheduler.ChanceScheduler',
        description="=========== items for agent scheduler extension ============= Driver to use for scheduling network to DHCP agent Driver to use for scheduling router to a default L3 agent Driver to use for scheduling a loadbalancer pool to an lbaas agent")

    neutron_server_2013_2_1.param(
        'network_auto_schedule', type='string', default='True',
        description="Allow auto scheduling networks to DHCP agent. It will schedule non-hosted networks to first DHCP agent which sends get_active_networks message to neutron server")

    neutron_server_2013_2_1.param(
        'router_auto_schedule', type='string', default='True',
        description="Allow auto scheduling routers to L3 agent. It will schedule non-hosted routers to first L3 agent which sends sync_routers message to neutron server")

    neutron_server_2013_2_1.param(
        'dhcp_agents_per_network', type='string', default='1',
        description="Number of DHCP agents scheduled to host a network. This enables redundant DHCP agents for configured networks.")

    neutron_server_2013_2_1.param(
        'tcp_keepidle', type='string', default='600',
        description="=========== WSGI parameters related to the API server ============== Sets the value of TCP_KEEPIDLE in seconds to use for each server socket when starting API server. Not supported on OS X.")

    neutron_server_2013_2_1.param(
        'retry_until_window', type='string', default='30', description="Number of seconds to keep retrying to listen")

    neutron_server_2013_2_1.param('backlog', type='string', default='4096',
                                     description="Number of backlog requests to configure the socket with.")

    neutron_server_2013_2_1.param(
        'use_ssl', type='string', default='False', description="Enable SSL on the API server")

    neutron_server_2013_2_1.param(
        'ssl_cert_file', type='string', default='/path/to/certfile',
        description="Certificate file to use when starting API server securely")

    neutron_server_2013_2_1.param(
        'ssl_key_file', type='string', default='/path/to/keyfile',
        description="Private key file to use when starting API server securely")

    neutron_server_2013_2_1.param(
        'ssl_ca_file', type='string', default='/path/to/cafile',
        description="CA certificate file to use when starting API server securely to verify connecting clients. This is an optional parameter only required if API clients need to authenticate to the API server using SSL certificates signed by a trusted CA")

    neutron_server_2013_2_1.section('quotas')

    neutron_server_2013_2_1.param(
        'quota_items', type='string', default='network,subnet,port', description="resource name(s) that are supported in quota features")

    neutron_server_2013_2_1.param(
        'default_quota', type='string', default='-1',
        description="default number of resource allowed per tenant, minus for unlimited")

    neutron_server_2013_2_1.param(
        'quota_network', type='string', default='10',
        description="number of networks allowed per tenant, and minus means unlimited")

    neutron_server_2013_2_1.param(
        'quota_subnet', type='string', default='10',
        description="number of subnets allowed per tenant, and minus means unlimited")

    neutron_server_2013_2_1.param('quota_port', type='string', default='50',
                                     description="number of ports allowed per tenant, and minus means unlimited")

    neutron_server_2013_2_1.param(
        'quota_security_group', type='string', default='10',
        description="number of security groups allowed per tenant, and minus means unlimited")

    neutron_server_2013_2_1.param(
        'quota_security_group_rule', type='string', default='100',
        description="number of security group rules allowed per tenant, and minus means unlimited")

    neutron_server_2013_2_1.param(
        'quota_driver', type='string', default='neutron.db.quota_db.DbQuotaDriver', description="default driver to use for quota checks")

    neutron_server_2013_2_1.section('agent')

    neutron_server_2013_2_1.param(
        'root_helper', type='string', default='sudo',
        description="Use 'sudo neutron-rootwrap /etc/neutron/rootwrap.conf' to use the real root filter facility. Change to 'sudo' to skip the filtering and just run the comand directly")

    neutron_server_2013_2_1.param(
        'report_interval', type='string', default='4',
        description="=========== items for agent management extension ============= seconds between nodes reporting state to server, should be less than agent_down_time")

    neutron_server_2013_2_1.section('keystone_authtoken')

    neutron_server_2013_2_1.param(
        'auth_host', type='host', default='127.0.0.1')

    neutron_server_2013_2_1.param(
        'auth_port', type='string', default='35357')

    neutron_server_2013_2_1.param(
        'auth_protocol', type='string', default='http')

    neutron_server_2013_2_1.param(
        'admin_tenant_name', type='string', default='%SERVICE_TENANT_NAME%')

    neutron_server_2013_2_1.param(
        'admin_user', type='string', default='%SERVICE_USER%')

    neutron_server_2013_2_1.param(
        'admin_password', type='string', default='%SERVICE_PASSWORD%')

    neutron_server_2013_2_1.param(
        'signing_dir', type='string', default='$state_path/keystone-signing')

    neutron_server_2013_2_1.section('database')

    neutron_server_2013_2_1.param(
        'connection', type='string', default='mysql://root:pass@127.0.0.1:3306/neutron',
        description="This line MUST be changed to actually run the plugin. Example:")

    neutron_server_2013_2_1.param(
        'slave_connection', type='string', default='',
        description="The SQLAlchemy connection string used to connect to the slave database")

    neutron_server_2013_2_1.param(
        'max_retries', type='string', default='10',
        description="Database reconnection retry times - in event connectivity is lost set to -1 implies an infinite retry count")

    neutron_server_2013_2_1.param(
        'retry_interval', type='string', default='10',
        description="Database reconnection interval in seconds - if the initial connection to the database fails")

    neutron_server_2013_2_1.param(
        'min_pool_size', type='string', default='1',
        description="Minimum number of SQL connections to keep open in a pool")

    neutron_server_2013_2_1.param(
        'max_pool_size', type='string', default='10',
        description="Maximum number of SQL connections to keep open in a pool")

    neutron_server_2013_2_1.param(
        'idle_timeout', type='string', default='3600',
        description="Timeout in seconds before idle sql connections are reaped")

    neutron_server_2013_2_1.param(
        'max_overflow', type='string', default='20',
        description="If set, use this value for max_overflow with sqlalchemy")

    neutron_server_2013_2_1.param(
        'connection_debug', type='string', default='0',
        description="Verbosity of SQL debugging information. 0=None, 100=Everything")

    neutron_server_2013_2_1.param(
        'connection_trace', type='string', default='False', description="Add python stack traces to SQL as comment strings")

    neutron_server_2013_2_1.param(
        'pool_timeout', type='string', default='10',
        description="If set, use this value for pool_timeout with sqlalchemy")

    neutron_server_2013_2_1.section('service_providers')

    neutron_server_2013_2_1.param(
        'service_provider', type='string', default='LOADBALANCER:Haproxy:neutron.services.loadbalancer.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default',
        description="Specify service providers (drivers) for advanced services like loadbalancer, VPN, Firewall. Must be in form: service_provider=<service_type>:<name>:<driver>[:default] List of allowed service type include LOADBALANCER, FIREWALL, VPN Combination of <service type> and <name> must be unique; <driver> must also be unique this is multiline option, example for default provider: service_provider=LOADBALANCER:name:lbaas_plugin_driver_path:default example of non-default provider: service_provider=FIREWALL:name2:firewall_driver_path --- Reference implementations ---")
