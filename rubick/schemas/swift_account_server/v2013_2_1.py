from rubick.schema import ConfigSchemaRegistry

swift_account_server = ConfigSchemaRegistry.register_schema(
    project='swift_account_server')

with swift_account_server.version('2013.2.1') as swift_account_server_2013_2_1:

    swift_account_server_2013_2_1.section('DEFAULT')

    swift_account_server_2013_2_1.param(
        'bind_ip', type='string', default='0.0.0.0')

    swift_account_server_2013_2_1.param(
        'bind_port', type='string', default='6002')

    swift_account_server_2013_2_1.param(
        'bind_timeout', type='string', default='30')

    swift_account_server_2013_2_1.param(
        'backlog', type='string', default='4096')

    swift_account_server_2013_2_1.param('user', type='string', default='swift')

    swift_account_server_2013_2_1.param(
        'swift_dir', type='string', default='/etc/swift')

    swift_account_server_2013_2_1.param(
        'devices', type='string', default='/srv/node')

    swift_account_server_2013_2_1.param(
        'mount_check', type='string', default='true')

    swift_account_server_2013_2_1.param(
        'disable_fallocate', type='string', default='false')

    swift_account_server_2013_2_1.param(
        'workers', type='string', default='auto',
        description="Use an integer to override the number of pre-forked processes that will accept connections.")

    swift_account_server_2013_2_1.param(
        'max_clients', type='string', default='1024', description="Maximum concurrent requests per worker")

    swift_account_server_2013_2_1.param(
        'log_name', type='string', default='swift', description="You can specify default log routing here if you want:")

    swift_account_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0', description="You can specify default log routing here if you want:")

    swift_account_server_2013_2_1.param(
        'log_level', type='string', default='INFO', description="You can specify default log routing here if you want:")

    swift_account_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log', description="You can specify default log routing here if you want:")

    swift_account_server_2013_2_1.param(
        'log_custom_handlers', type='string', default='',
        description="comma separated list of functions to call to setup custom log handlers. functions get passed: conf, name, log_to_console, log_route, fmt, logger, adapted_logger")

    swift_account_server_2013_2_1.param(
        'log_udp_host', type='string', default='', description="If set, log_udp_host will override log_address")

    swift_account_server_2013_2_1.param(
        'log_udp_port', type='string', default='514', description="If set, log_udp_host will override log_address")

    swift_account_server_2013_2_1.param(
        'log_statsd_host', type='host', default='localhost', description="You can enable StatsD logging here:")

    swift_account_server_2013_2_1.param(
        'log_statsd_port', type='string', default='8125', description="You can enable StatsD logging here:")

    swift_account_server_2013_2_1.param(
        'log_statsd_default_sample_rate', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_account_server_2013_2_1.param(
        'log_statsd_sample_rate_factor', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_account_server_2013_2_1.param(
        'log_statsd_metric_prefix', type='string', default='', description="You can enable StatsD logging here:")

    swift_account_server_2013_2_1.param(
        'db_preallocation', type='string', default='off',
        description="If you don't mind the extra disk space usage in overhead, you can turn this on to preallocate disk space with SQLite databases to decrease fragmentation.")

    swift_account_server_2013_2_1.param(
        'eventlet_debug', type='string', default='false')

    swift_account_server_2013_2_1.param(
        'fallocate_reserve', type='string', default='0',
        description="You can set fallocate_reserve to the number of bytes you'd like fallocate to reserve, whether there is space for the given file size or not.")

    swift_account_server_2013_2_1.section('pipeline:main')

    swift_account_server_2013_2_1.param(
        'pipeline', type='string', default='healthcheck recon account-server')

    swift_account_server_2013_2_1.section('app:account-server')

    swift_account_server_2013_2_1.param(
        'use', type='string', default='egg:swift#account')

    swift_account_server_2013_2_1.param(
        'set log_name', type='string', default='account-server', description="You can override the default log routing for this app here:")

    swift_account_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0', description="You can override the default log routing for this app here:")

    swift_account_server_2013_2_1.param(
        'set log_level', type='string', default='INFO', description="You can override the default log routing for this app here:")

    swift_account_server_2013_2_1.param(
        'set log_requests', type='string', default='true', description="You can override the default log routing for this app here:")

    swift_account_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log', description="You can override the default log routing for this app here:")

    swift_account_server_2013_2_1.param(
        'auto_create_account_prefix', type='string', default='.')

    swift_account_server_2013_2_1.param(
        'replication_server', type='string', default='false',
        description="Configure parameter for creating specific server To handle all verbs, including replication verbs, do not specify 'replication_server' (this is the default). To only handle replication, set to a True value (e.g. 'True' or '1'). To handle only non-replication verbs, set to 'False'. Unless you have a separate replication network, you should not specify any value for 'replication_server'.")

    swift_account_server_2013_2_1.section('filter:healthcheck')

    swift_account_server_2013_2_1.param(
        'use', type='string', default='egg:swift#healthcheck')

    swift_account_server_2013_2_1.param(
        'disable_path', type='string', default='',
        description="An optional filesystem path, which if present, will cause the healthcheck URL to return '503 Service Unavailable' with a body of 'DISABLED BY FILE'")

    swift_account_server_2013_2_1.section('filter:recon')

    swift_account_server_2013_2_1.param(
        'use', type='string', default='egg:swift#recon')

    swift_account_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_account_server_2013_2_1.section('account-replicator')

    swift_account_server_2013_2_1.param(
        'log_name', type='string', default='account-replicator',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'vm_test_mode', type='string', default='no')

    swift_account_server_2013_2_1.param(
        'per_diff', type='string', default='1000')

    swift_account_server_2013_2_1.param(
        'max_diffs', type='string', default='100')

    swift_account_server_2013_2_1.param(
        'concurrency', type='string', default='8')

    swift_account_server_2013_2_1.param(
        'interval', type='string', default='30')

    swift_account_server_2013_2_1.param(
        'error_suppression_interval', type='string', default='60',
        description="How long without an error before a node's error count is reset. This will also be how long before a node is reenabled after suppression is triggered.")

    swift_account_server_2013_2_1.param(
        'error_suppression_limit', type='string', default='10',
        description="How many errors can accumulate before a node is temporarily ignored.")

    swift_account_server_2013_2_1.param(
        'node_timeout', type='string', default='10')

    swift_account_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_account_server_2013_2_1.param(
        'reclaim_age', type='string', default='604800', description="The replicator also performs reclamation")

    swift_account_server_2013_2_1.param(
        'run_pause', type='string', default='30', description="Time in seconds to wait between replication passes")

    swift_account_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_account_server_2013_2_1.section('account-auditor')

    swift_account_server_2013_2_1.param(
        'log_name', type='string', default='account-auditor',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'interval', type='string', default='1800', description="Will audit each account at most once per interval")

    swift_account_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0')

    swift_account_server_2013_2_1.param(
        'log_level', type='string', default='INFO')

    swift_account_server_2013_2_1.param(
        'accounts_per_second', type='string', default='200')

    swift_account_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_account_server_2013_2_1.section('account-reaper')

    swift_account_server_2013_2_1.param(
        'log_name', type='string', default='account-reaper',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_account_server_2013_2_1.param(
        'concurrency', type='string', default='25')

    swift_account_server_2013_2_1.param(
        'interval', type='string', default='3600')

    swift_account_server_2013_2_1.param(
        'node_timeout', type='string', default='10')

    swift_account_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_account_server_2013_2_1.param(
        'delay_reaping', type='string', default='0',
        description="Normally, the reaper begins deleting account information for deleted accounts immediately; you can set this to delay its work however. The value is in seconds; 2592000 = 30 days for example.")

    swift_account_server_2013_2_1.param(
        'reap_warn_after', type='string', default='2592000',
        description="If the account fails to be be reaped due to a persistent error, the account reaper will log a message such as: Account <name> has not been reaped since <date> You can search logs for this message if space is not being reclaimed after you delete account(s). Default is 2592000 seconds (30 days). This is in addition to any time requested by delay_reaping.")
