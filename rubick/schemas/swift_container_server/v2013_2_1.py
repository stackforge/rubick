from rubick.schema import ConfigSchemaRegistry

swift_container_server = ConfigSchemaRegistry.register_schema(
    project='swift_container_server')

with swift_container_server.version('2013.2.1') as swift_container_server_2013_2_1:

    swift_container_server_2013_2_1.section('DEFAULT')

    swift_container_server_2013_2_1.param(
        'bind_ip', type='string', default='0.0.0.0')

    swift_container_server_2013_2_1.param(
        'bind_port', type='string', default='6001')

    swift_container_server_2013_2_1.param(
        'bind_timeout', type='string', default='30')

    swift_container_server_2013_2_1.param(
        'backlog', type='string', default='4096')

    swift_container_server_2013_2_1.param(
        'user', type='string', default='swift')

    swift_container_server_2013_2_1.param(
        'swift_dir', type='string', default='/etc/swift')

    swift_container_server_2013_2_1.param(
        'devices', type='string', default='/srv/node')

    swift_container_server_2013_2_1.param(
        'mount_check', type='string', default='true')

    swift_container_server_2013_2_1.param(
        'disable_fallocate', type='string', default='false')

    swift_container_server_2013_2_1.param(
        'workers', type='string', default='auto', description="Use an integer to override the number of pre-forked processes that will accept connections.")

    swift_container_server_2013_2_1.param(
        'max_clients', type='string', default='1024', description="Maximum concurrent requests per worker")

    swift_container_server_2013_2_1.param(
        'allowed_sync_hosts', type='string', default='127.0.0.1',
        description="This is a comma separated list of hosts allowed in the X-Container-Sync-To field for containers.")

    swift_container_server_2013_2_1.param(
        'log_name', type='string', default='swift', description="You can specify default log routing here if you want:")

    swift_container_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0', description="You can specify default log routing here if you want:")

    swift_container_server_2013_2_1.param(
        'log_level', type='string', default='INFO', description="You can specify default log routing here if you want:")

    swift_container_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log', description="You can specify default log routing here if you want:")

    swift_container_server_2013_2_1.param(
        'log_custom_handlers', type='string', default='',
        description="comma separated list of functions to call to setup custom log handlers. functions get passed: conf, name, log_to_console, log_route, fmt, logger, adapted_logger")

    swift_container_server_2013_2_1.param(
        'log_udp_host', type='string', default='', description="If set, log_udp_host will override log_address")

    swift_container_server_2013_2_1.param(
        'log_udp_port', type='string', default='514', description="If set, log_udp_host will override log_address")

    swift_container_server_2013_2_1.param(
        'log_statsd_host', type='host', default='localhost', description="You can enable StatsD logging here:")

    swift_container_server_2013_2_1.param(
        'log_statsd_port', type='string', default='8125', description="You can enable StatsD logging here:")

    swift_container_server_2013_2_1.param(
        'log_statsd_default_sample_rate', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_container_server_2013_2_1.param(
        'log_statsd_sample_rate_factor', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_container_server_2013_2_1.param(
        'log_statsd_metric_prefix', type='string', default='', description="You can enable StatsD logging here:")

    swift_container_server_2013_2_1.param(
        'db_preallocation', type='string', default='off',
        description="If you don't mind the extra disk space usage in overhead, you can turn this on to preallocate disk space with SQLite databases to decrease fragmentation.")

    swift_container_server_2013_2_1.param(
        'eventlet_debug', type='string', default='false')

    swift_container_server_2013_2_1.param(
        'fallocate_reserve', type='string', default='0',
        description="You can set fallocate_reserve to the number of bytes you'd like fallocate to reserve, whether there is space for the given file size or not.")

    swift_container_server_2013_2_1.section('pipeline:main')

    swift_container_server_2013_2_1.param(
        'pipeline', type='string', default='healthcheck recon container-server')

    swift_container_server_2013_2_1.section('app:container-server')

    swift_container_server_2013_2_1.param(
        'use', type='string', default='egg:swift#container')

    swift_container_server_2013_2_1.param(
        'set log_name', type='string', default='container-server', description="You can override the default log routing for this app here:")

    swift_container_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0', description="You can override the default log routing for this app here:")

    swift_container_server_2013_2_1.param(
        'set log_level', type='string', default='INFO', description="You can override the default log routing for this app here:")

    swift_container_server_2013_2_1.param(
        'set log_requests', type='string', default='true', description="You can override the default log routing for this app here:")

    swift_container_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log', description="You can override the default log routing for this app here:")

    swift_container_server_2013_2_1.param(
        'node_timeout', type='string', default='3')

    swift_container_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_container_server_2013_2_1.param(
        'allow_versions', type='string', default='false')

    swift_container_server_2013_2_1.param(
        'auto_create_account_prefix', type='string', default='.')

    swift_container_server_2013_2_1.param(
        'replication_server', type='string', default='false',
        description="Configure parameter for creating specific server To handle all verbs, including replication verbs, do not specify 'replication_server' (this is the default). To only handle replication, set to a True value (e.g. 'True' or '1'). To handle only non-replication verbs, set to 'False'. Unless you have a separate replication network, you should not specify any value for 'replication_server'.")

    swift_container_server_2013_2_1.section('filter:healthcheck')

    swift_container_server_2013_2_1.param(
        'use', type='string', default='egg:swift#healthcheck')

    swift_container_server_2013_2_1.param(
        'disable_path', type='string', default='',
        description="An optional filesystem path, which if present, will cause the healthcheck URL to return '503 Service Unavailable' with a body of 'DISABLED BY FILE'")

    swift_container_server_2013_2_1.section('filter:recon')

    swift_container_server_2013_2_1.param(
        'use', type='string', default='egg:swift#recon')

    swift_container_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_container_server_2013_2_1.section('container-replicator')

    swift_container_server_2013_2_1.param(
        'log_name', type='string', default='container-replicator',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'vm_test_mode', type='string', default='no')

    swift_container_server_2013_2_1.param(
        'per_diff', type='string', default='1000')

    swift_container_server_2013_2_1.param(
        'max_diffs', type='string', default='100')

    swift_container_server_2013_2_1.param(
        'concurrency', type='string', default='8')

    swift_container_server_2013_2_1.param(
        'interval', type='string', default='30')

    swift_container_server_2013_2_1.param(
        'node_timeout', type='string', default='10')

    swift_container_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_container_server_2013_2_1.param(
        'reclaim_age', type='string', default='604800', description="The replicator also performs reclamation")

    swift_container_server_2013_2_1.param(
        'run_pause', type='string', default='30', description="Time in seconds to wait between replication passes")

    swift_container_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_container_server_2013_2_1.section('container-updater')

    swift_container_server_2013_2_1.param(
        'log_name', type='string', default='container-updater',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'interval', type='string', default='300')

    swift_container_server_2013_2_1.param(
        'concurrency', type='string', default='4')

    swift_container_server_2013_2_1.param(
        'node_timeout', type='string', default='3')

    swift_container_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_container_server_2013_2_1.param(
        'slowdown', type='string', default='0.01', description="slowdown will sleep that amount between containers")

    swift_container_server_2013_2_1.param(
        'account_suppression_time', type='string', default='60',
        description="Seconds to suppress updating an account that has generated an error")

    swift_container_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_container_server_2013_2_1.section('container-auditor')

    swift_container_server_2013_2_1.param(
        'log_name', type='string', default='container-auditor',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'interval', type='string', default='1800', description="Will audit each container at most once per interval")

    swift_container_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift', description="containers_per_second = 200")

    swift_container_server_2013_2_1.section('container-sync')

    swift_container_server_2013_2_1.param(
        'log_name', type='string', default='container-sync',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_container_server_2013_2_1.param(
        'sync_proxy', type='string', default='http://127.0.0.1:8888',
        description="If you need to use an HTTP Proxy, set it here; defaults to no proxy.")

    swift_container_server_2013_2_1.param(
        'interval', type='string', default='300', description="Will sync each container at most once per interval")

    swift_container_server_2013_2_1.param(
        'container_time', type='string', default='60', description="Maximum amount of time to spend syncing each container per pass")
