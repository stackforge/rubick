from rubick.schema import ConfigSchemaRegistry

swift_proxy_server = ConfigSchemaRegistry.register_schema(
    project='swift_proxy_server')

with swift_proxy_server.version('2013.2.1') as swift_proxy_server_2013_2_1:

    swift_proxy_server_2013_2_1.section('DEFAULT')

    swift_proxy_server_2013_2_1.param(
        'bind_ip', type='string', default='0.0.0.0')

    swift_proxy_server_2013_2_1.param('bind_port', type='string', default='80')

    swift_proxy_server_2013_2_1.param(
        'bind_timeout', type='string', default='30')

    swift_proxy_server_2013_2_1.param('backlog', type='string', default='4096')

    swift_proxy_server_2013_2_1.param(
        'swift_dir', type='string', default='/etc/swift')

    swift_proxy_server_2013_2_1.param('user', type='string', default='swift')

    swift_proxy_server_2013_2_1.param('workers', type='string', default='auto',
                                      description="Use an integer to override the number of pre-forked processes that will accept connections.  Should default to the number of effective cpu cores in the system.  It's worth noting that individual workers will use many eventlet co-routines to service multiple concurrent requests.")

    swift_proxy_server_2013_2_1.param(
        'max_clients', type='string', default='1024', description="Maximum concurrent requests per worker")

    swift_proxy_server_2013_2_1.param(
        'cert_file', type='string', default='/etc/swift/proxy.crt',
        description="Set the following two lines to enable SSL. This is for testing only.")

    swift_proxy_server_2013_2_1.param(
        'key_file', type='string', default='/etc/swift/proxy.key',
        description="Set the following two lines to enable SSL. This is for testing only.")

    swift_proxy_server_2013_2_1.param(
        'log_name', type='string', default='swift', description="You can specify default log routing here if you want:")

    swift_proxy_server_2013_2_1.param(
        'log_facility', type='string', default='LOG_LOCAL0', description="You can specify default log routing here if you want:")

    swift_proxy_server_2013_2_1.param(
        'log_level', type='string', default='INFO', description="You can specify default log routing here if you want:")

    swift_proxy_server_2013_2_1.param(
        'log_headers', type='string', default='false', description="You can specify default log routing here if you want:")

    swift_proxy_server_2013_2_1.param(
        'log_address', type='string', default='/dev/log', description="You can specify default log routing here if you want:")

    swift_proxy_server_2013_2_1.param(
        'trans_id_suffix', type='string', default='',
        description="This optional suffix (default is empty) that would be appended to the swift transaction id allows one to easily figure out from which cluster that X-Trans-Id belongs to. This is very useful when one is managing more than one swift cluster.")

    swift_proxy_server_2013_2_1.param(
        'log_custom_handlers', type='string', default='',
        description="comma separated list of functions to call to setup custom log handlers. functions get passed: conf, name, log_to_console, log_route, fmt, logger, adapted_logger")

    swift_proxy_server_2013_2_1.param(
        'log_udp_host', type='string', default='', description="If set, log_udp_host will override log_address")

    swift_proxy_server_2013_2_1.param(
        'log_udp_port', type='string', default='514', description="If set, log_udp_host will override log_address")

    swift_proxy_server_2013_2_1.param(
        'log_statsd_host', type='host', default='localhost', description="You can enable StatsD logging here:")

    swift_proxy_server_2013_2_1.param(
        'log_statsd_port', type='string', default='8125', description="You can enable StatsD logging here:")

    swift_proxy_server_2013_2_1.param(
        'log_statsd_default_sample_rate', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_proxy_server_2013_2_1.param(
        'log_statsd_sample_rate_factor', type='string', default='1.0', description="You can enable StatsD logging here:")

    swift_proxy_server_2013_2_1.param(
        'log_statsd_metric_prefix', type='string', default='', description="You can enable StatsD logging here:")

    swift_proxy_server_2013_2_1.param(
        'cors_allow_origin', type='string', default='',
        description="Use a comma separated list of full url (http://foo.bar:1234,https://foo.bar)")

    swift_proxy_server_2013_2_1.param(
        'client_timeout', type='string', default='60')

    swift_proxy_server_2013_2_1.param(
        'eventlet_debug', type='string', default='false')

    swift_proxy_server_2013_2_1.section('pipeline:main')

    swift_proxy_server_2013_2_1.param(
        'pipeline', type='string', default='catch_errors healthcheck proxy-logging cache bulk slo ratelimit tempauth container-quotas account-quotas proxy-logging proxy-server')

    swift_proxy_server_2013_2_1.section('app:proxy-server')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#proxy')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='proxy-server',
        description="You can override the default log routing for this app here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this app here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this app here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this app here:")

    swift_proxy_server_2013_2_1.param(
        'log_handoffs', type='string', default='true')

    swift_proxy_server_2013_2_1.param(
        'recheck_account_existence', type='string', default='60')

    swift_proxy_server_2013_2_1.param(
        'recheck_container_existence', type='string', default='60')

    swift_proxy_server_2013_2_1.param(
        'object_chunk_size', type='string', default='8192')

    swift_proxy_server_2013_2_1.param(
        'client_chunk_size', type='string', default='8192')

    swift_proxy_server_2013_2_1.param(
        'node_timeout', type='string', default='10')

    swift_proxy_server_2013_2_1.param(
        'conn_timeout', type='string', default='0.5')

    swift_proxy_server_2013_2_1.param(
        'error_suppression_interval', type='string', default='60',
        description="How long without an error before a node's error count is reset. This will also be how long before a node is reenabled after suppression is triggered.")

    swift_proxy_server_2013_2_1.param(
        'error_suppression_limit', type='string', default='10',
        description="How many errors can accumulate before a node is temporarily ignored.")

    swift_proxy_server_2013_2_1.param(
        'allow_account_management', type='string', default='false',
        description="If set to 'true' any authorized user may create and delete accounts; if 'false' no one, even authorized, can.")

    swift_proxy_server_2013_2_1.param(
        'object_post_as_copy', type='string', default='true',
        description="Set object_post_as_copy = false to turn on fast posts where only the metadata changes are stored anew and the original data file is kept in place. This makes for quicker posts; but since the container metadata isn't updated in this mode, features like container sync won't be able to sync posts.")

    swift_proxy_server_2013_2_1.param(
        'account_autocreate', type='string', default='false',
        description="If set to 'true' authorized accounts that do not yet exist within the Swift cluster will be automatically created.")

    swift_proxy_server_2013_2_1.param(
        'max_containers_per_account', type='string', default='0',
        description="If set to a positive value, trying to create a container when the account already has at least this maximum containers will result in a 403 Forbidden. Note: This is a soft limit, meaning a user might exceed the cap for recheck_account_existence before the 403s kick in.")

    swift_proxy_server_2013_2_1.param(
        'max_containers_whitelist', type='string', default='',
        description="This is a comma separated list of account hashes that ignore the max_containers_per_account cap.")

    swift_proxy_server_2013_2_1.param(
        'deny_host_headers', type='string', default='',
        description="Comma separated list of Host headers to which the proxy will deny requests.")

    swift_proxy_server_2013_2_1.param(
        'auto_create_account_prefix', type='string',
        default='.', description="Prefix used when automatically creating accounts.")

    swift_proxy_server_2013_2_1.param(
        'put_queue_depth', type='string', default='10', description="Depth of the proxy put queue.")

    swift_proxy_server_2013_2_1.param(
        'rate_limit_after_segment', type='string', default='10',
        description="Start rate-limiting object segment serving after the Nth segment of a segmented object.")

    swift_proxy_server_2013_2_1.param(
        'rate_limit_segments_per_sec', type='string', default='1',
        description="Once segment rate-limiting kicks in for an object, limit segments served to N per second.")

    swift_proxy_server_2013_2_1.param(
        'sorting_method', type='string', default='shuffle',
        description="Storage nodes can be chosen at random (shuffle), by using timing measurements (timing), or by using an explicit match (affinity). Using timing measurements may allow for lower overall latency, while using affinity allows for finer control. In both the timing and affinity cases, equally-sorting nodes are still randomly chosen to spread load. The valid values for sorting_method are 'affinity', 'shuffle', and 'timing'.")

    swift_proxy_server_2013_2_1.param(
        'timing_expiry', type='string', default='300',
        description="If the 'timing' sorting_method is used, the timings will only be valid for the number of seconds configured by timing_expiry.")

    swift_proxy_server_2013_2_1.param(
        'allow_static_large_object', type='string', default='true',
        description="If set to false will treat objects with X-Static-Large-Object header set as a regular object on GETs, i.e. will return that object's contents. Should be set to false if slo is not used in pipeline.")

    swift_proxy_server_2013_2_1.param(
        'max_large_object_get_time', type='string', default='86400',
        description="The maximum time (seconds) that a large object connection is allowed to last.")

    swift_proxy_server_2013_2_1.param(
        'request_node_count', type='string', default='2 * replicas',
        description="Set to the number of nodes to contact for a normal request. You can use '* replicas' at the end to have it use the number given times the number of replicas for the ring being used for the request.")

    swift_proxy_server_2013_2_1.param(
        'read_affinity', type='string', default='',
        description="Example: first read from region 1 zone 1, then region 1 zone 2, then anything in region 2, then everything else: read_affinity = r1z1=100, r1z2=200, r2=300 Default is empty, meaning no preference.")

    swift_proxy_server_2013_2_1.param(
        'write_affinity', type='string', default='',
        description="Example: try to write to regions 1 and 2 before writing to any other nodes: write_affinity = r1, r2 Default is empty, meaning no preference.")

    swift_proxy_server_2013_2_1.param(
        'write_affinity_node_count', type='string', default='2 * replicas',
        description="The number of local (as governed by the write_affinity setting) nodes to attempt to contact first, before any non-local ones. You can use '* replicas' at the end to have it use the number given times the number of replicas for the ring being used for the request.")

    swift_proxy_server_2013_2_1.param(
        'swift_owner_headers', type='string', default='x-container-read, x-container-write, x-container-sync-key, x-container-sync-to, x-account-meta-temp-url-key, x-account-meta-temp-url-key-2',
        description="These are the headers whose values will only be shown to swift_owners. The exact definition of a swift_owner is up to the auth system in use, but usually indicates administrative responsibilities.")

    swift_proxy_server_2013_2_1.section('filter:tempauth')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#tempauth')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='tempauth',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'reseller_prefix', type='string', default='AUTH',
        description="The reseller prefix will verify a token begins with this prefix before even attempting to validate it. Also, with authorization, only Swift storage accounts with this prefix will be authorized by this middleware. Useful if multiple auth systems are in use for one Swift cluster.")

    swift_proxy_server_2013_2_1.param(
        'auth_prefix', type='string', default='/auth/',
        description="The auth prefix will cause requests beginning with this prefix to be routed to the auth subsystem, for granting tokens, etc.")

    swift_proxy_server_2013_2_1.param(
        'token_life', type='string', default='86400',
        description="The auth prefix will cause requests beginning with this prefix to be routed to the auth subsystem, for granting tokens, etc.")

    swift_proxy_server_2013_2_1.param(
        'allow_overrides', type='string', default='true',
        description="This allows middleware higher in the WSGI pipeline to override auth processing, useful for middleware such as tempurl and formpost. If you know you're not going to use such middleware and you want a bit of extra security, you can set this to false.")

    swift_proxy_server_2013_2_1.param(
        'storage_url_scheme', type='string', default='default',
        description="This specifies what scheme to return with storage urls: http, https, or default (chooses based on what the server is running as) This can be useful with an SSL load balancer in front of a non-SSL server.")

    swift_proxy_server_2013_2_1.param(
        'user_admin_admin', type='string', default='admin .admin .reseller_admin',
        description="Lastly, you need to list all the accounts/users you want here. The format is: user_<account>_<user> = <key> [group] [group] [...] [storage_url] or if you want underscores in <account> or <user>, you can base64 encode them (with no equal signs) and use this format: user64_<account_b64>_<user_b64> = <key> [group] [group] [...] [storage_url] There are special groups of: .reseller_admin = can do anything to any account for this auth .admin = can do anything within the account If neither of these groups are specified, the user can only access containers that have been explicitly allowed for them by a .admin or .reseller_admin. The trailing optional storage_url allows you to specify an alternate url to hand back to the user upon authentication. If not specified, this defaults to $HOST/v1/<reseller_prefix>_<account> where $HOST will do its best to resolve to what the requester would need to use to reach this host. Here are example entries, required for running the tests:")

    swift_proxy_server_2013_2_1.param(
        'user_test_tester', type='string', default='testing .admin',
        description="Lastly, you need to list all the accounts/users you want here. The format is: user_<account>_<user> = <key> [group] [group] [...] [storage_url] or if you want underscores in <account> or <user>, you can base64 encode them (with no equal signs) and use this format: user64_<account_b64>_<user_b64> = <key> [group] [group] [...] [storage_url] There are special groups of: .reseller_admin = can do anything to any account for this auth .admin = can do anything within the account If neither of these groups are specified, the user can only access containers that have been explicitly allowed for them by a .admin or .reseller_admin. The trailing optional storage_url allows you to specify an alternate url to hand back to the user upon authentication. If not specified, this defaults to $HOST/v1/<reseller_prefix>_<account> where $HOST will do its best to resolve to what the requester would need to use to reach this host. Here are example entries, required for running the tests:")

    swift_proxy_server_2013_2_1.param(
        'user_test2_tester2', type='string', default='testing2 .admin',
        description="Lastly, you need to list all the accounts/users you want here. The format is: user_<account>_<user> = <key> [group] [group] [...] [storage_url] or if you want underscores in <account> or <user>, you can base64 encode them (with no equal signs) and use this format: user64_<account_b64>_<user_b64> = <key> [group] [group] [...] [storage_url] There are special groups of: .reseller_admin = can do anything to any account for this auth .admin = can do anything within the account If neither of these groups are specified, the user can only access containers that have been explicitly allowed for them by a .admin or .reseller_admin. The trailing optional storage_url allows you to specify an alternate url to hand back to the user upon authentication. If not specified, this defaults to $HOST/v1/<reseller_prefix>_<account> where $HOST will do its best to resolve to what the requester would need to use to reach this host. Here are example entries, required for running the tests:")

    swift_proxy_server_2013_2_1.param(
        'user_test_tester3', type='string', default='testing3',
        description="Lastly, you need to list all the accounts/users you want here. The format is: user_<account>_<user> = <key> [group] [group] [...] [storage_url] or if you want underscores in <account> or <user>, you can base64 encode them (with no equal signs) and use this format: user64_<account_b64>_<user_b64> = <key> [group] [group] [...] [storage_url] There are special groups of: .reseller_admin = can do anything to any account for this auth .admin = can do anything within the account If neither of these groups are specified, the user can only access containers that have been explicitly allowed for them by a .admin or .reseller_admin. The trailing optional storage_url allows you to specify an alternate url to hand back to the user upon authentication. If not specified, this defaults to $HOST/v1/<reseller_prefix>_<account> where $HOST will do its best to resolve to what the requester would need to use to reach this host. Here are example entries, required for running the tests:")

    swift_proxy_server_2013_2_1.param('paste.filter_factory', type='string',
                                      default='keystoneclient.middleware.auth_token:filter_factory', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'auth_host', type='string', default='keystonehost', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'auth_port', type='string', default='35357', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'auth_protocol', type='string', default='http', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'auth_uri', type='string', default='http://keystonehost:5000/', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'admin_tenant_name', type='string', default='service', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'admin_user', type='string', default='swift', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'admin_password', type='string', default='password', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'delay_auth_decision', type='string', default='1', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'cache', type='string', default='swift.cache', description="[filter:authtoken]")

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#keystoneauth', description="[filter:keystoneauth]")

    swift_proxy_server_2013_2_1.param(
        'operator_roles', type='string', default='admin, swiftoperator',
        description="[filter:keystoneauth] Operator roles is the role which user would be allowed to manage a tenant and be able to create container or give ACL to others.")

    swift_proxy_server_2013_2_1.param(
        'reseller_admin_role', type='string', default='ResellerAdmin',
        description="[filter:keystoneauth] Operator roles is the role which user would be allowed to manage a tenant and be able to create container or give ACL to others. The reseller admin role has the ability to create and delete accounts")

    swift_proxy_server_2013_2_1.section('filter:healthcheck')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#healthcheck')

    swift_proxy_server_2013_2_1.param(
        'disable_path', type='string', default='',
        description="An optional filesystem path, which if present, will cause the healthcheck URL to return '503 Service Unavailable' with a body of 'DISABLED BY FILE'. This facility may be used to temporarily remove a Swift node from a load balancer pool during maintenance or upgrade (remove the file to allow the node back into the load balancer pool).")

    swift_proxy_server_2013_2_1.section('filter:cache')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#memcache')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='cache',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'memcache_servers', type='string', default='127.0.0.1:11211',
        description="If not set here, the value for memcache_servers will be read from memcache.conf (see memcache.conf-sample) or lacking that file, it will default to the value below. You can specify multiple servers separated with commas, as in: 10.1.2.3:11211,10.1.2.4:11211")

    swift_proxy_server_2013_2_1.param(
        'memcache_serialization_support', type='string', default='2',
        description="Sets how memcache values are serialized and deserialized: 0 = older, insecure pickle serialization 1 = json serialization but pickles can still be read (still insecure) 2 = json serialization only (secure and the default) If not set here, the value for memcache_serialization_support will be read from /etc/swift/memcache.conf (see memcache.conf-sample). To avoid an instant full cache flush, existing installations should upgrade with 0, then set to 1 and reload, then after some time (24 hours) set to 2 and reload. In the future, the ability to use pickle serialization will be removed.")

    swift_proxy_server_2013_2_1.section('filter:ratelimit')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#ratelimit')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='ratelimit',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'clock_accuracy', type='string', default='1000',
        description="clock_accuracy should represent how accurate the proxy servers' system clocks are with each other. 1000 means that all the proxies' clock are accurate to each other within 1 millisecond.  No ratelimit should be higher than the clock accuracy.")

    swift_proxy_server_2013_2_1.param(
        'max_sleep_time_seconds', type='string', default='60')

    swift_proxy_server_2013_2_1.param(
        'log_sleep_time_seconds', type='string', default='0', description="log_sleep_time_seconds of 0 means disabled")

    swift_proxy_server_2013_2_1.param(
        'rate_buffer_seconds', type='string', default='5',
        description="allows for slow rates (e.g. running up to 5 sec's behind) to catch up.")

    swift_proxy_server_2013_2_1.param(
        'account_ratelimit', type='string', default='0', description="account_ratelimit of 0 means disabled")

    swift_proxy_server_2013_2_1.param(
        'account_whitelist', type='string', default='a,b', description="these are comma separated lists of account names")

    swift_proxy_server_2013_2_1.param(
        'account_blacklist', type='string', default='c,d', description="these are comma separated lists of account names")

    swift_proxy_server_2013_2_1.param(
        'with container_limit_x', type='string', default='r')

    swift_proxy_server_2013_2_1.param(
        'container_ratelimit_0', type='string', default='100',
        description="for containers of size x limit write requests per second to r.  The container rate will be linearly interpolated from the values given. With the values below, a container of size 5 will get a rate of 75.")

    swift_proxy_server_2013_2_1.param(
        'container_ratelimit_10', type='string', default='50',
        description="for containers of size x limit write requests per second to r.  The container rate will be linearly interpolated from the values given. With the values below, a container of size 5 will get a rate of 75.")

    swift_proxy_server_2013_2_1.param(
        'container_ratelimit_50', type='string', default='20',
        description="for containers of size x limit write requests per second to r.  The container rate will be linearly interpolated from the values given. With the values below, a container of size 5 will get a rate of 75.")

    swift_proxy_server_2013_2_1.param(
        'container_listing_ratelimit_0', type='string', default='100',
        description="Similarly to the above container-level write limits, the following will limit container GET (listing) requests.")

    swift_proxy_server_2013_2_1.param(
        'container_listing_ratelimit_10', type='string', default='50',
        description="Similarly to the above container-level write limits, the following will limit container GET (listing) requests.")

    swift_proxy_server_2013_2_1.param(
        'container_listing_ratelimit_50', type='string', default='20',
        description="Similarly to the above container-level write limits, the following will limit container GET (listing) requests.")

    swift_proxy_server_2013_2_1.section('filter:domain_remap')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#domain_remap')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='domain_remap',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'storage_domain', type='string', default='example.com')

    swift_proxy_server_2013_2_1.param('path_root', type='string', default='v1')

    swift_proxy_server_2013_2_1.param(
        'reseller_prefixes', type='string', default='AUTH')

    swift_proxy_server_2013_2_1.section('filter:catch_errors')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#catch_errors')

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='catch_errors',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.section('filter:cname_lookup')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#cname_lookup', description="Note: this middleware requires python-dnspython")

    swift_proxy_server_2013_2_1.param(
        'set log_name', type='string', default='cname_lookup',
        description="Note: this middleware requires python-dnspython You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_facility', type='string', default='LOG_LOCAL0',
        description="Note: this middleware requires python-dnspython You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_level', type='string', default='INFO',
        description="Note: this middleware requires python-dnspython You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_headers', type='string', default='false',
        description="Note: this middleware requires python-dnspython You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'set log_address', type='string', default='/dev/log',
        description="Note: this middleware requires python-dnspython You can override the default log routing for this filter here:")

    swift_proxy_server_2013_2_1.param(
        'storage_domain', type='string', default='example.com')

    swift_proxy_server_2013_2_1.param(
        'lookup_depth', type='string', default='1')

    swift_proxy_server_2013_2_1.section('filter:staticweb')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#staticweb')

    swift_proxy_server_2013_2_1.section('filter:tempurl')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#tempurl')

    swift_proxy_server_2013_2_1.param(
        'methods', type='string', default='GET HEAD PUT', description="The methods allowed with Temp URLs.")

    swift_proxy_server_2013_2_1.param(
        'incoming_remove_headers', type='string', default='x-timestamp',
        description="The headers to remove from incoming requests. Simply a whitespace delimited list of header names and names can optionally end with '*' to indicate a prefix match. incoming_allow_headers is a list of exceptions to these removals.")

    swift_proxy_server_2013_2_1.param(
        'incoming_allow_headers', type='string', default='',
        description="The headers allowed as exceptions to incoming_remove_headers. Simply a whitespace delimited list of header names and names can optionally end with '*' to indicate a prefix match.")

    swift_proxy_server_2013_2_1.param(
        'outgoing_remove_headers', type='string', default='x-object-meta-*',
        description="The headers to remove from outgoing responses. Simply a whitespace delimited list of header names and names can optionally end with '*' to indicate a prefix match. outgoing_allow_headers is a list of exceptions to these removals.")

    swift_proxy_server_2013_2_1.section('filter:formpost')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#formpost')

    swift_proxy_server_2013_2_1.section('filter:name_check')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#name_check')

    swift_proxy_server_2013_2_1.param(
        'forbidden_chars', type='string', default='\'"`<>')

    swift_proxy_server_2013_2_1.param(
        'maximum_length', type='string', default='255')

    swift_proxy_server_2013_2_1.param(
        'forbidden_regexp', type='string', default='/\\./|/\\.\\./|/\\.$|/\\.\\.$')

    swift_proxy_server_2013_2_1.section('filter:list-endpoints')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#list_endpoints')

    swift_proxy_server_2013_2_1.param(
        'list_endpoints_path', type='string', default='/endpoints/')

    swift_proxy_server_2013_2_1.section('filter:proxy-logging')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#proxy_logging')

    swift_proxy_server_2013_2_1.param(
        'access_log_name', type='string', default='swift',
        description="If not set, logging directives from [DEFAULT] without 'access_' will be used")

    swift_proxy_server_2013_2_1.param(
        'access_log_facility', type='string', default='LOG_LOCAL0',
        description="If not set, logging directives from [DEFAULT] without 'access_' will be used")

    swift_proxy_server_2013_2_1.param(
        'access_log_level', type='string', default='INFO',
        description="If not set, logging directives from [DEFAULT] without 'access_' will be used")

    swift_proxy_server_2013_2_1.param(
        'access_log_address', type='string', default='/dev/log',
        description="If not set, logging directives from [DEFAULT] without 'access_' will be used")

    swift_proxy_server_2013_2_1.param(
        'access_log_udp_host', type='string', default='',
        description="If set, access_log_udp_host will override access_log_address")

    swift_proxy_server_2013_2_1.param(
        'access_log_udp_port', type='string', default='514',
        description="If set, access_log_udp_host will override access_log_address")

    swift_proxy_server_2013_2_1.param(
        'access_log_statsd_host', type='host', default='localhost',
        description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.param(
        'access_log_statsd_port', type='string', default='8125',
        description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.param(
        'access_log_statsd_default_sample_rate', type='string',
        default='1.0', description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.param(
        'access_log_statsd_sample_rate_factor', type='string',
        default='1.0', description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.param(
        'access_log_statsd_metric_prefix', type='string',
        default='', description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.param(
        'access_log_headers', type='string', default='false',
        description="You can use log_statsd_* from [DEFAULT] or override them here:")

    swift_proxy_server_2013_2_1.section('filter:bulk')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#bulk')

    swift_proxy_server_2013_2_1.param(
        'max_containers_per_extraction', type='string', default='10000')

    swift_proxy_server_2013_2_1.param(
        'max_failed_extractions', type='string', default='1000')

    swift_proxy_server_2013_2_1.param(
        'max_deletes_per_request', type='string', default='10000')

    swift_proxy_server_2013_2_1.param(
        'yield_frequency', type='string', default='60')

    swift_proxy_server_2013_2_1.section('filter:container-quotas')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#container_quotas')

    swift_proxy_server_2013_2_1.section('filter:slo')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#slo')

    swift_proxy_server_2013_2_1.param(
        'max_manifest_segments', type='string', default='1000')

    swift_proxy_server_2013_2_1.param(
        'max_manifest_size', type='string', default='2097152')

    swift_proxy_server_2013_2_1.param(
        'min_segment_size', type='string', default='1048576')

    swift_proxy_server_2013_2_1.section('filter:account-quotas')

    swift_proxy_server_2013_2_1.param(
        'use', type='string', default='egg:swift#account_quotas')
