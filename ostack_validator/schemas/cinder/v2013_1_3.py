from ostack_validator.schema import ConfigSchemaRegistry

cinder = ConfigSchemaRegistry.register_schema(project='cinder')

cinder.version('2013.1.3')

cinder.section('DEFAULT')

# make exception message format errors fatal (boolean value)
cinder.param('fatal_exception_format_errors', type='boolean', default='false')

# JSON file representing policy (string value)
cinder.param('policy_file', type='string', default='policy.json')

# Rule checked when requested rule is not found (string value)
cinder.param('policy_default_rule', type='string', default='default')

# number of volumes allowed per project (integer value)
cinder.param('quota_volumes', type='integer', default='10')

# number of volume snapshots allowed per project (integer
# value)
cinder.param('quota_snapshots', type='integer', default='10')

# number of volume gigabytes (snapshots are also included)
# allowed per project (integer value)
cinder.param('quota_gigabytes', type='integer', default='1000')

# number of seconds until a reservation expires (integer
# value)
cinder.param('reservation_expire', type='integer', default='86400')

# count of reservations until usage is refreshed (integer
# value)
cinder.param('until_refresh', type='integer', default='0')

# number of seconds between subsequent usage refreshes
# (integer value)
cinder.param('max_age', type='integer', default='0')

# default driver to use for quota checks (string value)
cinder.param('quota_driver', type='string', default='cinder.quota.DbQuotaDriver')

# whether to use default quota class for default quota
# (boolean value)
cinder.param('use_default_quota_class', type='boolean', default='true')

# seconds between nodes reporting state to datastore (integer
# value)
cinder.param('report_interval', type='integer', default='10')

# seconds between running periodic tasks (integer value)
cinder.param('periodic_interval', type='integer', default='60')

# range of seconds to randomly delay when starting the
# periodic task scheduler to reduce stampeding. (Disable by
# setting to 0) (integer value)
cinder.param('periodic_fuzzy_delay', type='integer', default='60')

# IP address for OpenStack Volume API to listen (string value)
cinder.param('osapi_volume_listen', type='string', default='0.0.0.0')

# port for os volume api to listen (integer value)
cinder.param('osapi_volume_listen_port', type='integer', default='8776')

# File name of clean sqlite db (string value)
cinder.param('sqlite_clean_db', type='string', default='clean.sqlite')

# should we use everything for testing (boolean value)
cinder.param('fake_tests', type='boolean', default='true')

# Number of backlog requests to configure the socket with
# (integer value)
cinder.param('backlog', type='integer', default='4096')

# Sets the value of TCP_KEEPIDLE in seconds for each server
# socket. Not supported on OS X. (integer value)
cinder.param('tcp_keepidle', type='integer', default='600')

# CA certificate file to use to verify connecting clients
# (string value)
cinder.param('ssl_ca_file', type='string', default='<None>')

# Certificate file to use when starting the server securely
# (string value)
cinder.param('ssl_cert_file', type='string', default='<None>')

# Private key file to use when starting the server securely
# (string value)
cinder.param('ssl_key_file', type='string', default='<None>')

# the maximum number of items returned in a single response
# from a collection resource (integer value)
cinder.param('osapi_max_limit', type='integer', default='1000')

# Base URL that will be presented to users in links to the
# OpenStack Volume API (string value)
cinder.param('osapi_volume_base_URL', type='string', default='<None>')

# Treat X-Forwarded-For as the canonical remote address. Only
# enable this if you have a sanitizing proxy. (boolean value)
cinder.param('use_forwarded_for', type='boolean', default='false')

# Max size for body of a request (integer value)
cinder.param('osapi_max_request_body_size', type='integer', default='114688')

# Ceph config file to use. (string value)
cinder.param('backup_ceph_conf', type='string', default='/etc/ceph/ceph.conf')

# the Ceph user to connect with (string value)
cinder.param('backup_ceph_user', type='string', default='cinder')

# the chunk size in bytes that a backup will be broken into
# before transfer to backup store (integer value)
cinder.param('backup_ceph_chunk_size', type='integer', default='134217728')

# the Ceph pool to backup to (string value)
cinder.param('backup_ceph_pool', type='string', default='backups')

# RBD stripe unit to use when creating a backup image (integer
# value)
cinder.param('backup_ceph_stripe_unit', type='integer', default='0')

# RBD stripe count to use when creating a backup image
# (integer value)
cinder.param('backup_ceph_stripe_count', type='integer', default='0')

# If True, always discard excess bytes when restoring volumes.
# (boolean value)
cinder.param('restore_discard_excess_bytes', type='boolean', default='true')

# The URL of the Swift endpoint (string value)
cinder.param('backup_swift_url', type='string', default='http://localhost:8080/v1/AUTH_')

# Swift authentication mechanism (string value)
cinder.param('backup_swift_auth', type='string', default='per_user')

# Swift user name (string value)
cinder.param('backup_swift_user', type='string', default='<None>')

# Swift key for authentication (string value)
cinder.param('backup_swift_key', type='string', default='<None>')

# The default Swift container to use (string value)
cinder.param('backup_swift_container', type='string', default='volumebackups')

# The size in bytes of Swift backup objects (integer value)
cinder.param('backup_swift_object_size', type='integer', default='52428800')

# The number of retries to make for Swift operations (integer
# value)
cinder.param('backup_swift_retry_attempts', type='integer', default='3')

# The backoff time in seconds between Swift retries (integer
# value)
cinder.param('backup_swift_retry_backoff', type='integer', default='2')

# Compression algorithm (None to disable) (string value)
cinder.param('backup_compression_algorithm', type='string', default='zlib')

# Volume prefix for the backup id when backing up to TSM
# (string value)
cinder.param('backup_tsm_volume_prefix', type='string', default='backup')

# TSM password for the running username (string value)
cinder.param('backup_tsm_password', type='string', default='password')

# Enable or Disable compression for backups (boolean value)
cinder.param('backup_tsm_compression', type='boolean', default='true')

# Driver to use for backups. (string value)
cinder.param('backup_driver', type='string', default='cinder.backup.drivers.swift')

# The maximum number of times to rescan targetsto find volume
# (integer value)
cinder.param('num_volume_device_scan_tries', type='integer', default='3')

# iscsi target user-land tool to use (string value)
cinder.param('iscsi_helper', type='string', default='tgtadm')

# Volume configuration file storage directory (string value)
cinder.param('volumes_dir', type='string', default='$state_path/volumes')

# IET configuration file (string value)
cinder.param('iet_conf', type='string', default='/etc/iet/ietd.conf')

# Comma-separatd list of initiator IQNs allowed to connect to
# the iSCSI target. (From Nova compute nodes.) (string value)
cinder.param('lio_initiator_iqns', type='string', default='')

# Sets the behavior of the iSCSI target to either perform
# blockio or fileio optionally, auto can be set and Cinder
# will autodetect type of backing device (string value)
cinder.param('iscsi_iotype', type='string', default='fileio')

# iser target user-land tool to use (string value)
cinder.param('iser_helper', type='string', default='tgtadm')

# Volume configuration file storage directory (string value)
cinder.param('volumes_dir', type='string', default='$state_path/volumes')

# Base dir containing mount points for nfs shares (string
# value)
cinder.param('nfs_mount_point_base', type='string', default='$state_path/mnt')

# Mount options passed to the nfs client. See section of the
# nfs man page for details (string value)
cinder.param('nfs_mount_options', type='string', default='<None>')

# Base dir containing mount points for gluster shares (string
# value)
cinder.param('glusterfs_mount_point_base', type='string', default='$state_path/mnt')

# Virtualization api connection type : libvirt, xenapi, or
# fake (string value)
cinder.param('connection_type', type='string', default='<None>')

# File name for the paste.deploy config for cinder-api (string
# value)
cinder.param('api_paste_config', type='string', default='api-paste.ini')

# Directory where the cinder python module is installed
# (string value)
cinder.param('pybasedir', type='string', default='/usr/lib/python/site-packages')

# Directory where cinder binaries are installed (string value)
cinder.param('bindir', type='string', default='$pybasedir/bin')

# Top-level directory for maintaining cinder's state (string
# value)
cinder.param('state_path', type='string', default='$pybasedir')

# ip address of this host (string value)
cinder.param('my_ip', type='string', default='10.0.0.1')

# default glance hostname or ip (string value)
cinder.param('glance_host', type='string', default='$my_ip')

# default glance port (integer value)
cinder.param('glance_port', type='integer', default='9292')

# A list of the glance api servers available to cinder
# ([hostname|ip]:port) (list value)
cinder.param('glance_api_servers', type='list', default='$glance_host:$glance_port')

# Version of the glance api to use (integer value)
cinder.param('glance_api_version', type='integer', default='1')

# Number retries when downloading an image from glance
# (integer value)
cinder.param('glance_num_retries', type='integer', default='0')

# Allow to perform insecure SSL (https) requests to glance
# (boolean value)
cinder.param('glance_api_insecure', type='boolean', default='false')

# Whether to attempt to negotiate SSL layer compression when
# using SSL (https) requests. Set to False to disable SSL
# layer compression. In some cases disabling this may improve
# data throughput, eg when high network bandwidth is available
# and you are using already compressed image formats such as
# qcow2 . (boolean value)
cinder.param('glance_api_ssl_compression', type='boolean', default='false')

# http/https timeout value for glance operations. If no value
# (None) is supplied here, the glanceclient default value is
# used. (integer value)
cinder.param('glance_request_timeout', type='integer', default='<None>')

# the topic scheduler nodes listen on (string value)
cinder.param('scheduler_topic', type='string', default='cinder-scheduler')

# the topic volume nodes listen on (string value)
cinder.param('volume_topic', type='string', default='cinder-volume')

# the topic volume backup nodes listen on (string value)
cinder.param('backup_topic', type='string', default='cinder-backup')

# Deploy v1 of the Cinder API.  (boolean value)
cinder.param('enable_v1_api', type='boolean', default='true')

# Deploy v2 of the Cinder API.  (boolean value)
cinder.param('enable_v2_api', type='boolean', default='true')

# whether to rate limit the api (boolean value)
cinder.param('api_rate_limit', type='boolean', default='true')

# Specify list of extensions to load when using
# osapi_volume_extension option with
# cinder.api.contrib.select_extensions (list value)
cinder.param('osapi_volume_ext_list', type='list', default='')

# osapi volume extension to load (multi valued)
cinder.param('osapi_volume_extension', type='multi', default='cinder.api.contrib.standard_extensions')

# full class name for the Manager for volume (string value)
cinder.param('volume_manager', type='string', default='cinder.volume.manager.VolumeManager')

# full class name for the Manager for volume backup (string
# value)
cinder.param('backup_manager', type='string', default='cinder.backup.manager.BackupManager')

# full class name for the Manager for scheduler (string value)
cinder.param('scheduler_manager', type='string', default='cinder.scheduler.manager.SchedulerManager')

# Name of this node.  This can be an opaque identifier.  It is
# not necessarily a hostname, FQDN, or IP address. (string
# value)
cinder.param('host', type='string', default='cinder')

# availability zone of this node (string value)
cinder.param('storage_availability_zone', type='string', default='nova')

# default availability zone to use when creating a new volume.
# If this is not set then we use the value from the
# storage_availability_zone option as the default
# availability_zone for new volumes. (string value)
cinder.param('default_availability_zone', type='string', default='<None>')

# Memcached servers or None for in process cache. (list value)
cinder.param('memcached_servers', type='list', default='<None>')

# default volume type to use (string value)
cinder.param('default_volume_type', type='string', default='<None>')

# time period to generate volume usages for.  Time period must
# be hour, day, month or year (string value)
cinder.param('volume_usage_audit_period', type='string', default='month')

# Deprecated: command to use for running commands as root
# (string value)
cinder.param('root_helper', type='string', default='sudo')

# Path to the rootwrap configuration file to use for running
# commands as root (string value)
cinder.param('rootwrap_config', type='string', default='<None>')

# Whether to log monkey patching (boolean value)
cinder.param('monkey_patch', type='boolean', default='false')

# List of modules/decorators to monkey patch (list value)
cinder.param('monkey_patch_modules', type='list', default='')

# maximum time since last check-in for up service (integer
# value)
cinder.param('service_down_time', type='integer', default='60')

# The full class name of the volume API class to use (string
# value)
cinder.param('volume_api_class', type='string', default='cinder.volume.api.API')

# The full class name of the volume backup API class (string
# value)
cinder.param('backup_api_class', type='string', default='cinder.backup.api.API')

# The strategy to use for auth. Supports noauth, keystone, and
# deprecated. (string value)
cinder.param('auth_strategy', type='string', default='noauth')

# A list of backend names to use. These backend names should
# be backed by a unique [CONFIG] group with its options (list
# value)
cinder.param('enabled_backends', type='list', default='<None>')

# Whether snapshots count against GigaByte quota (boolean
# value)
cinder.param('no_snapshot_gb_quota', type='boolean', default='false')

# The full class name of the volume transfer API class (string
# value)
cinder.param('transfer_api_class', type='string', default='cinder.transfer.api.API')

# The full class name of the compute API class to use (string
# value)
cinder.param('compute_api_class', type='string', default='cinder.compute.nova.API')

# Info to match when looking for nova in the service catalog.
# Format is : separated values of the form:
# <service_type>:<service_name>:<endpoint_type> (string value)
cinder.param('nova_catalog_info', type='string', default='compute:nova:publicURL')

# Same as nova_catalog_info, but for admin endpoint. (string
# value)
cinder.param('nova_catalog_admin_info', type='string', default='compute:nova:adminURL')

# Override service catalog lookup with template for nova
# endpoint e.g. http://localhost:8774/v2/%(tenant_id)s (string
# value)
cinder.param('nova_endpoint_template', type='string', default='<None>')

# Same as nova_endpoint_template, but for admin endpoint.
# (string value)
cinder.param('nova_endpoint_admin_template', type='string', default='<None>')

# region name of this node (string value)
cinder.param('os_region_name', type='string', default='<None>')

# Location of ca certicates file to use for nova client
# requests. (string value)
cinder.param('nova_ca_certificates_file', type='string', default='<None>')

# Allow to perform insecure SSL requests to nova (boolean
# value)
cinder.param('nova_api_insecure', type='boolean', default='false')

# The backend to use for db (string value)
cinder.param('db_backend', type='string', default='sqlalchemy')

# Services to be added to the available pool on create
# (boolean value)
cinder.param('enable_new_services', type='boolean', default='true')

# Template string to be used to generate volume names (string
# value)
cinder.param('volume_name_template', type='string', default='volume-%s')

# Template string to be used to generate snapshot names
# (string value)
cinder.param('snapshot_name_template', type='string', default='snapshot-%s')

# Template string to be used to generate backup names (string
# value)
cinder.param('backup_name_template', type='string', default='backup-%s')

# driver to use for database access (string value)
cinder.param('db_driver', type='string', default='cinder.db')

# A list of url schemes that can be downloaded directly via
# the direct_url.  Currently supported schemes: [file]. (list
# value)
cinder.param('allowed_direct_url_schemes', type='list', default='')

# Directory used for temporary storage during image conversion
# (string value)
cinder.param('image_conversion_dir', type='string', default='$state_path/conversion')

# The full class name of the key manager API class (string
# value)
cinder.param('keymgr_api_class', type='string', default='cinder.keymgr.not_implemented_key_mgr.NotImplementedKeyManager')

# The backend to use for db (string value)
cinder.param('backend', type='string', default='sqlalchemy')

# Enable the experimental use of thread pooling for all DB API
# calls (boolean value)
cinder.param('use_tpool', type='boolean', default='false')

# The SQLAlchemy connection string used to connect to the
# database (string value)
cinder.param('connection', type='string', default='sqlite:////cinder/openstack/common/db/$sqlite_db')

# timeout before idle sql connections are reaped (integer
# value)
cinder.param('idle_timeout', type='integer', default='3600')

# Minimum number of SQL connections to keep open in a pool
# (integer value)
cinder.param('min_pool_size', type='integer', default='1')

# Maximum number of SQL connections to keep open in a pool
# (integer value)
cinder.param('max_pool_size', type='integer', default='5')

# maximum db connection retries during startup. (setting -1
# implies an infinite retry count) (integer value)
cinder.param('max_retries', type='integer', default='10')

# interval between retries of opening a sql connection
# (integer value)
cinder.param('retry_interval', type='integer', default='10')

# If set, use this value for max_overflow with sqlalchemy
# (integer value)
cinder.param('max_overflow', type='integer', default='<None>')

# Verbosity of SQL debugging information. 0=None,
# 100=Everything (integer value)
cinder.param('connection_debug', type='integer', default='0')

# Add python stack traces to SQL as comment strings (boolean
# value)
cinder.param('connection_trace', type='boolean', default='false')

# the filename to use with sqlite (string value)
cinder.param('sqlite_db', type='string', default='cinder.sqlite')

# If true, use synchronous mode for sqlite (boolean value)
cinder.param('sqlite_synchronous', type='boolean', default='true')

# port for eventlet backdoor to listen (integer value)
cinder.param('backdoor_port', type='integer', default='<None>')

# Whether to disable inter-process locks (boolean value)
cinder.param('disable_process_locking', type='boolean', default='false')

# Directory to use for lock files. Default to a temp directory
# (string value)
cinder.param('lock_path', type='string', default='<None>')

# Print debugging output (set logging level to DEBUG instead
# of default WARNING level). (boolean value)
cinder.param('debug', type='boolean', default='false')

# Print more verbose output (set logging level to INFO instead
# of default WARNING level). (boolean value)
cinder.param('verbose', type='boolean', default='false')

# Log output to standard error (boolean value)
cinder.param('use_stderr', type='boolean', default='true')

# format string to use for log messages with context (string
# value)
cinder.param('logging_context_format_string', type='string', default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user)s %(tenant)s] %(instance)s%(message)s')

# format string to use for log messages without context
# (string value)
cinder.param('logging_default_format_string', type='string', default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s')

# data to append to log format when level is DEBUG (string
# value)
cinder.param('logging_debug_format_suffix', type='string', default='%(funcName)s %(pathname)s:%(lineno)d')

# prefix each line of exception output with this format
# (string value)
cinder.param('logging_exception_prefix', type='string', default='%(asctime)s.%(msecs)03d %(process)d TRACE %(name)s %(instance)s')

# list of logger=LEVEL pairs (list value)
cinder.param('default_log_levels', type='list', default='amqplibWARN,sqlalchemyWARN,botoWARN,sudsINFO,keystoneINFO,eventlet.wsgi.serverWARN')

# publish error events (boolean value)
cinder.param('publish_errors', type='boolean', default='false')

# make deprecations fatal (boolean value)
cinder.param('fatal_deprecations', type='boolean', default='false')

# If an instance is passed with the log message, format it
# like this (string value)
cinder.param('instance_format', type='string', default='"[instance: %(uuid)s] "')

# If an instance UUID is passed with the log message, format
# it like this (string value)
cinder.param('instance_uuid_format', type='string', default='"[instance: %(uuid)s] "')

# If this option is specified, the logging configuration file
# specified is used and overrides any other logging options
# specified. Please see the Python logging module
# documentation for details on logging configuration files.
# (string value)
cinder.param('log_config', type='string', default='<None>')

# A logging.Formatter log message format string which may use
# any of the available logging.LogRecord attributes. This
# option is deprecated.  Please use
# logging_context_format_string and
# logging_default_format_string instead. (string value)
cinder.param('log_format', type='string', default='<None>')

# Format string for %%(asctime)s in log records. Default:
# %(default)s (string value)
cinder.param('log_date_format', type='string', default='%Y-%m-%d %H:%M:%S')

# (Optional) Name of log file to output to. If no default is
# set, logging will go to stdout. (string value)
cinder.param('log_file', type='string', default='<None>')

# (Optional) The base directory used for relative --log-file
# paths (string value)
cinder.param('log_dir', type='string', default='<None>')

# Use syslog for logging. (boolean value)
cinder.param('use_syslog', type='boolean', default='false')

# syslog facility to receive log lines (string value)
cinder.param('syslog_log_facility', type='string', default='LOG_USER')

# Default notification level for outgoing notifications
# (string value)
cinder.param('default_notification_level', type='string', default='INFO')

# Default publisher_id for outgoing notifications (string
# value)
cinder.param('default_publisher_id', type='string', default='<None>')

# AMQP topic used for OpenStack notifications (list value)
cinder.param('notification_topics', type='list', default='notifications')

# AMQP topic(s) used for OpenStack notifications (list value)
cinder.param('topics', type='list', default='notifications')

# Some periodic tasks can be run in a separate process. Should
# we run them here? (boolean value)
cinder.param('run_external_periodic_tasks', type='boolean', default='true')

# The messaging module to use, defaults to kombu. (string
# value)
cinder.param('rpc_backend', type='string', default='cinder.openstack.common.rpc.impl_kombu')

# Size of RPC thread pool (integer value)
cinder.param('rpc_thread_pool_size', type='integer', default='64')

# Size of RPC connection pool (integer value)
cinder.param('rpc_conn_pool_size', type='integer', default='30')

# Seconds to wait for a response from call or multicall
# (integer value)
cinder.param('rpc_response_timeout', type='integer', default='60')

# Seconds to wait before a cast expires (TTL). Only supported
# by impl_zmq. (integer value)
cinder.param('rpc_cast_timeout', type='integer', default='30')

# Modules of exceptions that are permitted to be recreatedupon
# receiving exception data from an rpc call. (list value)
cinder.param('allowed_rpc_exception_modules', type='list', default='cinder.openstack.common.exception,nova.exception,cinder.exception,exceptions')

# If passed, use a fake RabbitMQ provider (boolean value)
cinder.param('fake_rabbit', type='boolean', default='false')

# AMQP exchange to connect to if using RabbitMQ or Qpid
# (string value)
cinder.param('control_exchange', type='string', default='openstack')

# Enable a fast single reply queue if using AMQP based RPC
# like RabbitMQ or Qpid. (boolean value)
cinder.param('amqp_rpc_single_reply_queue', type='boolean', default='false')

# Use durable queues in amqp. (boolean value)
cinder.param('amqp_durable_queues', type='boolean', default='false')

# Auto-delete queues in amqp. (boolean value)
cinder.param('amqp_auto_delete', type='boolean', default='false')

# SSL version to use (valid only if SSL enabled) (string
# value)
cinder.param('kombu_ssl_version', type='string', default='')

# SSL key file (valid only if SSL enabled) (string value)
cinder.param('kombu_ssl_keyfile', type='string', default='')

# SSL cert file (valid only if SSL enabled) (string value)
cinder.param('kombu_ssl_certfile', type='string', default='')

# SSL certification authority file (valid only if SSL enabled)
# (string value)
cinder.param('kombu_ssl_ca_certs', type='string', default='')

# The RabbitMQ broker address where a single node is used
# (string value)
cinder.param('rabbit_host', type='string', default='localhost')

# The RabbitMQ broker port where a single node is used
# (integer value)
cinder.param('rabbit_port', type='integer', default='5672')

# RabbitMQ HA cluster host:port pairs (list value)
cinder.param('rabbit_hosts', type='list', default='$rabbit_host:$rabbit_port')

# connect over SSL for RabbitMQ (boolean value)
cinder.param('rabbit_use_ssl', type='boolean', default='false')

# the RabbitMQ userid (string value)
cinder.param('rabbit_userid', type='string', default='guest')

# the RabbitMQ password (string value)
cinder.param('rabbit_password', type='string', default='guest')

# the RabbitMQ virtual host (string value)
cinder.param('rabbit_virtual_host', type='string', default='/')

# how frequently to retry connecting with RabbitMQ (integer
# value)
cinder.param('rabbit_retry_interval', type='integer', default='1')

# how long to backoff for between retries when connecting to
# RabbitMQ (integer value)
cinder.param('rabbit_retry_backoff', type='integer', default='2')

# maximum retries with trying to connect to RabbitMQ (the
# default of 0 implies an infinite retry count) (integer
# value)
cinder.param('rabbit_max_retries', type='integer', default='0')

# use H/A queues in RabbitMQ (x-ha-policy: all).You need to
# wipe RabbitMQ database when changing this option. (boolean
# value)
cinder.param('rabbit_ha_queues', type='boolean', default='false')

# Qpid broker hostname (string value)
cinder.param('qpid_hostname', type='string', default='localhost')

# Qpid broker port (integer value)
cinder.param('qpid_port', type='integer', default='5672')

# Qpid HA cluster host:port pairs (list value)
cinder.param('qpid_hosts', type='list', default='$qpid_hostname:$qpid_port')

# Username for qpid connection (string value)
cinder.param('qpid_username', type='string', default='')

# Password for qpid connection (string value)
cinder.param('qpid_password', type='string', default='')

# Space separated list of SASL mechanisms to use for auth
# (string value)
cinder.param('qpid_sasl_mechanisms', type='string', default='')

# Seconds between connection keepalive heartbeats (integer
# value)
cinder.param('qpid_heartbeat', type='integer', default='60')

# Transport to use, either 'tcp' or 'ssl' (string value)
cinder.param('qpid_protocol', type='string', default='tcp')

# Disable Nagle algorithm (boolean value)
cinder.param('qpid_tcp_nodelay', type='boolean', default='true')

# The qpid topology version to use.  Version 1 is what was
# originally used by impl_qpid.  Version 2 includes some
# backwards-incompatible changes that allow broker federation
# to work.  Users should update to version 2 when they are
# able to take everything down, as it requires a clean break.
# (integer value)
cinder.param('qpid_topology_version', type='integer', default='1')

# ZeroMQ bind address. Should be a wildcard (*), an ethernet
# interface, or IP. The "host" option should point or resolve
# to this address. (string value)
cinder.param('rpc_zmq_bind_address', type='string', default='*')

# MatchMaker driver (string value)
cinder.param('rpc_zmq_matchmaker', type='string', default='cinder.openstack.common.rpc.matchmaker.MatchMakerLocalhost')

# ZeroMQ receiver listening port (integer value)
cinder.param('rpc_zmq_port', type='integer', default='9501')

# Number of ZeroMQ contexts, defaults to 1 (integer value)
cinder.param('rpc_zmq_contexts', type='integer', default='1')

# Maximum number of ingress messages to locally buffer per
# topic. Default is unlimited. (integer value)
cinder.param('rpc_zmq_topic_backlog', type='integer', default='<None>')

# Directory for holding IPC sockets (string value)
cinder.param('rpc_zmq_ipc_dir', type='string', default='/var/run/openstack')

# Name of this node. Must be a valid hostname, FQDN, or IP
# address. Must match "host" option, if running Nova. (string
# value)
cinder.param('rpc_zmq_host', type='string', default='cinder')

# Matchmaker ring file (JSON) (string value)
cinder.param('matchmaker_ringfile', type='string', default='/etc/nova/matchmaker_ring.json')

# Heartbeat frequency (integer value)
cinder.param('matchmaker_heartbeat_freq', type='integer', default='300')

# Heartbeat time-to-live. (integer value)
cinder.param('matchmaker_heartbeat_ttl', type='integer', default='600')

# Host to locate redis (string value)
cinder.param('host', type='string', default='127.0.0.1')

# Use this port to connect to redis host. (integer value)
cinder.param('port', type='integer', default='6379')

# Password for Redis server. (optional) (string value)
cinder.param('password', type='string', default='<None>')

# The scheduler host manager class to use (string value)
cinder.param('scheduler_host_manager', type='string', default='cinder.scheduler.host_manager.HostManager')

# Maximum number of attempts to schedule an volume (integer
# value)
cinder.param('scheduler_max_attempts', type='integer', default='3')

# Which filter class names to use for filtering hosts when not
# specified in the request. (list value)
cinder.param('scheduler_default_filters', type='list', default='AvailabilityZoneFilter,CapacityFilter,CapabilitiesFilter')

# Which weigher class names to use for weighing hosts. (list
# value)
cinder.param('scheduler_default_weighers', type='list', default='CapacityWeigher')

# Default scheduler driver to use (string value)
cinder.param('scheduler_driver', type='string', default='cinder.scheduler.filter_scheduler.FilterScheduler')

# Absolute path to scheduler configuration JSON file. (string
# value)
cinder.param('scheduler_json_config_location', type='string', default='')

# maximum number of volume gigabytes to allow per host
# (integer value)
cinder.param('max_gigabytes', type='integer', default='10000')

# Multiplier used for weighing volume capacity. Negative
# numbers mean to stack vs spread. (floating point value)
cinder.param('capacity_weight_multiplier', type='floating point', default='1.0')

# The number of characters in the salt. (integer value)
cinder.param('volume_transfer_salt_length', type='integer', default='8')

# The number of characters in the autogenerated auth key.
# (integer value)
cinder.param('volume_transfer_key_length', type='integer', default='16')

# Create volume from snapshot at the host where snapshot
# resides (boolean value)
cinder.param('snapshot_same_host', type='boolean', default='true')

# Ensure that the new volumes are the same AZ as snapshot or
# source volume (boolean value)
cinder.param('cloned_volume_same_az', type='boolean', default='true')

# number of times to attempt to run flakey shell commands
# (integer value)
cinder.param('num_shell_tries', type='integer', default='3')

# The percentage of backend capacity is reserved (integer
# value)
cinder.param('reserved_percentage', type='integer', default='0')

# The maximum number of iscsi target ids per host (integer
# value)
cinder.param('iscsi_num_targets', type='integer', default='100')

# prefix for iscsi volumes (string value)
cinder.param('iscsi_target_prefix', type='string', default='iqn.2010-10.org.openstack:')

# The IP address that the iSCSI daemon is listening on (string
# value)
cinder.param('iscsi_ip_address', type='string', default='$my_ip')

# The port that the iSCSI daemon is listening on (integer
# value)
cinder.param('iscsi_port', type='integer', default='3260')

# The maximum number of times to rescan iSER targetto find
# volume (integer value)
cinder.param('num_iser_scan_tries', type='integer', default='3')

# The maximum number of iser target ids per host (integer
# value)
cinder.param('iser_num_targets', type='integer', default='100')

# prefix for iser volumes (string value)
cinder.param('iser_target_prefix', type='string', default='iqn.2010-10.org.iser.openstack:')

# The IP address that the iSER daemon is listening on (string
# value)
cinder.param('iser_ip_address', type='string', default='$my_ip')

# The port that the iSER daemon is listening on (integer
# value)
cinder.param('iser_port', type='integer', default='3260')

# The backend name for a given driver implementation (string
# value)
cinder.param('volume_backend_name', type='string', default='<None>')

# Do we attach/detach volumes in cinder using multipath for
# volume to image and image to volume transfers? (boolean
# value)
cinder.param('use_multipath_for_image_xfer', type='boolean', default='false')

# Method used to wipe old voumes (valid options are: none,
# zero, shred) (string value)
cinder.param('volume_clear', type='string', default='zero')

# Size in MiB to wipe at start of old volumes. 0 => all
# (integer value)
cinder.param('volume_clear_size', type='integer', default='0')

# List of all available devices (list value)
cinder.param('available_devices', type='list', default='')

# IP address of Coraid ESM (string value)
cinder.param('coraid_esm_address', type='string', default='')

# User name to connect to Coraid ESM (string value)
cinder.param('coraid_user', type='string', default='admin')

# Name of group on Coraid ESM to which coraid_user belongs
# (must have admin privilege) (string value)
cinder.param('coraid_group', type='string', default='admin')

# Password to connect to Coraid ESM (string value)
cinder.param('coraid_password', type='string', default='password')

# Volume Type key name to store ESM Repository Name (string
# value)
cinder.param('coraid_repository_key', type='string', default='coraid_repository')

# Group name to use for creating volumes (string value)
cinder.param('eqlx_group_name', type='string', default='group-0')

# Timeout for the Group Manager cli command execution (integer
# value)
cinder.param('eqlx_cli_timeout', type='integer', default='30')

# Maximum retry count for reconnection (integer value)
cinder.param('eqlx_cli_max_retries', type='integer', default='5')

# Use CHAP authentificaion for targets? (boolean value)
cinder.param('eqlx_use_chap', type='boolean', default='false')

# Existing CHAP account name (string value)
cinder.param('eqlx_chap_login', type='string', default='admin')

# Password for specified CHAP account name (string value)
cinder.param('eqlx_chap_password', type='string', default='password')

# Pool in which volumes will be created (string value)
cinder.param('eqlx_pool', type='string', default='default')

# File with the list of available gluster shares (string
# value)
cinder.param('glusterfs_shares_config', type='string', default='/etc/cinder/glusterfs_shares')

# Use du or df for free space calculation (string value)
cinder.param('glusterfs_disk_util', type='string', default='df')

# Create volumes as sparsed files which take no space.If set
# to False volume is created as regular file.In such case
# volume creation takes a lot of time. (boolean value)
cinder.param('glusterfs_sparsed_volumes', type='boolean', default='true')

# Create volumes as QCOW2 files rather than raw files.
# (boolean value)
cinder.param('glusterfs_qcow2_volumes', type='boolean', default='false')

# Path to the directory on GPFS mount point where volumes are
# stored (string value)
cinder.param('gpfs_mount_point_base', type='string', default='<None>')

# Path to GPFS Glance repository as mounted on Nova nodes
# (string value)
cinder.param('gpfs_images_dir', type='string', default='<None>')

# Set this if Glance image repo is on GPFS as well so that the
# image bits can be transferred efficiently between Glance and
# Cinder.  Valid values are copy or copy_on_write. copy
# performs a full copy of the image, copy_on_write efficiently
# shares unmodified blocks of the image. (string value)
cinder.param('gpfs_images_share_mode', type='string', default='<None>')

# A lengthy chain of copy-on-write snapshots or clones could
# have impact on performance.  This option limits the number
# of indirections required to reach a specific block. 0
# indicates unlimited. (integer value)
cinder.param('gpfs_max_clone_depth', type='integer', default='0')

# Create volumes as sparse files which take no space. If set
# to False volume is created as regular file. In this case
# volume creation may take a significantly longer time.
# (boolean value)
cinder.param('gpfs_sparse_volumes', type='boolean', default='true')

# configuration file for HDS cinder plugin for HUS (string
# value)
cinder.param('hds_cinder_config_file', type='string', default='/opt/hds/hus/cinder_hus_conf.xml')

# config data for cinder huawei plugin (string value)
cinder.param('cinder_huawei_conf_file', type='string', default='/etc/cinder/cinder_huawei_conf.xml')

# Name for the VG that will contain exported volumes (string
# value)
cinder.param('volume_group', type='string', default='cinder-volumes')

# Size of thin provisioning pool (None uses entire cinder VG)
# (string value)
cinder.param('pool_size', type='string', default='<None>')

# If set, create lvms with multiple mirrors. Note that this
# requires lvm_mirrors + 2 pvs with available space (integer
# value)
cinder.param('lvm_mirrors', type='integer', default='0')

# Type of LVM volumes to deploy; (default or thin) (string
# value)
cinder.param('lvm_type', type='string', default='default')

# Vfiler to use for provisioning (string value)
cinder.param('netapp_vfiler', type='string', default='<None>')

# User name for the storage controller (string value)
cinder.param('netapp_login', type='string', default='<None>')

# Password for the storage controller (string value)
cinder.param('netapp_password', type='string', default='<None>')

# Cluster vserver to use for provisioning (string value)
cinder.param('netapp_vserver', type='string', default='<None>')

# Host name for the storage controller (string value)
cinder.param('netapp_server_hostname', type='string', default='<None>')

# Port number for the storage controller (integer value)
cinder.param('netapp_server_port', type='integer', default='80')

# Threshold available percent to start cache cleaning.
# (integer value)
cinder.param('thres_avl_size_perc_start', type='integer', default='20')

# Threshold available percent to stop cache cleaning. (integer
# value)
cinder.param('thres_avl_size_perc_stop', type='integer', default='60')

# Threshold minutes after which cache file can be cleaned.
# (integer value)
cinder.param('expiry_thres_minutes', type='integer', default='720')

# Volume size multiplier to ensure while creation (floating
# point value)
cinder.param('netapp_size_multiplier', type='floating point', default='1.2')

# Comma separated volumes to be used for provisioning (string
# value)
cinder.param('netapp_volume_list', type='string', default='<None>')

# Storage family type. (string value)
cinder.param('netapp_storage_family', type='string', default='ontap_cluster')

# Storage protocol type. (string value)
cinder.param('netapp_storage_protocol', type='string', default='<None>')

# Transport type protocol (string value)
cinder.param('netapp_transport_type', type='string', default='http')

# IP address of Nexenta SA (string value)
cinder.param('nexenta_host', type='string', default='')

# HTTP port to connect to Nexenta REST API server (integer
# value)
cinder.param('nexenta_rest_port', type='integer', default='2000')

# Use http or https for REST connection (default auto) (string
# value)
cinder.param('nexenta_rest_protocol', type='string', default='auto')

# User name to connect to Nexenta SA (string value)
cinder.param('nexenta_user', type='string', default='admin')

# Password to connect to Nexenta SA (string value)
cinder.param('nexenta_password', type='string', default='nexenta')

# Nexenta target portal port (integer value)
cinder.param('nexenta_iscsi_target_portal_port', type='integer', default='3260')

# pool on SA that will hold all volumes (string value)
cinder.param('nexenta_volume', type='string', default='cinder')

# IQN prefix for iSCSI targets (string value)
cinder.param('nexenta_target_prefix', type='string', default='iqn.1986-03.com.sun:02:cinder-')

# prefix for iSCSI target groups on SA (string value)
cinder.param('nexenta_target_group_prefix', type='string', default='cinder/')

# File with the list of available nfs shares (string value)
cinder.param('nexenta_shares_config', type='string', default='/etc/cinder/nfs_shares')

# Base dir containing mount points for nfs shares (string
# value)
cinder.param('nexenta_mount_point_base', type='string', default='$state_path/mnt')

# Create volumes as sparsed files which take no space.If set
# to False volume is created as regular file.In such case
# volume creation takes a lot of time. (boolean value)
cinder.param('nexenta_sparsed_volumes', type='boolean', default='true')

# Default compression value for new ZFS folders. (string
# value)
cinder.param('nexenta_volume_compression', type='string', default='on')

# Mount options passed to the nfs client. See section of the
# nfs man page for details (string value)
cinder.param('nexenta_mount_options', type='string', default='<None>')

# Percent of ACTUAL usage of the underlying volume before no
# new volumes can be allocated to the volume destination.
# (floating point value)
cinder.param('nexenta_used_ratio', type='floating point', default='0.95')

# This will compare the allocated to available space on the
# volume destination.  If the ratio exceeds this number, the
# destination will no longer be valid. (floating point value)
cinder.param('nexenta_oversub_ratio', type='floating point', default='1.0')

# block size for volumes (blank=default,8KB) (string value)
cinder.param('nexenta_blocksize', type='string', default='')

# flag to create sparse volumes (boolean value)
cinder.param('nexenta_sparse', type='boolean', default='false')

# File with the list of available nfs shares (string value)
cinder.param('nfs_shares_config', type='string', default='/etc/cinder/nfs_shares')

# Create volumes as sparsed files which take no space.If set
# to False volume is created as regular file.In such case
# volume creation takes a lot of time. (boolean value)
cinder.param('nfs_sparsed_volumes', type='boolean', default='true')

# Percent of ACTUAL usage of the underlying volume before no
# new volumes can be allocated to the volume destination.
# (floating point value)
cinder.param('nfs_used_ratio', type='floating point', default='0.95')

# This will compare the allocated to available space on the
# volume destination.  If the ratio exceeds this number, the
# destination will no longer be valid. (floating point value)
cinder.param('nfs_oversub_ratio', type='floating point', default='1.0')

# the RADOS pool in which rbd volumes are stored (string
# value)
cinder.param('rbd_pool', type='string', default='rbd')

# the RADOS client name for accessing rbd volumes - only set
# when using cephx authentication (string value)
cinder.param('rbd_user', type='string', default='<None>')

# path to the ceph configuration file to use (string value)
cinder.param('rbd_ceph_conf', type='string', default='')

# flatten volumes created from snapshots to remove dependency
# (boolean value)
cinder.param('rbd_flatten_volume_from_snapshot', type='boolean', default='false')

# the libvirt uuid of the secret for the rbd_uservolumes
# (string value)
cinder.param('rbd_secret_uuid', type='string', default='<None>')

# where to store temporary image files if the volume driver
# does not write them directly to the volume (string value)
cinder.param('volume_tmp_dir', type='string', default='<None>')

# maximum number of nested clones that can be taken of a
# volume before enforcing a flatten prior to next clone. A
# value of zero disables cloning (integer value)
cinder.param('rbd_max_clone_depth', type='integer', default='5')

# 3PAR WSAPI Server Url like https://<3par ip>:8080/api/v1
# (string value)
cinder.param('hp3par_api_url', type='string', default='')

# 3PAR Super user username (string value)
cinder.param('hp3par_username', type='string', default='')

# 3PAR Super user password (string value)
cinder.param('hp3par_password', type='string', default='')

# This option is DEPRECATED and no longer used. The 3par
# domain name to use. (string value)
cinder.param('hp3par_domain', type='string', default='<None>')

# The CPG to use for volume creation (string value)
cinder.param('hp3par_cpg', type='string', default='OpenStack')

# The CPG to use for Snapshots for volumes. If empty
# hp3par_cpg will be used (string value)
cinder.param('hp3par_cpg_snap', type='string', default='')

# The time in hours to retain a snapshot.  You can't delete it
# before this expires. (string value)
cinder.param('hp3par_snapshot_retention', type='string', default='')

# The time in hours when a snapshot expires  and is deleted.
# This must be larger than expiration (string value)
cinder.param('hp3par_snapshot_expiration', type='string', default='')

# Enable HTTP debugging to 3PAR (boolean value)
cinder.param('hp3par_debug', type='boolean', default='false')

# List of target iSCSI addresses to use. (list value)
cinder.param('hp3par_iscsi_ips', type='list', default='')

# Use thin provisioning for SAN volumes? (boolean value)
cinder.param('san_thin_provision', type='boolean', default='true')

# IP address of SAN controller (string value)
cinder.param('san_ip', type='string', default='')

# Username for SAN controller (string value)
cinder.param('san_login', type='string', default='admin')

# Password for SAN controller (string value)
cinder.param('san_password', type='string', default='')

# Filename of private key to use for SSH authentication
# (string value)
cinder.param('san_private_key', type='string', default='')

# Cluster name to use for creating volumes (string value)
cinder.param('san_clustername', type='string', default='')

# SSH port to use with SAN (integer value)
cinder.param('san_ssh_port', type='integer', default='22')

# Execute commands locally instead of over SSH; use if the
# volume service is running on the SAN device (boolean value)
cinder.param('san_is_local', type='boolean', default='false')

# SSH connection timeout in seconds (integer value)
cinder.param('ssh_conn_timeout', type='integer', default='30')

# Minimum ssh connections in the pool (integer value)
cinder.param('ssh_min_pool_conn', type='integer', default='1')

# Maximum ssh connections in the pool (integer value)
cinder.param('ssh_max_pool_conn', type='integer', default='5')

# The ZFS path under which to create zvols for volumes.
# (string value)
cinder.param('san_zfs_volume_base', type='string', default='rpool/')

# Path or URL to Scality SOFS configuration file (string
# value)
cinder.param('scality_sofs_config', type='string', default='<None>')

# Base dir where Scality SOFS shall be mounted (string value)
cinder.param('scality_sofs_mount_point', type='string', default='$state_path/scality')

# Path from Scality SOFS root to volume dir (string value)
cinder.param('scality_sofs_volume_dir', type='string', default='cinder/volumes')

# Set 512 byte emulation on volume creation;  (boolean value)
cinder.param('sf_emulate_512', type='boolean', default='true')

# Allow tenants to specify QOS on create (boolean value)
cinder.param('sf_allow_tenant_qos', type='boolean', default='false')

# Create SolidFire accounts with this prefix (string value)
cinder.param('sf_account_prefix', type='string', default='cinder')

# SolidFire API port. Useful if the device api is behind a
# proxy on a different port. (integer value)
cinder.param('sf_api_port', type='integer', default='443')

# Storage system storage pool for volumes (string value)
cinder.param('storwize_svc_volpool_name', type='string', default='volpool')

# Storage system space-efficiency parameter for volumes
# (percentage) (integer value)
cinder.param('storwize_svc_vol_rsize', type='integer', default='2')

# Storage system threshold for volume capacity warnings
# (percentage) (integer value)
cinder.param('storwize_svc_vol_warning', type='integer', default='0')

# Storage system autoexpand parameter for volumes (True/False)
# (boolean value)
cinder.param('storwize_svc_vol_autoexpand', type='boolean', default='true')

# Storage system grain size parameter for volumes
# (32/64/128/256) (integer value)
cinder.param('storwize_svc_vol_grainsize', type='integer', default='256')

# Storage system compression option for volumes (boolean
# value)
cinder.param('storwize_svc_vol_compression', type='boolean', default='false')

# Enable Easy Tier for volumes (boolean value)
cinder.param('storwize_svc_vol_easytier', type='boolean', default='true')

# The I/O group in which to allocate volumes (integer value)
cinder.param('storwize_svc_vol_iogrp', type='integer', default='0')

# Maximum number of seconds to wait for FlashCopy to be
# prepared. Maximum value is 600 seconds (10 minutes) (integer
# value)
cinder.param('storwize_svc_flashcopy_timeout', type='integer', default='120')

# Connection protocol (iSCSI/FC) (string value)
cinder.param('storwize_svc_connection_protocol', type='string', default='iSCSI')

# Connect with multipath (FC only; iSCSI multipath is
# controlled by Nova) (boolean value)
cinder.param('storwize_svc_multipath_enabled', type='boolean', default='false')

# Allows vdisk to multi host mapping (boolean value)
cinder.param('storwize_svc_multihostmap_enabled', type='boolean', default='true')

# IP address for connecting to VMware ESX/VC server. (string
# value)
cinder.param('vmware_host_ip', type='string', default='<None>')

# Username for authenticating with VMware ESX/VC server.
# (string value)
cinder.param('vmware_host_username', type='string', default='<None>')

# Password for authenticating with VMware ESX/VC server.
# (string value)
cinder.param('vmware_host_password', type='string', default='<None>')

# Optional VIM service WSDL Location e.g
# http://<server>/vimService.wsdl. Optional over-ride to
# default location for bug work-arounds. (string value)
cinder.param('vmware_wsdl_location', type='string', default='<None>')

# Number of times VMware ESX/VC server API must be retried
# upon connection related issues. (integer value)
cinder.param('vmware_api_retry_count', type='integer', default='10')

# The interval used for polling remote tasks invoked on VMware
# ESX/VC server. (integer value)
cinder.param('vmware_task_poll_interval', type='integer', default='5')

# Name for the folder in the VC datacenter that will contain
# cinder volumes. (string value)
cinder.param('vmware_volume_folder', type='string', default='cinder-volumes')

# Timeout in seconds for VMDK volume transfer between Cinder
# and Glance. (integer value)
cinder.param('vmware_image_transfer_timeout_secs', type='integer', default='7200')

# Path to store VHD backed volumes (string value)
cinder.param('windows_iscsi_lun_path', type='string', default='C:\iSCSIVirtualDisks')

# NFS server to be used by XenAPINFSDriver (string value)
cinder.param('xenapi_nfs_server', type='string', default='<None>')

# Path of exported NFS, used by XenAPINFSDriver (string value)
cinder.param('xenapi_nfs_serverpath', type='string', default='<None>')

# URL for XenAPI connection (string value)
cinder.param('xenapi_connection_url', type='string', default='<None>')

# Username for XenAPI connection (string value)
cinder.param('xenapi_connection_username', type='string', default='root')

# Password for XenAPI connection (string value)
cinder.param('xenapi_connection_password', type='string', default='<None>')

# Base path to the storage repository (string value)
cinder.param('xenapi_sr_base_path', type='string', default='/var/run/sr-mount')

# Proxy driver that connects to the IBM Storage Array (string
# value)
cinder.param('xiv_ds8k_proxy', type='string', default='xiv_ds8k_openstack.nova_proxy.XIVDS8KNovaProxy')

# Connection type to the IBM Storage Array
# (fibre_channel|iscsi) (string value)
cinder.param('xiv_ds8k_connection_type', type='string', default='iscsi')

# Management IP of Zadara VPSA (string value)
cinder.param('zadara_vpsa_ip', type='string', default='<None>')

# Zadara VPSA port number (string value)
cinder.param('zadara_vpsa_port', type='string', default='<None>')

# Use SSL connection (boolean value)
cinder.param('zadara_vpsa_use_ssl', type='boolean', default='false')

# User name for the VPSA (string value)
cinder.param('zadara_user', type='string', default='<None>')

# Password for the VPSA (string value)
cinder.param('zadara_password', type='string', default='<None>')

# Name of VPSA storage pool for volumes (string value)
cinder.param('zadara_vpsa_poolname', type='string', default='<None>')

# Default thin provisioning policy for volumes (boolean value)
cinder.param('zadara_vol_thin', type='boolean', default='true')

# Default encryption policy for volumes (boolean value)
cinder.param('zadara_vol_encrypt', type='boolean', default='false')

# Default striping mode for volumes (string value)
cinder.param('zadara_default_striping_mode', type='string', default='simple')

# Default stripe size for volumes (string value)
cinder.param('zadara_default_stripesize', type='string', default='64')

# Default template for VPSA volume names (string value)
cinder.param('zadara_vol_name_template', type='string', default='OS_%s')

# Automatically detach from servers on volume delete (boolean
# value)
cinder.param('zadara_vpsa_auto_detach_on_delete', type='boolean', default='true')

# Don't halt on deletion of non-existing volumes (boolean
# value)
cinder.param('zadara_vpsa_allow_nonexistent_delete', type='boolean', default='true')

# Driver to use for volume creation (string value)
cinder.param('volume_driver', type='string', default='cinder.volume.drivers.lvm.LVMISCSIDriver')

# Timeout for creating the volume to migrate to when
# performing volume migration (seconds) (integer value)
cinder.param('migration_create_volume_timeout_secs', type='integer', default='300')

# The default block size used when copying/clearing volumes
# (string value)
cinder.param('volume_dd_blocksize', type='string', default='1M')

