from rubick.schema import ConfigSchemaRegistry

swift_object_server = ConfigSchemaRegistry.register_schema(
    project='swift_object_server')

with swift_object_server.version('2013.2.1') as swift_object_server_2013_2_1:

    swift_object_server_2013_2_1.section('DEFAULT')

    swift_object_server_2013_2_1.param(
        'bind_ip', type='string', default='0.0.0.0')

    swift_object_server_2013_2_1.param(
        'bind_port', type='string', default='6000')

    swift_object_server_2013_2_1.param(
        'bind_timeout', type='string', default='30')

    swift_object_server_2013_2_1.param(
        'backlog', type='string', default='4096')

    swift_object_server_2013_2_1.param('user', type='string', default='swift')

    swift_object_server_2013_2_1.param(
        'swift_dir', type='string', default='/etc/swift')

    swift_object_server_2013_2_1.param(
        'devices', type='string', default='/srv/node')

    swift_object_server_2013_2_1.param(
        'mount_check', type='string', default='true')

    swift_object_server_2013_2_1.param(
        'disable_fallocate', type='string', default='false')

    swift_object_server_2013_2_1.param(
        'expiring_objects_container_divisor', type='string', default='86400')

    swift_object_server_2013_2_1.param(
        'workers', type='string', default='auto',
        description="Use an integer to override the number of pre-forked processes that will accept connections.")

    swift_object_server_2013_2_1.param(
        'max_clients', type='string', default='1024', description="Maximum concurrent requests per worker")

    swift_object_server_2013_2_1.param(
        'log_name', type='string', default='swift', description="You can specify default log routing here if you want:")

    swift_object_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0', description="You can specify default log routing here if you want:")

    swift_object_server_2013_2_1.param(
        'log_level', type='string', default='INFO', description="You can specify default log routing here if you want:")

    swift_object_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log', description="You can specify default log routing here if you want:")

    swift_object_server_2013_2_1.param(
        'log_custom_handlers', type='string', default='',
        description="comma separated list of functions to call to setup custom log handlers. functions get passed: conf, name, log_to_console, log_route, fmt, logger, adapted_logger")

    swift_object_server_2013_2_1.param(
        'log_udp_host', type='string', default='', description="If set, log_udp_host will override log_address")

    swift_object_server_2013_2_1.param(
        'log_udp_port', type='string', default='514', description="If set, log_udp_host will override log_address")

    swift_object_server_2013_2_1.param(
        'log_statsd_host', type='host', default='localhost', description="You can enable StatsD logging here:")

    swift_object_server_2013_2_1.param(
        'log_statsd_port', type='string', default='8125', description="You can enable StatsD logging here:")

    swift_object_server_2013_2_1.param(
        'log_statsd_default_sample_rate', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_object_server_2013_2_1.param(
        'log_statsd_sample_rate_factor', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_object_server_2013_2_1.param(
        'log_statsd_metric_prefix', type='string', default='', description="You can enable StatsD logging here:")

    swift_object_server_2013_2_1.param(
        'eventlet_debug', type='string', default='false')

    swift_object_server_2013_2_1.param(
        'fallocate_reserve', type='string', default='0',
        description="You can set fallocate_reserve to the number of bytes you'd like fallocate to reserve, whether there is space for the given file size or not.")

    swift_object_server_2013_2_1.section('pipeline:main')

    swift_object_server_2013_2_1.param(
        'pipeline', type='string', default='healthcheck recon object-server')

    swift_object_server_2013_2_1.section('app:object-server')

    swift_object_server_2013_2_1.param(
        'use', type='string', default='egg:swift#object')

    swift_object_server_2013_2_1.param(
        'set log_name', type='string', default='object-server',
        description="You can override the default log routing for this app here:")

    swift_object_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here:")

    swift_object_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here:")

    swift_object_server_2013_2_1.param(
        'set log_requests', type='string', default='true',
        description="You can override the default log routing for this app here:")

    swift_object_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here:")

    swift_object_server_2013_2_1.param(
        'node_timeout', type='string', default='3')

    swift_object_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_object_server_2013_2_1.param(
        'network_chunk_size', type='string', default='65536')

    swift_object_server_2013_2_1.param(
        'disk_chunk_size', type='string', default='65536')

    swift_object_server_2013_2_1.param(
        'max_upload_time', type='string', default='86400')

    swift_object_server_2013_2_1.param('slow', type='string', default='0')

    swift_object_server_2013_2_1.param(
        'keep_cache_size', type='string', default='5424880',
        description="Objects smaller than this are not evicted from the buffercache once read")

    swift_object_server_2013_2_1.param(
        'keep_cache_private', type='string', default='false',
        description="If true, objects for authenticated GET requests may be kept in buffer cache if small enough")

    swift_object_server_2013_2_1.param(
        'mb_per_sync', type='string', default='512', description="on PUTs, sync data every n MB")

    swift_object_server_2013_2_1.param(
        'allowed_headers', type='string', default='Content-Disposition, Content-Encoding, X-Delete-At, X-Object-Manifest, X-Static-Large-Object',
        description="Comma separated list of headers that can be set in metadata on an object. This list is in addition to X-Object-Meta-* headers and cannot include Content-Type, etag, Content-Length, or deleted")

    swift_object_server_2013_2_1.param(
        'auto_create_account_prefix', type='string', default='.')

    swift_object_server_2013_2_1.param(
        'replication_server', type='string', default='false',
        description="Configure parameter for creating specific server To handle all verbs, including replication verbs, do not specify 'replication_server' (this is the default). To only handle replication, set to a True value (e.g. 'True' or '1'). To handle only non-replication verbs, set to 'False'. Unless you have a separate replication network, you should not specify any value for 'replication_server'.")

    swift_object_server_2013_2_1.param(
        'threads_per_disk', type='string', default='0',
        description="Configure parameter for creating specific server To handle all verbs, including replication verbs, do not specify 'replication_server' (this is the default). To only handle replication, set to a True value (e.g. 'True' or '1'). To handle only non-replication verbs, set to 'False'. Unless you have a separate replication network, you should not specify any value for 'replication_server'. A value of 0 means 'don't use thread pools'. A reasonable starting point is 4.")

    swift_object_server_2013_2_1.section('filter:healthcheck')

    swift_object_server_2013_2_1.param(
        'use', type='string', default='egg:swift#healthcheck')

    swift_object_server_2013_2_1.param(
        'disable_path', type='string', default='',
        description="An optional filesystem path, which if present, will cause the healthcheck URL to return '503 Service Unavailable' with a body of 'DISABLED BY FILE'")

    swift_object_server_2013_2_1.section('filter:recon')

    swift_object_server_2013_2_1.param(
        'use', type='string', default='egg:swift#recon')

    swift_object_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_object_server_2013_2_1.param(
        'recon_lock_path', type='string', default='/var/lock')

    swift_object_server_2013_2_1.section('object-replicator')

    swift_object_server_2013_2_1.param(
        'log_name', type='string', default='object-replicator',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'vm_test_mode', type='string', default='no')

    swift_object_server_2013_2_1.param(
        'daemonize', type='string', default='on')

    swift_object_server_2013_2_1.param(
        'run_pause', type='string', default='30')

    swift_object_server_2013_2_1.param(
        'concurrency', type='string', default='1')

    swift_object_server_2013_2_1.param(
        'stats_interval', type='string', default='300')

    swift_object_server_2013_2_1.param(
        'rsync_timeout', type='string', default='900', description="max duration of a partition rsync")

    swift_object_server_2013_2_1.param(
        'rsync_bwlimit', type='string', default='0', description="bandwith limit for rsync in kB/s. 0 means unlimited")

    swift_object_server_2013_2_1.param(
        'rsync_io_timeout', type='string', default='30', description="passed to rsync for io op timeout")

    swift_object_server_2013_2_1.param(
        'http_timeout', type='string', default='60', description="max duration of an http request")

    swift_object_server_2013_2_1.param(
        'lockup_timeout', type='string', default='1800',
        description="attempts to kill all workers if nothing replicates for lockup_timeout seconds")

    swift_object_server_2013_2_1.param(
        'reclaim_age', type='string', default='604800', description="The replicator also performs reclamation")

    swift_object_server_2013_2_1.param(
        'ring_check_interval', type='string', default='15')

    swift_object_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_object_server_2013_2_1.param(
        'rsync_error_log_line_length', type='string', default='0',
        description="limits how long rsync error log lines are 0 means to log the entire line")

    swift_object_server_2013_2_1.section('object-updater')

    swift_object_server_2013_2_1.param(
        'log_name', type='string', default='object-updater',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'interval', type='string', default='300')

    swift_object_server_2013_2_1.param(
        'concurrency', type='string', default='1')

    swift_object_server_2013_2_1.param(
        'node_timeout', type='string', default='10')

    swift_object_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_object_server_2013_2_1.param(
        'slowdown', type='string', default='0.01', description="slowdown will sleep that amount between objects")

    swift_object_server_2013_2_1.section('object-auditor')

    swift_object_server_2013_2_1.param(
        'log_name', type='string', default='object-auditor',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here (don't use set!):")

    swift_object_server_2013_2_1.param(
        'files_per_second', type='string', default='20')

    swift_object_server_2013_2_1.param(
        'bytes_per_second', type='string', default='10000000')

    swift_object_server_2013_2_1.param(
        'log_time', type='string', default='3600')

    swift_object_server_2013_2_1.param(
        'zero_byte_files_per_second', type='string', default='50')

    swift_object_server_2013_2_1.param(
        'recon_cache_path', type='string', default='/var/cache/swift')

    swift_object_server_2013_2_1.param(
        'object_size_stats', type='string', default='',
        description="Takes a comma separated list of ints. If set, the object auditor will increment a counter for every object whose size is <= to the given break points and report the result after a full scan.")
