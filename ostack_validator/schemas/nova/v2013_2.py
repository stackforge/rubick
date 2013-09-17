from ostack_validator.schema import ConfigSchemaRegistry

nova = ConfigSchemaRegistry.register_schema(project='nova')

nova.version('2013.1')

nova.section('DEFAULT')

# availability_zone to show internal services under (string
# value)
nova.param('internal_service_availability_zone', type='string', default='internal')

# default compute node availability_zone (string value)
nova.param('default_availability_zone', type='string', default='nova')

# Filename of root CA (string value)
nova.param('ca_file', type='string', default='cacert.pem')

# Filename of private key (string value)
nova.param('key_file', type='string', default='private/cakey.pem')

# Filename of root Certificate Revocation List (string value)
nova.param('crl_file', type='string', default='crl.pem')

# Where we keep our keys (string value)
nova.param('keys_path', type='string', default='$state_path/keys')

# Where we keep our root CA (string value)
nova.param('ca_path', type='string', default='$state_path/CA')

# Should we use a CA for each project? (boolean value)
nova.param('use_project_ca', type='boolean', default='false')

# Subject for certificate for users, %s for project, user,
# timestamp (string value)
nova.param('user_cert_subject', type='string', default='/C')

# Subject for certificate for projects, %s for project,
# timestamp (string value)
nova.param('project_cert_subject', type='string', default='/C')

# make exception message format errors fatal (boolean value)
nova.param('fatal_exception_format_errors', type='boolean', default='false')

# Some periodic tasks can be run in a separate process. Should
# we run them here? (boolean value)
nova.param('run_external_periodic_tasks', type='boolean', default='true')

# ip address of this host (string value)
nova.param('my_ip', type='string', default='10.0.0.1')

# Name of this node.  This can be an opaque identifier.  It is
# not necessarily a hostname, FQDN, or IP address. However,
# the node name must be valid within an AMQP key, and if using
# ZeroMQ, a valid hostname, FQDN, or IP address (string value)
nova.param('host', type='string', default='nova')

# use ipv6 (boolean value)
nova.param('use_ipv6', type='boolean', default='false')

# If set, send compute.instance.update notifications on
# instance state changes.  Valid values are False for no
# notifications, True for notifications on any instance
# changes. (boolean value)
nova.param('notify_on_any_change', type='boolean', default='false')

# If set, send api.fault notifications on caught exceptions in
# the API service. (boolean value)
nova.param('notify_api_faults', type='boolean', default='false')

# If set, send compute.instance.update notifications on
# instance state changes.  Valid values are None for no
# notifications, "vm_state" for notifications on VM state
# changes, or "vm_and_task_state" for notifications on VM and
# task state changes. (string value)
nova.param('notify_on_state_change', type='string', default='<None>')

# Directory where the nova python module is installed (string
# value)
nova.param('pybasedir', type='string', default='/usr/lib/python/site-packages')

# Directory where nova binaries are installed (string value)
nova.param('bindir', type='string', default='$pybasedir/bin')

# Top-level directory for maintaining nova's state (string
# value)
nova.param('state_path', type='string', default='$pybasedir')

# JSON file representing policy (string value)
nova.param('policy_file', type='string', default='policy.json')

# Rule checked when requested rule is not found (string value)
nova.param('policy_default_rule', type='string', default='default')

# number of instances allowed per project (integer value)
nova.param('quota_instances', type='integer', default='10')

# number of instance cores allowed per project (integer value)
nova.param('quota_cores', type='integer', default='20')

# megabytes of instance ram allowed per project (integer
# value)
nova.param('quota_ram', type='integer', default='51200')

# number of floating ips allowed per project (integer value)
nova.param('quota_floating_ips', type='integer', default='10')

# number of metadata items allowed per instance (integer
# value)
nova.param('quota_metadata_items', type='integer', default='128')

# number of injected files allowed (integer value)
nova.param('quota_injected_files', type='integer', default='5')

# number of bytes allowed per injected file (integer value)
nova.param('quota_injected_file_content_bytes', type='integer', default='10240')

# number of bytes allowed per injected file path (integer
# value)
nova.param('quota_injected_file_path_bytes', type='integer', default='255')

# number of security groups per project (integer value)
nova.param('quota_security_groups', type='integer', default='10')

# number of security rules per security group (integer value)
nova.param('quota_security_group_rules', type='integer', default='20')

# number of key pairs per user (integer value)
nova.param('quota_key_pairs', type='integer', default='100')

# number of seconds until a reservation expires (integer
# value)
nova.param('reservation_expire', type='integer', default='86400')

# count of reservations until usage is refreshed (integer
# value)
nova.param('until_refresh', type='integer', default='0')

# number of seconds between subsequent usage refreshes
# (integer value)
nova.param('max_age', type='integer', default='0')

# default driver to use for quota checks (string value)
nova.param('quota_driver', type='string', default='nova.quota.DbQuotaDriver')

# seconds between nodes reporting state to datastore (integer
# value)
nova.param('report_interval', type='integer', default='10')

# enable periodic tasks (boolean value)
nova.param('periodic_enable', type='boolean', default='true')

# range of seconds to randomly delay when starting the
# periodic task scheduler to reduce stampeding. (Disable by
# setting to 0) (integer value)
nova.param('periodic_fuzzy_delay', type='Disable by setting to 0) (integer', default='60')

# a list of APIs to enable by default (list value)
nova.param('enabled_apis', type='list', default='ec2,osapi_compute,metadata')

# a list of APIs with enabled SSL (list value)
nova.param('enabled_ssl_apis', type='list', default='')

# IP address for EC2 API to listen (string value)
nova.param('ec2_listen', type='string', default='0.0.0.0')

# port for ec2 api to listen (integer value)
nova.param('ec2_listen_port', type='integer', default='8773')

# Number of workers for EC2 API service (integer value)
nova.param('ec2_workers', type='integer', default='<None>')

# IP address for OpenStack API to listen (string value)
nova.param('osapi_compute_listen', type='string', default='0.0.0.0')

# list port for osapi compute (integer value)
nova.param('osapi_compute_listen_port', type='integer', default='8774')

# Number of workers for OpenStack API service (integer value)
nova.param('osapi_compute_workers', type='integer', default='<None>')

# OpenStack metadata service manager (string value)
nova.param('metadata_manager', type='string', default='nova.api.manager.MetadataManager')

# IP address for metadata api to listen (string value)
nova.param('metadata_listen', type='string', default='0.0.0.0')

# port for metadata api to listen (integer value)
nova.param('metadata_listen_port', type='integer', default='8775')

# Number of workers for metadata service (integer value)
nova.param('metadata_workers', type='integer', default='<None>')

# full class name for the Manager for compute (string value)
nova.param('compute_manager', type='string', default='nova.compute.manager.ComputeManager')

# full class name for the Manager for console proxy (string
# value)
nova.param('console_manager', type='string', default='nova.console.manager.ConsoleProxyManager')

# full class name for the Manager for cert (string value)
nova.param('cert_manager', type='string', default='nova.cert.manager.CertManager')

# full class name for the Manager for network (string value)
nova.param('network_manager', type='string', default='nova.network.manager.VlanManager')

# full class name for the Manager for scheduler (string value)
nova.param('scheduler_manager', type='string', default='nova.scheduler.manager.SchedulerManager')

# maximum time since last check-in for up service (integer
# value)
nova.param('service_down_time', type='integer', default='60')

# File name of clean sqlite db (string value)
nova.param('sqlite_clean_db', type='string', default='clean.sqlite')

# Whether to log monkey patching (boolean value)
nova.param('monkey_patch', type='boolean', default='false')

# List of modules/decorators to monkey patch (list value)
nova.param('monkey_patch_modules', type='list', default='nova.api.ec2.cloud:nova.openstack.common.notifier.api.notify_decorator,nova.compute.api:nova.openstack.common.notifier.api.notify_decorator')

# Length of generated instance admin passwords (integer value)
nova.param('password_length', type='integer', default='12')

# Whether to disable inter-process locks (boolean value)
nova.param('disable_process_locking', type='boolean', default='false')

# time period to generate instance usages for.  Time period
# must be hour, day, month or year (string value)
nova.param('instance_usage_audit_period', type='string', default='month')

# Path to the rootwrap configuration file to use for running
# commands as root (string value)
nova.param('rootwrap_config', type='string', default='/etc/nova/rootwrap.conf')

# Explicitly specify the temporary working directory (string
# value)
nova.param('tempdir', type='string', default='<None>')

# File name for the paste.deploy config for nova-api (string
# value)
nova.param('api_paste_config', type='string', default='api-paste.ini')

# A python format string that is used as the template to
# generate log lines. The following values can be formatted
# into it: client_ip, date_time, request_line, status_code,
# body_length, wall_seconds. (string value)
nova.param('wsgi_log_format', type='string', default='%(client_ip)s "%(request_line)s" status: %(status_code)s len: %(body_length)s time: %(wall_seconds).7f')

# CA certificate file to use to verify connecting clients
# (string value)
nova.param('ssl_ca_file', type='string', default='<None>')

# SSL certificate of API server (string value)
nova.param('ssl_cert_file', type='string', default='<None>')

# SSL private key of API server (string value)
nova.param('ssl_key_file', type='string', default='<None>')

# Sets the value of TCP_KEEPIDLE in seconds for each server
# socket. Not supported on OS X. (integer value)
nova.param('tcp_keepidle', type='integer', default='600')

# whether to rate limit the api (boolean value)
nova.param('api_rate_limit', type='boolean', default='true')

# The strategy to use for auth: noauth or keystone. (string
# value)
nova.param('auth_strategy', type='string', default='noauth')

# Treat X-Forwarded-For as the canonical remote address. Only
# enable this if you have a sanitizing proxy. (boolean value)
nova.param('use_forwarded_for', type='boolean', default='false')

# Number of failed auths before lockout. (integer value)
nova.param('lockout_attempts', type='integer', default='5')

# Number of minutes to lockout if triggered. (integer value)
nova.param('lockout_minutes', type='integer', default='15')

# Number of minutes for lockout window. (integer value)
nova.param('lockout_window', type='integer', default='15')

# URL to get token from ec2 request. (string value)
nova.param('keystone_ec2_url', type='string', default='http://localhost:5000/v2.0/ec2tokens')

# Return the IP address as private dns hostname in describe
# instances (boolean value)
nova.param('ec2_private_dns_show_ip', type='boolean', default='false')

# Validate security group names according to EC2 specification
# (boolean value)
nova.param('ec2_strict_validation', type='boolean', default='true')

# Time in seconds before ec2 timestamp expires (integer value)
nova.param('ec2_timestamp_expiry', type='integer', default='300')

# the ip of the ec2 api server (string value)
nova.param('ec2_host', type='string', default='$my_ip')

# the internal ip of the ec2 api server (string value)
nova.param('ec2_dmz_host', type='string', default='$my_ip')

# the port of the ec2 api server (integer value)
nova.param('ec2_port', type='integer', default='8773')

# the protocol to use when connecting to the ec2 api server
# (http, https) (string value)
nova.param('ec2_scheme', type='http, https) (string', default='http')

# the path prefix used to call the ec2 api server (string
# value)
nova.param('ec2_path', type='string', default='/services/Cloud')

# list of region=fqdn pairs separated by commas (list value)
nova.param('region_list', type='list', default='')

# List of metadata versions to skip placing into the config
# drive (string value)
nova.param('config_drive_skip_versions', type='string', default='1.0 2007-01-19 2007-03-01 2007-08-29 2007-10-10 2007-12-15 2008-02-01 2008-09-01')

# Set flag to indicate Quantum will proxy metadata requests
# and resolve instance ids. (boolean value)
nova.param('service_quantum_metadata_proxy', type='boolean', default='false')

# Shared secret to validate proxies Quantum metadata requests
# (string value)
nova.param('quantum_metadata_proxy_shared_secret', type='string', default='')

# the maximum number of items returned in a single response
# from a collection resource (integer value)
nova.param('osapi_max_limit', type='integer', default='1000')

# Base URL that will be presented to users in links to the
# OpenStack Compute API (string value)
nova.param('osapi_compute_link_prefix', type='string', default='<None>')

# Base URL that will be presented to users in links to glance
# resources (string value)
nova.param('osapi_glance_link_prefix', type='string', default='<None>')

# Permit instance snapshot operations. (boolean value)
nova.param('allow_instance_snapshots', type='boolean', default='true')

# Specify list of extensions to load when using
# osapi_compute_extension option with
# nova.api.openstack.compute.contrib.select_extensions (list
# value)
nova.param('osapi_compute_ext_list', type='list', default='')

# Full path to fping. (string value)
nova.param('fping_path', type='string', default='/usr/sbin/fping')

# List of instance states that should hide network info (list
# value)
nova.param('osapi_hide_server_address_states', type='list', default='building')

# Enables or disables quotaing of tenant networks (boolean
# value)
nova.param('enable_network_quota', type='boolean', default='false')

# Control for checking for default networks (string value)
nova.param('use_quantum_default_nets', type='string', default='False')

# Default tenant id when creating quantum networks (string
# value)
nova.param('quantum_default_tenant_id', type='string', default='default')

# osapi compute extension to load (multi valued)
nova.param('osapi_compute_extension', type='multi', default='nova.api.openstack.compute.contrib.standard_extensions')

# Allows use of instance password during server creation
# (boolean value)
nova.param('enable_instance_password', type='boolean', default='true')

# the maximum body size per each osapi request(bytes) (integer
# value)
nova.param('osapi_max_request_body_size', type='bytes) (integer', default='114688')

# the topic cert nodes listen on (string value)
nova.param('cert_topic', type='string', default='cert')

# image id used when starting up a cloudpipe vpn server
# (string value)
nova.param('vpn_image_id', type='string', default='0')

# Instance type for vpn instances (string value)
nova.param('vpn_instance_type', type='string', default='m1.tiny')

# Template for cloudpipe instance boot script (string value)
nova.param('boot_script_template', type='string', default='$pybasedir/nova/cloudpipe/bootscript.template')

# Network to push into openvpn config (string value)
nova.param('dmz_net', type='string', default='10.0.0.0')

# Netmask to push into openvpn config (string value)
nova.param('dmz_mask', type='string', default='255.255.255.0')

# Suffix to add to project name for vpn key and secgroups
# (string value)
nova.param('vpn_key_suffix', type='string', default='-vpn')

# Memcached servers or None for in process cache. (list value)
nova.param('memcached_servers', type='list', default='<None>')

# The full class name of the compute API class to use (string
# value)
nova.param('compute_api_class', type='string', default='nova.compute.api.API')

# Allow destination machine to match source for resize. Useful
# when testing in single-host environments. (boolean value)
nova.param('allow_resize_to_same_host', type='boolean', default='false')

# availability zone to use when user doesn't specify one
# (string value)
nova.param('default_schedule_zone', type='string', default='<None>')

# These are image properties which a snapshot should not
# inherit from an instance (list value)
nova.param('non_inheritable_image_properties', type='list', default='cache_in_nova,bittorrent')

# kernel image that indicates not to use a kernel, but to use
# a raw disk image instead (string value)
nova.param('null_kernel', type='string', default='nokernel')

# When creating multiple instances with a single request using
# the os-multiple-create API extension, this template will be
# used to build the display name for each instance. The
# benefit is that the instances end up with different
# hostnames. To restore legacy behavior of every instance
# having the same name, set this option to "%(name)s".  Valid
# keys for the template are: name, uuid, count. (string value)
nova.param('multi_instance_display_name_template', type='name)s".  Valid keys for the template are: name, uuid, count. (string', default='%(name)s-%(uuid)s')

# default instance type to use, testing only (string value)
nova.param('default_instance_type', type='string', default='m1.small')

# Console proxy host to use to connect to instances on this
# host. (string value)
nova.param('console_host', type='string', default='nova')

# Name of network to use to set access ips for instances
# (string value)
nova.param('default_access_ip_network_name', type='string', default='<None>')

# Whether to batch up the application of IPTables rules during
# a host restart and apply all at the end of the init phase
# (boolean value)
nova.param('defer_iptables_apply', type='boolean', default='false')

# where instances are stored on disk (string value)
nova.param('instances_path', type='string', default='$state_path/instances')

# Generate periodic compute.instance.exists notifications
# (boolean value)
nova.param('instance_usage_audit', type='boolean', default='false')

# Number of 1 second retries needed in live_migration (integer
# value)
nova.param('live_migration_retry_count', type='integer', default='30')

# Whether to start guests that were running before the host
# rebooted (boolean value)
nova.param('resume_guests_state_on_host_boot', type='boolean', default='false')

# interval to pull bandwidth usage info (integer value)
nova.param('bandwidth_poll_interval', type='integer', default='600')

# Number of seconds between instance info_cache self healing
# updates (integer value)
nova.param('heal_instance_info_cache_interval', type='integer', default='60')

# Interval in seconds for querying the host status (integer
# value)
nova.param('host_state_interval', type='integer', default='120')

# Number of seconds to wait between runs of the image cache
# manager (integer value)
nova.param('image_cache_manager_interval', type='integer', default='2400')

# Interval in seconds for reclaiming deleted instances
# (integer value)
nova.param('reclaim_instance_interval', type='integer', default='0')

# Interval in seconds for gathering volume usages (integer
# value)
nova.param('volume_usage_poll_interval', type='integer', default='0')

# Action to take if a running deleted instance is
# detected.Valid options are 'noop', 'log' and 'reap'. Set to
# 'noop' to disable. (string value)
nova.param('running_deleted_instance_action', type='string', default='log')

# Number of seconds to wait between runs of the cleanup task.
# (integer value)
nova.param('running_deleted_instance_poll_interval', type='integer', default='1800')

# Number of seconds after being deleted when a running
# instance should be considered eligible for cleanup. (integer
# value)
nova.param('running_deleted_instance_timeout', type='integer', default='0')

# Automatically hard reboot an instance if it has been stuck
# in a rebooting state longer than N seconds. Set to 0 to
# disable. (integer value)
nova.param('reboot_timeout', type='integer', default='0')

# Amount of time in seconds an instance can be in BUILD before
# going into ERROR status.Set to 0 to disable. (integer value)
nova.param('instance_build_timeout', type='integer', default='0')

# Automatically unrescue an instance after N seconds. Set to 0
# to disable. (integer value)
nova.param('rescue_timeout', type='integer', default='0')

# Automatically confirm resizes after N seconds. Set to 0 to
# disable. (integer value)
nova.param('resize_confirm_window', type='integer', default='0')

# Amount of disk in MB to reserve for the host (integer value)
nova.param('reserved_host_disk_mb', type='integer', default='0')

# Amount of memory in MB to reserve for the host (integer
# value)
nova.param('reserved_host_memory_mb', type='integer', default='512')

# Class that will manage stats for the local compute host
# (string value)
nova.param('compute_stats_class', type='string', default='nova.compute.stats.Stats')

# the topic compute nodes listen on (string value)
nova.param('compute_topic', type='string', default='compute')

# Driver to use for the console proxy (string value)
nova.param('console_driver', type='string', default='nova.console.xvp.XVPConsoleProxy')

# Stub calls to compute worker for tests (boolean value)
nova.param('stub_compute', type='boolean', default='false')

# Publicly visible name for this console host (string value)
nova.param('console_public_hostname', type='string', default='nova')

# the topic console proxy nodes listen on (string value)
nova.param('console_topic', type='string', default='console')

# port for VMware VMRC connections (integer value)
nova.param('console_vmrc_port', type='integer', default='443')

# number of retries for retrieving VMRC information (integer
# value)
nova.param('console_vmrc_error_retries', type='integer', default='10')

# XVP conf template (string value)
nova.param('console_xvp_conf_template', type='string', default='$pybasedir/nova/console/xvp.conf.template')

# generated XVP conf file (string value)
nova.param('console_xvp_conf', type='string', default='/etc/xvp.conf')

# XVP master process pid file (string value)
nova.param('console_xvp_pid', type='string', default='/var/run/xvp.pid')

# XVP log file (string value)
nova.param('console_xvp_log', type='string', default='/var/log/xvp.log')

# port for XVP to multiplex VNC connections on (integer value)
nova.param('console_xvp_multiplex_port', type='integer', default='5900')

# the topic console auth proxy nodes listen on (string value)
nova.param('consoleauth_topic', type='string', default='consoleauth')

# How many seconds before deleting tokens (integer value)
nova.param('console_token_ttl', type='integer', default='600')

# Manager for console auth (string value)
nova.param('consoleauth_manager', type='string', default='nova.consoleauth.manager.ConsoleAuthManager')

# Services to be added to the available pool on create
# (boolean value)
nova.param('enable_new_services', type='boolean', default='true')

# Template string to be used to generate instance names
# (string value)
nova.param('instance_name_template', type='string', default='instance-%08x')

# Template string to be used to generate snapshot names
# (string value)
nova.param('snapshot_name_template', type='string', default='snapshot-%s')

# driver to use for database access (string value)
nova.param('db_driver', type='string', default='nova.db')

# When set, compute API will consider duplicate hostnames
# invalid within the specified scope, regardless of case.
# Should be empty, "project" or "global". (string value)
nova.param('osapi_compute_unique_server_name_scope', type='string', default='')

# default glance hostname or ip (string value)
nova.param('glance_host', type='string', default='$my_ip')

# default glance port (integer value)
nova.param('glance_port', type='integer', default='9292')

# Default protocol to use when connecting to glance. Set to
# https for SSL. (string value)
nova.param('glance_protocol', type='string', default='http')

# A list of the glance api servers available to nova. Prefix
# with https:// for ssl-based glance api servers.
# ([hostname|ip]:port) (list value)
nova.param('glance_api_servers', type='[hostname|ip]:port) (list', default='$glance_host:$glance_port')

# Allow to perform insecure SSL (https) requests to glance
# (boolean value)
nova.param('glance_api_insecure', type='https) requests to glance (boolean', default='false')

# Number retries when downloading an image from glance
# (integer value)
nova.param('glance_num_retries', type='integer', default='0')

# A list of url scheme that can be downloaded directly via the
# direct_url.  Currently supported schemes: [file]. (list
# value)
nova.param('allowed_direct_url_schemes', type='list', default='')

# parent dir for tempdir used for image decryption (string
# value)
nova.param('image_decryption_dir', type='string', default='/tmp')

# hostname or ip for openstack to use when accessing the s3
# api (string value)
nova.param('s3_host', type='string', default='$my_ip')

# port used when accessing the s3 api (integer value)
nova.param('s3_port', type='integer', default='3333')

# access key to use for s3 server for images (string value)
nova.param('s3_access_key', type='string', default='notchecked')

# secret key to use for s3 server for images (string value)
nova.param('s3_secret_key', type='string', default='notchecked')

# whether to use ssl when talking to s3 (boolean value)
nova.param('s3_use_ssl', type='boolean', default='false')

# whether to affix the tenant id to the access key when
# downloading from s3 (boolean value)
nova.param('s3_affix_tenant', type='boolean', default='false')

# Backend to use for IPv6 generation (string value)
nova.param('ipv6_backend', type='string', default='rfc2462')

# The full class name of the network API class to use (string
# value)
nova.param('network_api_class', type='string', default='nova.network.api.API')

# Driver to use for network creation (string value)
nova.param('network_driver', type='string', default='nova.network.linux_net')

# Default pool for floating ips (string value)
nova.param('default_floating_pool', type='string', default='nova')

# Autoassigning floating ip to VM (boolean value)
nova.param('auto_assign_floating_ip', type='boolean', default='false')

# full class name for the DNS Manager for floating IPs (string
# value)
nova.param('floating_ip_dns_manager', type='string', default='nova.network.noop_dns_driver.NoopDNSDriver')

# full class name for the DNS Manager for instance IPs (string
# value)
nova.param('instance_dns_manager', type='string', default='nova.network.noop_dns_driver.NoopDNSDriver')

# full class name for the DNS Zone for instance IPs (string
# value)
nova.param('instance_dns_domain', type='string', default='')

# URL for ldap server which will store dns entries (string
# value)
nova.param('ldap_dns_url', type='string', default='ldap://ldap.example.com:389')

# user for ldap DNS (string value)
nova.param('ldap_dns_user', type='string', default='uid')

# password for ldap DNS (string value)
nova.param('ldap_dns_password', type='string', default='password')

# Hostmaster for ldap dns driver Statement of Authority
# (string value)
nova.param('ldap_dns_soa_hostmaster', type='string', default='hostmaster@example.org')

# DNS Servers for ldap dns driver (multi valued)
nova.param('ldap_dns_servers', type='multi', default='dns.example.org')

# Base DN for DNS entries in ldap (string value)
nova.param('ldap_dns_base_dn', type='string', default='ou')

# Refresh interval (in seconds) for ldap dns driver Statement
# of Authority (string value)
nova.param('ldap_dns_soa_refresh', type='in seconds) for ldap dns driver Statement of Authority (string', default='1800')

# Retry interval (in seconds) for ldap dns driver Statement of
# Authority (string value)
nova.param('ldap_dns_soa_retry', type='in seconds) for ldap dns driver Statement of Authority (string', default='3600')

# Expiry interval (in seconds) for ldap dns driver Statement
# of Authority (string value)
nova.param('ldap_dns_soa_expiry', type='in seconds) for ldap dns driver Statement of Authority (string', default='86400')

# Minimum interval (in seconds) for ldap dns driver Statement
# of Authority (string value)
nova.param('ldap_dns_soa_minimum', type='in seconds) for ldap dns driver Statement of Authority (string', default='7200')

# location of flagfiles for dhcpbridge (multi valued)
nova.param('dhcpbridge_flagfile', type='multi', default='/etc/nova/nova-dhcpbridge.conf')

# Location to keep network config files (string value)
nova.param('networks_path', type='string', default='$state_path/networks')

# Interface for public IP addresses (string value)
nova.param('public_interface', type='string', default='eth0')

# MTU setting for vlan (string value)
nova.param('network_device_mtu', type='string', default='<None>')

# location of nova-dhcpbridge (string value)
nova.param('dhcpbridge', type='string', default='$bindir/nova-dhcpbridge')

# Public IP of network host (string value)
nova.param('routing_source_ip', type='string', default='$my_ip')

# Lifetime of a DHCP lease in seconds (integer value)
nova.param('dhcp_lease_time', type='integer', default='120')

# if set, uses specific dns server for dnsmasq. Canbe
# specified multiple times. (multi valued)
nova.param('dns_server', type='multi', default='')

# if set, uses the dns1 and dns2 from the network ref.as dns
# servers. (boolean value)
nova.param('use_network_dns_servers', type='boolean', default='false')

# A list of dmz range that should be accepted (list value)
nova.param('dmz_cidr', type='list', default='')

# Traffic to this range will always be snatted to the fallback
# ip, even if it would normally be bridged out of the node.
# Can be specified multiple times. (multi valued)
nova.param('force_snat_range', type='multi', default='')

# Override the default dnsmasq settings with this file (string
# value)
nova.param('dnsmasq_config_file', type='string', default='')

# Driver used to create ethernet devices. (string value)
nova.param('linuxnet_interface_driver', type='string', default='nova.network.linux_net.LinuxBridgeInterfaceDriver')

# Name of Open vSwitch bridge used with linuxnet (string
# value)
nova.param('linuxnet_ovs_integration_bridge', type='string', default='br-int')

# send gratuitous ARPs for HA setup (boolean value)
nova.param('send_arp_for_ha', type='boolean', default='false')

# send this many gratuitous ARPs for HA setup (integer value)
nova.param('send_arp_for_ha_count', type='integer', default='3')

# Use single default gateway. Only first nic of vm will get
# default gateway from dhcp server (boolean value)
nova.param('use_single_default_gateway', type='boolean', default='false')

# An interface that bridges can forward to. If this is set to
# all then all traffic will be forwarded. Can be specified
# multiple times. (multi valued)
nova.param('forward_bridge_interface', type='multi', default='all')

# the ip for the metadata api server (string value)
nova.param('metadata_host', type='string', default='$my_ip')

# the port for the metadata api port (integer value)
nova.param('metadata_port', type='integer', default='8775')

# Regular expression to match iptables rule that shouldalways
# be on the top. (string value)
nova.param('iptables_top_regex', type='string', default='')

# Regular expression to match iptables rule that shouldalways
# be on the bottom. (string value)
nova.param('iptables_bottom_regex', type='string', default='')

# Bridge for simple network instances (string value)
nova.param('flat_network_bridge', type='string', default='<None>')

# Dns for simple network (string value)
nova.param('flat_network_dns', type='string', default='8.8.4.4')

# Whether to attempt to inject network setup into guest
# (boolean value)
nova.param('flat_injected', type='boolean', default='false')

# FlatDhcp will bridge into this interface if set (string
# value)
nova.param('flat_interface', type='string', default='<None>')

# First VLAN for private networks (integer value)
nova.param('vlan_start', type='integer', default='100')

# vlans will bridge into this interface if set (string value)
nova.param('vlan_interface', type='string', default='<None>')

# Number of networks to support (integer value)
nova.param('num_networks', type='integer', default='1')

# Public IP for the cloudpipe VPN servers (string value)
nova.param('vpn_ip', type='string', default='$my_ip')

# First Vpn port for private networks (integer value)
nova.param('vpn_start', type='integer', default='1000')

# Number of addresses in each private subnet (integer value)
nova.param('network_size', type='integer', default='256')

# Fixed IP address block (string value)
nova.param('fixed_range', type='string', default='10.0.0.0/8')

# Fixed IPv6 address block (string value)
nova.param('fixed_range_v6', type='string', default='fd00::/48')

# Default IPv4 gateway (string value)
nova.param('gateway', type='string', default='<None>')

# Default IPv6 gateway (string value)
nova.param('gateway_v6', type='string', default='<None>')

# Number of addresses reserved for vpn clients (integer value)
nova.param('cnt_vpn_clients', type='integer', default='0')

# Seconds after which a deallocated ip is disassociated
# (integer value)
nova.param('fixed_ip_disassociate_timeout', type='integer', default='600')

# Number of attempts to create unique mac address (integer
# value)
nova.param('create_unique_mac_address_attempts', type='integer', default='5')

# If passed, use fake network devices and addresses (boolean
# value)
nova.param('fake_network', type='boolean', default='false')

# If True, skip using the queue and make local calls (boolean
# value)
nova.param('fake_call', type='boolean', default='false')

# If True, unused gateway devices (VLAN and bridge) are
# deleted in VLAN network mode with multi hosted networks
# (boolean value)
nova.param('teardown_unused_network_gateway', type='VLAN and bridge) are deleted in VLAN network mode with multi hosted networks (boolean', default='false')

# If True, send a dhcp release on instance termination
# (boolean value)
nova.param('force_dhcp_release', type='boolean', default='false')

# If True in multi_host mode, all compute hosts share the same
# dhcp address. (boolean value)
nova.param('share_dhcp_address', type='boolean', default='false')

# If True, when a DNS entry must be updated, it sends a fanout
# cast to all network hosts to update their DNS entries in
# multi host mode (boolean value)
nova.param('update_dns_entries', type='boolean', default='false')

# Number of seconds to wait between runs of updates to DNS
# entries. (integer value)
nova.param('dns_update_periodic_interval', type='integer', default='-1')

# domain to use for building the hostnames (string value)
nova.param('dhcp_domain', type='string', default='novalocal')

# Indicates underlying L3 management library (string value)
nova.param('l3_lib', type='string', default='nova.network.l3.LinuxNetL3')

# URL for connecting to quantum (string value)
nova.param('quantum_url', type='string', default='http://127.0.0.1:9696')

# timeout value for connecting to quantum in seconds (integer
# value)
nova.param('quantum_url_timeout', type='integer', default='30')

# username for connecting to quantum in admin context (string
# value)
nova.param('quantum_admin_username', type='string', default='<None>')

# password for connecting to quantum in admin context (string
# value)
nova.param('quantum_admin_password', type='string', default='<None>')

# tenant name for connecting to quantum in admin context
# (string value)
nova.param('quantum_admin_tenant_name', type='string', default='<None>')

# region name for connecting to quantum in admin context
# (string value)
nova.param('quantum_region_name', type='string', default='<None>')

# auth url for connecting to quantum in admin context (string
# value)
nova.param('quantum_admin_auth_url', type='string', default='http://localhost:5000/v2.0')

# if set, ignore any SSL validation issues (boolean value)
nova.param('quantum_api_insecure', type='boolean', default='false')

# auth strategy for connecting to quantum in admin context
# (string value)
nova.param('quantum_auth_strategy', type='string', default='keystone')

# Name of Integration Bridge used by Open vSwitch (string
# value)
nova.param('quantum_ovs_bridge', type='string', default='br-int')

# Number of seconds before querying quantum for extensions
# (integer value)
nova.param('quantum_extension_sync_interval', type='integer', default='600')

# the topic network nodes listen on (string value)
nova.param('network_topic', type='string', default='network')

# Default value for multi_host in networks. Also, if set, some
# rpc network calls will be sent directly to host. (boolean
# value)
nova.param('multi_host', type='boolean', default='false')

# The full class name of the security API class (string value)
nova.param('security_group_api', type='string', default='nova')

# The full class name of the security group handler class
# (string value)
nova.param('security_group_handler', type='string', default='nova.network.sg.NullSecurityGroupHandler')

# Queues to delete (multi valued)
nova.param('queues', type='multi', default='')

# delete nova exchange too. (boolean value)
nova.param('delete_exchange', type='boolean', default='false')

# Record sessions to FILE.[session_number] (boolean value)
nova.param('record', type='boolean', default='false')

# Become a daemon (background process) (boolean value)
nova.param('daemon', type='background process) (boolean', default='false')

# Disallow non-encrypted connections (boolean value)
nova.param('ssl_only', type='boolean', default='false')

# Source is ipv6 (boolean value)
nova.param('source_is_ipv6', type='boolean', default='false')

# SSL certificate file (string value)
nova.param('cert', type='string', default='self.pem')

# SSL key file (if separate from cert) (string value)
nova.param('key', type='if separate from cert) (string', default='<None>')

# Run webserver on same port. Serve files from DIR. (string
# value)
nova.param('web', type='string', default='/usr/share/novnc')

# Host on which to listen for incoming requests (string value)
nova.param('novncproxy_host', type='string', default='0.0.0.0')

# Port on which to listen for incoming requests (integer
# value)
nova.param('novncproxy_port', type='integer', default='6080')

# path to s3 buckets (string value)
nova.param('buckets_path', type='string', default='$state_path/buckets')

# IP address for S3 API to listen (string value)
nova.param('s3_listen', type='string', default='0.0.0.0')

# port for s3 api to listen (integer value)
nova.param('s3_listen_port', type='integer', default='3333')

# The backend to use for db (string value)
nova.param('db_backend', type='string', default='sqlalchemy')

# Enable the experimental use of thread pooling for all DB API
# calls (boolean value)
nova.param('dbapi_use_tpool', type='boolean', default='false')

# The SQLAlchemy connection string used to connect to the
# database (string value)
nova.param('sql_connection', type='string', default='sqlite:////nova/openstack/common/db/$sqlite_db')

# the filename to use with sqlite (string value)
nova.param('sqlite_db', type='string', default='nova.sqlite')

# timeout before idle sql connections are reaped (integer
# value)
nova.param('sql_idle_timeout', type='integer', default='3600')

# If passed, use synchronous mode for sqlite (boolean value)
nova.param('sqlite_synchronous', type='boolean', default='true')

# Minimum number of SQL connections to keep open in a pool
# (integer value)
nova.param('sql_min_pool_size', type='integer', default='1')

# Maximum number of SQL connections to keep open in a pool
# (integer value)
nova.param('sql_max_pool_size', type='integer', default='5')

# maximum db connection retries during startup. (setting -1
# implies an infinite retry count) (integer value)
nova.param('sql_max_retries', type='setting -1 implies an infinite retry count) (integer', default='10')

# interval between retries of opening a sql connection
# (integer value)
nova.param('sql_retry_interval', type='integer', default='10')

# If set, use this value for max_overflow with sqlalchemy
# (integer value)
nova.param('sql_max_overflow', type='integer', default='<None>')

# Verbosity of SQL debugging information. 0=None,
# 100=Everything (integer value)
nova.param('sql_connection_debug', type='integer', default='0')

# Add python stack traces to SQL as comment strings (boolean
# value)
nova.param('sql_connection_trace', type='boolean', default='false')

# port for eventlet backdoor to listen (integer value)
nova.param('backdoor_port', type='integer', default='<None>')

# Whether to disable inter-process locks (boolean value)
nova.param('disable_process_locking', type='boolean', default='false')

# Directory to use for lock files. Default to a temp directory
# (string value)
nova.param('lock_path', type='string', default='<None>')

# Print debugging output (set logging level to DEBUG instead
# of default WARNING level). (boolean value)
nova.param('debug', type='set logging level to DEBUG instead of default WARNING level). (boolean', default='false')

# Print more verbose output (set logging level to INFO instead
# of default WARNING level). (boolean value)
nova.param('verbose', type='set logging level to INFO instead of default WARNING level). (boolean', default='false')

# Log output to standard error (boolean value)
nova.param('use_stderr', type='boolean', default='true')

# Default file mode used when creating log files (string
# value)
nova.param('logfile_mode', type='string', default='0644')

# format string to use for log messages with context (string
# value)
nova.param('logging_context_format_string', type='string', default='%(asctime)s.%(msecs)03d %(levelname)s %(name)s [%(request_id)s %(user)s %(tenant)s] %(instance)s%(message)s')

# format string to use for log messages without context
# (string value)
nova.param('logging_default_format_string', type='string', default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s')

# data to append to log format when level is DEBUG (string
# value)
nova.param('logging_debug_format_suffix', type='string', default='%(funcName)s %(pathname)s:%(lineno)d')

# prefix each line of exception output with this format
# (string value)
nova.param('logging_exception_prefix', type='string', default='%(asctime)s.%(msecs)03d %(process)d TRACE %(name)s %(instance)s')

# list of logger=LEVEL pairs (list value)
nova.param('default_log_levels', type='list', default='amqplib')

# publish error events (boolean value)
nova.param('publish_errors', type='boolean', default='false')

# make deprecations fatal (boolean value)
nova.param('fatal_deprecations', type='boolean', default='false')

# If an instance is passed with the log message, format it
# like this (string value)
nova.param('instance_format', type='string', default='"[instance: %(uuid)s] "')

# If an instance UUID is passed with the log message, format
# it like this (string value)
nova.param('instance_uuid_format', type='string', default='"[instance: %(uuid)s] "')

# If this option is specified, the logging configuration file
# specified is used and overrides any other logging options
# specified. Please see the Python logging module
# documentation for details on logging configuration files.
# (string value)
nova.param('log_config', type='string', default='<None>')

# A logging.Formatter log message format string which may use
# any of the available logging.LogRecord attributes. Default:
# %(default)s (string value)
nova.param('log_format', type='default)s (string', default='%(asctime)s %(levelname)8s [%(name)s] %(message)s')

# Format string for %%(asctime)s in log records. Default:
# %(default)s (string value)
nova.param('log_date_format', type='asctime)s in log records. Default: %(default)s (string', default='%Y-%m-%d %H:%M:%S')

# (Optional) Name of log file to output to. If not set,
# logging will go to stdout. (string value)
nova.param('log_file', type='Optional) Name of log file to output to. If not set, logging will go to stdout. (string', default='<None>')

# (Optional) The directory to keep log files in (will be
# prepended to --log-file) (string value)
nova.param('log_dir', type='Optional) The directory to keep log files in (will be prepended to --log-file) (string', default='<None>')

# Use syslog for logging. (boolean value)
nova.param('use_syslog', type='boolean', default='false')

# syslog facility to receive log lines (string value)
nova.param('syslog_log_facility', type='string', default='LOG_USER')

# Driver or drivers to handle sending notifications (multi
# valued)
nova.param('notification_driver', type='multi', default='')

# Default notification level for outgoing notifications
# (string value)
nova.param('default_notification_level', type='string', default='INFO')

# Default publisher_id for outgoing notifications (string
# value)
nova.param('default_publisher_id', type='string', default='$host')

# AMQP topic used for openstack notifications (list value)
nova.param('notification_topics', type='list', default='notifications')

# The messaging module to use, defaults to kombu. (string
# value)
nova.param('rpc_backend', type='string', default='nova.openstack.common.rpc.impl_kombu')

# Size of RPC thread pool (integer value)
nova.param('rpc_thread_pool_size', type='integer', default='64')

# Size of RPC connection pool (integer value)
nova.param('rpc_conn_pool_size', type='integer', default='30')

# Seconds to wait for a response from call or multicall
# (integer value)
nova.param('rpc_response_timeout', type='integer', default='60')

# Seconds to wait before a cast expires (TTL). Only supported
# by impl_zmq. (integer value)
nova.param('rpc_cast_timeout', type='TTL). Only supported by impl_zmq. (integer', default='30')

# Modules of exceptions that are permitted to be recreatedupon
# receiving exception data from an rpc call. (list value)
nova.param('allowed_rpc_exception_modules', type='list', default='nova.openstack.common.exception,nova.exception,cinder.exception,exceptions')

# If passed, use a fake RabbitMQ provider (boolean value)
nova.param('fake_rabbit', type='boolean', default='false')

# AMQP exchange to connect to if using RabbitMQ or Qpid
# (string value)
nova.param('control_exchange', type='string', default='openstack')

# Enable a fast single reply queue if using AMQP based RPC
# like RabbitMQ or Qpid. (boolean value)
nova.param('amqp_rpc_single_reply_queue', type='boolean', default='false')

# SSL version to use (valid only if SSL enabled) (string
# value)
nova.param('kombu_ssl_version', type='valid only if SSL enabled) (string', default='')

# SSL key file (valid only if SSL enabled) (string value)
nova.param('kombu_ssl_keyfile', type='valid only if SSL enabled) (string', default='')

# SSL cert file (valid only if SSL enabled) (string value)
nova.param('kombu_ssl_certfile', type='valid only if SSL enabled) (string', default='')

# SSL certification authority file (valid only if SSL enabled)
# (string value)
nova.param('kombu_ssl_ca_certs', type='valid only if SSL enabled) (string', default='')

# The RabbitMQ broker address where a single node is used
# (string value)
nova.param('rabbit_host', type='string', default='localhost')

# The RabbitMQ broker port where a single node is used
# (integer value)
nova.param('rabbit_port', type='integer', default='5672')

# RabbitMQ HA cluster host:port pairs (list value)
nova.param('rabbit_hosts', type='list', default='$rabbit_host:$rabbit_port')

# connect over SSL for RabbitMQ (boolean value)
nova.param('rabbit_use_ssl', type='boolean', default='false')

# the RabbitMQ userid (string value)
nova.param('rabbit_userid', type='string', default='guest')

# the RabbitMQ password (string value)
nova.param('rabbit_password', type='string', default='guest')

# the RabbitMQ virtual host (string value)
nova.param('rabbit_virtual_host', type='string', default='/')

# how frequently to retry connecting with RabbitMQ (integer
# value)
nova.param('rabbit_retry_interval', type='integer', default='1')

# how long to backoff for between retries when connecting to
# RabbitMQ (integer value)
nova.param('rabbit_retry_backoff', type='integer', default='2')

# maximum retries with trying to connect to RabbitMQ (the
# default of 0 implies an infinite retry count) (integer
# value)
nova.param('rabbit_max_retries', type='the default of 0 implies an infinite retry count) (integer', default='0')

# use durable queues in RabbitMQ (boolean value)
nova.param('rabbit_durable_queues', type='boolean', default='false')

# use H/A queues in RabbitMQ (x-ha-policy: all).You need to
# wipe RabbitMQ database when changing this option. (boolean
# value)
nova.param('rabbit_ha_queues', type='x-ha-policy: all).You need to wipe RabbitMQ database when changing this option. (boolean', default='false')

# Qpid broker hostname (string value)
nova.param('qpid_hostname', type='string', default='localhost')

# Qpid broker port (string value)
nova.param('qpid_port', type='string', default='5672')

# Qpid HA cluster host:port pairs (list value)
nova.param('qpid_hosts', type='list', default='$qpid_hostname:$qpid_port')

# Username for qpid connection (string value)
nova.param('qpid_username', type='string', default='')

# Password for qpid connection (string value)
nova.param('qpid_password', type='string', default='')

# Space separated list of SASL mechanisms to use for auth
# (string value)
nova.param('qpid_sasl_mechanisms', type='string', default='')

# Seconds between connection keepalive heartbeats (integer
# value)
nova.param('qpid_heartbeat', type='integer', default='60')

# Transport to use, either 'tcp' or 'ssl' (string value)
nova.param('qpid_protocol', type='string', default='tcp')

# Disable Nagle algorithm (boolean value)
nova.param('qpid_tcp_nodelay', type='boolean', default='true')

# ZeroMQ bind address. Should be a wildcard (*), an ethernet
# interface, or IP. The "host" option should point or resolve
# to this address. (string value)
nova.param('rpc_zmq_bind_address', type='*), an ethernet interface, or IP. The "host" option should point or resolve to this address. (string', default='*')

# MatchMaker driver (string value)
nova.param('rpc_zmq_matchmaker', type='string', default='nova.openstack.common.rpc.matchmaker.MatchMakerLocalhost')

# ZeroMQ receiver listening port (integer value)
nova.param('rpc_zmq_port', type='integer', default='9501')

# Number of ZeroMQ contexts, defaults to 1 (integer value)
nova.param('rpc_zmq_contexts', type='integer', default='1')

# Maximum number of ingress messages to locally buffer per
# topic. Default is unlimited. (integer value)
nova.param('rpc_zmq_topic_backlog', type='integer', default='<None>')

# Directory for holding IPC sockets (string value)
nova.param('rpc_zmq_ipc_dir', type='string', default='/var/run/openstack')

# Name of this node. Must be a valid hostname, FQDN, or IP
# address. Must match "host" option, if running Nova. (string
# value)
nova.param('rpc_zmq_host', type='string', default='sorcha')

# Matchmaker ring file (JSON) (string value)
nova.param('matchmaker_ringfile', type='JSON) (string', default='/etc/nova/matchmaker_ring.json')

# The scheduler host manager class to use (string value)
nova.param('scheduler_host_manager', type='string', default='nova.scheduler.host_manager.HostManager')

# Maximum number of attempts to schedule an instance (integer
# value)
nova.param('scheduler_max_attempts', type='integer', default='3')

# New instances will be scheduled on a host chosen randomly
# from a subset of the N best hosts. This property defines the
# subset size that a host is chosen from. A value of 1 chooses
# the first host returned by the weighing functions. This
# value must be at least 1. Any value less than 1 will be
# ignored, and 1 will be used instead (integer value)
nova.param('scheduler_host_subset_size', type='integer', default='1')

# Virtual CPU to Physical CPU allocation ratio (floating point
# value)
nova.param('cpu_allocation_ratio', type='floating point', default='16.0')

# virtual disk to physical disk allocation ratio (floating
# point value)
nova.param('disk_allocation_ratio', type='floating point', default='1.0')

# Ignore hosts that have too many
# builds/resizes/snaps/migrations (integer value)
nova.param('max_io_ops_per_host', type='integer', default='8')

# Images to run on isolated host (list value)
nova.param('isolated_images', type='list', default='')

# Host reserved for specific images (list value)
nova.param('isolated_hosts', type='list', default='')

# Ignore hosts that have too many instances (integer value)
nova.param('max_instances_per_host', type='integer', default='50')

# virtual ram to physical ram allocation ratio (floating point
# value)
nova.param('ram_allocation_ratio', type='floating point', default='1.5')

# Filter classes available to the scheduler which may be
# specified more than once.  An entry of
# "nova.scheduler.filters.standard_filters" maps to all
# filters included with nova. (multi valued)
nova.param('scheduler_available_filters', type='multi', default='nova.scheduler.filters.all_filters')

# Which filter class names to use for filtering hosts when not
# specified in the request. (list value)
nova.param('scheduler_default_filters', type='list', default='RetryFilter,AvailabilityZoneFilter,RamFilter,ComputeFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter')

# Which weight class names to use for weighing hosts (list
# value)
nova.param('scheduler_weight_classes', type='list', default='nova.scheduler.weights.all_weighers')

# Default driver to use for the scheduler (string value)
nova.param('scheduler_driver', type='string', default='nova.scheduler.filter_scheduler.FilterScheduler')

# Driver to use for scheduling compute calls (string value)
nova.param('compute_scheduler_driver', type='string', default='nova.scheduler.filter_scheduler.FilterScheduler')

# Default driver to use for scheduling calls (string value)
nova.param('default_scheduler_driver', type='string', default='nova.scheduler.chance.ChanceScheduler')

# the topic scheduler nodes listen on (string value)
nova.param('scheduler_topic', type='string', default='scheduler')

# Absolute path to scheduler configuration JSON file. (string
# value)
nova.param('scheduler_json_config_location', type='string', default='')

# Which cost functions the LeastCostScheduler should use (list
# value)
nova.param('least_cost_functions', type='list', default='<None>')

# How much weight to give the noop cost function (floating
# point value)
nova.param('noop_cost_fn_weight', type='floating point', default='1.0')

# How much weight to give the fill-first cost function. A
# negative value will reverse behavior: e.g. spread-first
# (floating point value)
nova.param('compute_fill_first_cost_fn_weight', type='floating point', default='<None>')

# Multiplier used for weighing ram.  Negative numbers mean to
# stack vs spread. (floating point value)
nova.param('ram_weight_multiplier', type='floating point', default='1.0')

# The driver for servicegroup service (valid options are: db,
# zk, mc) (string value)
nova.param('servicegroup_driver', type='valid options are: db, zk, mc) (string', default='db')

# Config drive format. One of iso9660 (default) or vfat
# (string value)
nova.param('config_drive_format', type='default) or vfat (string', default='iso9660')

# Where to put temporary files associated with config drive
# creation (string value)
nova.param('config_drive_tempdir', type='string', default='<None>')

# Set to force injection to take place on a config drive (if
# set, valid options are: always) (string value)
nova.param('force_config_drive', type='if set, valid options are: always) (string', default='<None>')

# Name and optionally path of the tool used for ISO image
# creation (string value)
nova.param('mkisofs_cmd', type='string', default='genisoimage')

# Template file for injected network (string value)
nova.param('injected_network_template', type='string', default='$pybasedir/nova/virt/interfaces.template')

# mkfs commands for ephemeral device. The format is
# <os_type>=<mkfs command> (multi valued)
nova.param('virt_mkfs', type='multi', default='default')

nova.param('virt_mkfs', type='string', default='linux')

nova.param('virt_mkfs', type='string', default='windows')

# time to wait for a NBD device coming up (integer value)
nova.param('timeout_nbd', type='integer', default='10')

# Driver to use for controlling virtualization. Options
# include: libvirt.LibvirtDriver, xenapi.XenAPIDriver,
# fake.FakeDriver, baremetal.BareMetalDriver,
# vmwareapi.VMWareESXDriver (string value)
nova.param('compute_driver', type='string', default='<None>')

# The default format an ephemeral_volume will be formatted
# with on creation. (string value)
nova.param('default_ephemeral_format', type='string', default='<None>')

# VM image preallocation mode: "none" => no storage
# provisioning is done up front, "space" => storage is fully
# allocated at instance start (string value)
nova.param('preallocate_images', type='string', default='none')

# Whether to use cow images (boolean value)
nova.param('use_cow_images', type='boolean', default='true')

# Firewall driver (defaults to hypervisor specific iptables
# driver) (string value)
nova.param('firewall_driver', type='defaults to hypervisor specific iptables driver) (string', default='<None>')

# Whether to allow network traffic from same network (boolean
# value)
nova.param('allow_same_net_traffic', type='boolean', default='true')

# External virtual switch Name, if not provided, the first
# external virtual switch is used (string value)
nova.param('vswitch_name', type='string', default='<None>')

# Required for live migration among hosts with different CPU
# features (boolean value)
nova.param('limit_cpu_features', type='boolean', default='false')

# Sets the admin password in the config drive image (boolean
# value)
nova.param('config_drive_inject_password', type='boolean', default='false')

# qemu-img is used to convert between different image types
# (string value)
nova.param('qemu_img_cmd', type='string', default='qemu-img.exe')

# Attaches the Config Drive image as a cdrom drive instead of
# a disk drive (boolean value)
nova.param('config_drive_cdrom', type='boolean', default='false')

# The number of times we retry on attaching volume  (integer
# value)
nova.param('hyperv_attaching_volume_retry_count', type='integer', default='10')

# The seconds to wait between an volume attachment attempt
# (integer value)
nova.param('hyperv_wait_between_attach_retry', type='integer', default='5')

# Force volumeutils v1 (boolean value)
nova.param('force_volumeutils_v1', type='boolean', default='false')

# Force backing images to raw format (boolean value)
nova.param('force_raw_images', type='boolean', default='true')

# Rescue ami image (string value)
nova.param('rescue_image_id', type='string', default='<None>')

# Rescue aki image (string value)
nova.param('rescue_kernel_id', type='string', default='<None>')

# Rescue ari image (string value)
nova.param('rescue_ramdisk_id', type='string', default='<None>')

# Libvirt domain type (valid options are: kvm, lxc, qemu, uml,
# xen) (string value)
nova.param('libvirt_type', type='valid options are: kvm, lxc, qemu, uml, xen) (string', default='kvm')

# Override the default libvirt URI (which is dependent on
# libvirt_type) (string value)
nova.param('libvirt_uri', type='which is dependent on libvirt_type) (string', default='')

# Inject the admin password at boot time, without an agent.
# (boolean value)
nova.param('libvirt_inject_password', type='boolean', default='false')

# Inject the ssh public key at boot time (boolean value)
nova.param('libvirt_inject_key', type='boolean', default='true')

# The partition to inject to : -2 => disable, -1 => inspect
# (libguestfs only), 0 => not partitioned, >0 => partition
# number (integer value)
nova.param('libvirt_inject_partition', type='libguestfs only), 0 => not partitioned, >0 => partition number (integer', default='1')

# Sync virtual and real mouse cursors in Windows VMs (boolean
# value)
nova.param('use_usb_tablet', type='boolean', default='true')

# Migration target URI (any included "%s" is replaced with the
# migration target hostname) (string value)
nova.param('live_migration_uri', type='any included "%s" is replaced with the migration target hostname) (string', default='qemu+tcp://%s/system')

# Migration flags to be set for live migration (string value)
nova.param('live_migration_flag', type='string', default='VIR_MIGRATE_UNDEFINE_SOURCE, VIR_MIGRATE_PEER2PEER')

# Migration flags to be set for block migration (string value)
nova.param('block_migration_flag', type='string', default='VIR_MIGRATE_UNDEFINE_SOURCE, VIR_MIGRATE_PEER2PEER, VIR_MIGRATE_NON_SHARED_INC')

# Maximum bandwidth to be used during migration, in Mbps
# (integer value)
nova.param('live_migration_bandwidth', type='integer', default='0')

# Snapshot image format (valid options are : raw, qcow2, vmdk,
# vdi). Defaults to same as source image (string value)
nova.param('snapshot_image_format', type='valid options are : raw, qcow2, vmdk, vdi). Defaults to same as source image (string', default='<None>')

# The libvirt VIF driver to configure the VIFs. (string value)
nova.param('libvirt_vif_driver', type='string', default='nova.virt.libvirt.vif.LibvirtGenericVIFDriver')

# Libvirt handlers for remote volumes. (list value)
nova.param('libvirt_volume_drivers', type='list', default='iscsi')

# Override the default disk prefix for the devices attached to
# a server, which is dependent on libvirt_type. (valid options
# are: sd, xvd, uvd, vd) (string value)
nova.param('libvirt_disk_prefix', type='valid options are: sd, xvd, uvd, vd) (string', default='<None>')

# Number of seconds to wait for instance to shut down after
# soft reboot request is made. We fall back to hard reboot if
# instance does not shutdown within this window. (integer
# value)
nova.param('libvirt_wait_soft_reboot_seconds', type='integer', default='120')

# Use a separated OS thread pool to realize non-blocking
# libvirt calls (boolean value)
nova.param('libvirt_nonblocking', type='boolean', default='true')

# Set to "host-model" to clone the host CPU feature flags; to
# "host-passthrough" to use the host CPU model exactly; to
# "custom" to use a named CPU model; to "none" to not set any
# CPU model. If libvirt_type="kvm|qemu", it will default to
# "host-model", otherwise it will default to "none" (string
# value)
nova.param('libvirt_cpu_mode', type='string', default='<None>')

# Set to a named libvirt CPU model (see names listed in
# /usr/share/libvirt/cpu_map.xml). Only has effect if
# libvirt_cpu_mode="custom" and libvirt_type="kvm|qemu"
# (string value)
nova.param('libvirt_cpu_model', type='see names listed in /usr/share/libvirt/cpu_map.xml). Only has effect if libvirt_cpu_mode="custom" and libvirt_type="kvm|qemu" (string', default='<None>')

# Location where libvirt driver will store snapshots before
# uploading them to image service (string value)
nova.param('libvirt_snapshots_directory', type='string', default='$instances_path/snapshots')

# Location where the Xen hvmloader is kept (string value)
nova.param('xen_hvmloader_path', type='string', default='/usr/lib/xen/boot/hvmloader')

# Specific cachemodes to use for different disk types e.g:
# ["file=directsync","block=none"] (list value)
nova.param('disk_cachemodes', type='list', default='')

# VM Images format. Acceptable values are: raw, qcow2, lvm,
# default. If default is specified, then use_cow_images flag
# is used instead of this one. (string value)
nova.param('libvirt_images_type', type='string', default='default')

# LVM Volume Group that is used for VM images, when you
# specify libvirt_images_type=lvm. (string value)
nova.param('libvirt_images_volume_group', type='string', default='<None>')

# Create sparse logical volumes (with virtualsize) if this
# flag is set to True. (boolean value)
nova.param('libvirt_sparse_logical_volumes', type='with virtualsize) if this flag is set to True. (boolean', default='false')

# The amount of storage (in megabytes) to allocate for LVM
# snapshot copy-on-write blocks. (integer value)
nova.param('libvirt_lvm_snapshot_size', type='in megabytes) to allocate for LVM snapshot copy-on-write blocks. (integer', default='1000')

# Where cached images are stored under $instances_path.This is
# NOT the full path - just a folder name.For per-compute-host
# cached images, set to _base_$my_ip (string value)
nova.param('base_dir_name', type='string', default='_base')

# Allows image information files to be stored in non-standard
# locations (string value)
nova.param('image_info_filename_pattern', type='string', default='$instances_path/$base_dir_name/%(image)s.info')

# Should unused base images be removed? (boolean value)
nova.param('remove_unused_base_images', type='boolean', default='true')

# Should unused kernel images be removed? This is only safe to
# enable if all compute nodes have been updated to support
# this option. This will enabled by default in future.
# (boolean value)
nova.param('remove_unused_kernels', type='boolean', default='false')

# Unused resized base images younger than this will not be
# removed (integer value)
nova.param('remove_unused_resized_minimum_age_seconds', type='integer', default='3600')

# Unused unresized base images younger than this will not be
# removed (integer value)
nova.param('remove_unused_original_minimum_age_seconds', type='integer', default='86400')

# Write a checksum for files in _base to disk (boolean value)
nova.param('checksum_base_images', type='boolean', default='false')

# How frequently to checksum base images (integer value)
nova.param('checksum_interval_seconds', type='integer', default='3600')

# Compress snapshot images when possible. This currently
# applies exclusively to qcow2 images (boolean value)
nova.param('libvirt_snapshot_compression', type='boolean', default='false')

# Name of Integration Bridge used by Open vSwitch (string
# value)
nova.param('libvirt_ovs_bridge', type='string', default='br-int')

# Use virtio for bridge interfaces with KVM/QEMU (boolean
# value)
nova.param('libvirt_use_virtio_for_bridges', type='boolean', default='true')

# number of times to rescan iSCSI target to find volume
# (integer value)
nova.param('num_iscsi_scan_tries', type='integer', default='3')

# the RADOS client name for accessing rbd volumes (string
# value)
nova.param('rbd_user', type='string', default='<None>')

# the libvirt uuid of the secret for the rbd_uservolumes
# (string value)
nova.param('rbd_secret_uuid', type='string', default='<None>')

# Dir where the nfs volume is mounted on the compute node
# (string value)
nova.param('nfs_mount_point_base', type='string', default='$state_path/mnt')

# Mount options passed to the nfs client. See section of the
# nfs man page for details (string value)
nova.param('nfs_mount_options', type='string', default='<None>')

# number of times to rediscover AoE target to find volume
# (integer value)
nova.param('num_aoe_discover_tries', type='integer', default='3')

# Dir where the glusterfs volume is mounted on the compute
# node (string value)
nova.param('glusterfs_mount_point_base', type='string', default='$state_path/mnt')

# use multipath connection of the iSCSI volume (boolean value)
nova.param('libvirt_iscsi_use_multipath', type='boolean', default='false')

# Path or URL to Scality SOFS configuration file (string
# value)
nova.param('scality_sofs_config', type='string', default='<None>')

# Base dir where Scality SOFS shall be mounted (string value)
nova.param('scality_sofs_mount_point', type='string', default='$state_path/scality')

# PowerVM manager type (ivm, hmc) (string value)
nova.param('powervm_mgr_type', type='ivm, hmc) (string', default='ivm')

# PowerVM manager host or ip (string value)
nova.param('powervm_mgr', type='string', default='<None>')

# PowerVM manager user name (string value)
nova.param('powervm_mgr_user', type='string', default='<None>')

# PowerVM manager user password (string value)
nova.param('powervm_mgr_passwd', type='string', default='<None>')

# PowerVM image remote path where images will be moved. Make
# sure this path can fit your biggest image in glance (string
# value)
nova.param('powervm_img_remote_path', type='string', default='/home/padmin')

# Local directory to download glance images to. Make sure this
# path can fit your biggest image in glance (string value)
nova.param('powervm_img_local_path', type='string', default='/tmp')

# URL for connection to VMware ESX/VC host. Required if
# compute_driver is vmwareapi.VMwareESXDriver or
# vmwareapi.VMwareVCDriver. (string value)
nova.param('vmwareapi_host_ip', type='string', default='<None>')

# Username for connection to VMware ESX/VC host. Used only if
# compute_driver is vmwareapi.VMwareESXDriver or
# vmwareapi.VMwareVCDriver. (string value)
nova.param('vmwareapi_host_username', type='string', default='<None>')

# Password for connection to VMware ESX/VC host. Used only if
# compute_driver is vmwareapi.VMwareESXDriver or
# vmwareapi.VMwareVCDriver. (string value)
nova.param('vmwareapi_host_password', type='string', default='<None>')

# Name of a VMware Cluster ComputeResource. Used only if
# compute_driver is vmwareapi.VMwareVCDriver. (string value)
nova.param('vmwareapi_cluster_name', type='string', default='<None>')

# The interval used for polling of remote tasks. Used only if
# compute_driver is vmwareapi.VMwareESXDriver or
# vmwareapi.VMwareVCDriver. (floating point value)
nova.param('vmwareapi_task_poll_interval', type='floating point', default='5.0')

# The number of times we retry on failures, e.g., socket
# error, etc. Used only if compute_driver is
# vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.
# (integer value)
nova.param('vmwareapi_api_retry_count', type='integer', default='10')

# VNC starting port (integer value)
nova.param('vnc_port', type='integer', default='5900')

# Total number of VNC ports (integer value)
nova.param('vnc_port_total', type='integer', default='10000')

# VNC password (string value)
nova.param('vnc_password', type='string', default='<None>')

# Whether to use linked clone (boolean value)
nova.param('use_linked_clone', type='boolean', default='true')

# Physical ethernet adapter name for vlan networking (string
# value)
nova.param('vmwareapi_vlan_interface', type='string', default='vmnic0')

# Optional VIM Service WSDL Location e.g
# http://<server>/vimService.wsdl
nova.param('vmwareapi_wsdl_loc', type='string', default='<None>')

# number of seconds to wait for agent reply (integer value)
nova.param('agent_timeout', type='integer', default='30')

# number of seconds to wait for agent to be fully operational
# (integer value)
nova.param('agent_version_timeout', type='integer', default='300')

# number of seconds to wait for agent reply to resetnetwork
# request (integer value)
nova.param('agent_resetnetwork_timeout', type='integer', default='60')

# Specifies the path in which the xenapi guest agent should be
# located. If the agent is present, network configuration is
# not injected into the image. Used if
# compute_driver=xenapi.XenAPIDriver and  flat_injected=True
# (string value)
nova.param('xenapi_agent_path', type='string', default='usr/sbin/xe-update-networking')

# Disable XenAPI agent. Reduces the amount of time it takes
# nova to detect that a VM has started, when that VM does not
# have the agent installed (boolean value)
nova.param('xenapi_disable_agent', type='boolean', default='false')

# URL for connection to XenServer/Xen Cloud Platform. Required
# if compute_driver=xenapi.XenAPIDriver (string value)
nova.param('xenapi_connection_url', type='string', default='<None>')

# Username for connection to XenServer/Xen Cloud Platform.
# Used only if compute_driver=xenapi.XenAPIDriver (string
# value)
nova.param('xenapi_connection_username', type='string', default='root')

# Password for connection to XenServer/Xen Cloud Platform.
# Used only if compute_driver=xenapi.XenAPIDriver (string
# value)
nova.param('xenapi_connection_password', type='string', default='<None>')

# Maximum number of concurrent XenAPI connections. Used only
# if compute_driver=xenapi.XenAPIDriver (integer value)
nova.param('xenapi_connection_concurrent', type='integer', default='5')

# The interval used for polling of coalescing vhds. Used only
# if compute_driver=xenapi.XenAPIDriver (floating point value)
nova.param('xenapi_vhd_coalesce_poll_interval', type='floating point', default='5.0')

# Ensure compute service is running on host XenAPI connects
# to. (boolean value)
nova.param('xenapi_check_host', type='boolean', default='true')

# Max number of times to poll for VHD to coalesce. Used only
# if compute_driver=xenapi.XenAPIDriver (integer value)
nova.param('xenapi_vhd_coalesce_max_attempts', type='integer', default='5')

# Base path to the storage repository (string value)
nova.param('xenapi_sr_base_path', type='string', default='/var/run/sr-mount')

# iSCSI Target Host (string value)
nova.param('target_host', type='string', default='<None>')

# iSCSI Target Port, 3260 Default (string value)
nova.param('target_port', type='string', default='3260')

# IQN Prefix (string value)
nova.param('iqn_prefix', type='string', default='iqn.2010-10.org.openstack')

# Used to enable the remapping of VBD dev (Works around an
# issue in Ubuntu Maverick) (boolean value)
nova.param('xenapi_remap_vbd_dev', type='Works around an issue in Ubuntu Maverick) (boolean', default='false')

# Specify prefix to remap VBD dev to (ex. /dev/xvdb ->
# /dev/sdb) (string value)
nova.param('xenapi_remap_vbd_dev_prefix', type='ex. /dev/xvdb -> /dev/sdb) (string', default='sd')

# Timeout in seconds for XenAPI login. (integer value)
nova.param('xenapi_login_timeout', type='integer', default='10')

# To use for hosts with different CPUs (boolean value)
nova.param('use_join_force', type='boolean', default='true')

# Name of Integration Bridge used by Open vSwitch (string
# value)
nova.param('xenapi_ovs_integration_bridge', type='string', default='xapi1')

# Cache glance images locally. `all` will cache all images,
# `some` will only cache images that have the image_property
# `cache_in_nova=True`, and `none` turns off caching entirely
# (string value)
nova.param('cache_images', type='string', default='all')

# Default OS type (string value)
nova.param('default_os_type', type='string', default='linux')

# Time to wait for a block device to be created (integer
# value)
nova.param('block_device_creation_timeout', type='integer', default='10')

# Maximum size in bytes of kernel or ramdisk images (integer
# value)
nova.param('max_kernel_ramdisk_size', type='integer', default='16777216')

# Filter for finding the SR to be used to install guest
# instances on. The default value is the Local Storage in
# default XenServer/XCP installations. To select an SR with a
# different matching criteria, you could set it to other-
# config:my_favorite_sr=true. On the other hand, to fall back
# on the Default SR, as displayed by XenCenter, set this flag
# to: default-sr:true (string value)
nova.param('sr_matching_filter', type='string', default='other-config:i18n-key')

# Whether to use sparse_copy for copying data on a resize down
# (False will use standard dd). This speeds up resizes down
# considerably since large runs of zeros won't have to be
# rsynced (boolean value)
nova.param('xenapi_sparse_copy', type='False will use standard dd). This speeds up resizes down considerably since large runs of zeros won't have to be rsynced (boolean', default='true')

# Maximum number of retries to unplug VBD (integer value)
nova.param('xenapi_num_vbd_unplug_retries', type='integer', default='10')

# Whether or not to download images via Bit Torrent
# (all|some|none). (string value)
nova.param('xenapi_torrent_images', type='all|some|none). (string', default='none')

# Base URL for torrent files. (string value)
nova.param('xenapi_torrent_base_url', type='string', default='<None>')

# Probability that peer will become a seeder. (1.0 = 100%)
# (floating point value)
nova.param('xenapi_torrent_seed_chance', type='1.0 = 100%) (floating point', default='1.0')

# Number of seconds after downloading an image via BitTorrent
# that it should be seeded for other peers. (integer value)
nova.param('xenapi_torrent_seed_duration', type='integer', default='3600')

# Cached torrent files not accessed within this number of
# seconds can be reaped (integer value)
nova.param('xenapi_torrent_max_last_accessed', type='integer', default='86400')

# Beginning of port range to listen on (integer value)
nova.param('xenapi_torrent_listen_port_start', type='integer', default='6881')

# End of port range to listen on (integer value)
nova.param('xenapi_torrent_listen_port_end', type='integer', default='6891')

# Number of seconds a download can remain at the same progress
# percentage w/o being considered a stall (integer value)
nova.param('xenapi_torrent_download_stall_cutoff', type='integer', default='600')

# Maximum number of seeder processes to run concurrently
# within a given dom0. (-1 = no limit) (integer value)
nova.param('xenapi_torrent_max_seeder_processes_per_host', type='-1 = no limit) (integer', default='1')

# number of seconds to wait for instance to go to running
# state (integer value)
nova.param('xenapi_running_timeout', type='integer', default='60')

# The XenAPI VIF driver using XenServer Network APIs. (string
# value)
nova.param('xenapi_vif_driver', type='string', default='nova.virt.xenapi.vif.XenAPIBridgeDriver')

# Object Store Driver used to handle image uploads. (string
# value)
nova.param('xenapi_image_upload_handler', type='string', default='nova.virt.xenapi.imageupload.glance.GlanceStore')

# location of vnc console proxy, in the form
# "http://127.0.0.1:6080/vnc_auto.html" (string value)
nova.param('novncproxy_base_url', type='string', default='http://127.0.0.1:6080/vnc_auto.html')

# location of nova xvp vnc console proxy, in the form
# "http://127.0.0.1:6081/console" (string value)
nova.param('xvpvncproxy_base_url', type='string', default='http://127.0.0.1:6081/console')

# IP address on which instance vncservers should listen
# (string value)
nova.param('vncserver_listen', type='string', default='127.0.0.1')

# the address to which proxy clients (like nova-xvpvncproxy)
# should connect (string value)
nova.param('vncserver_proxyclient_address', type='like nova-xvpvncproxy) should connect (string', default='127.0.0.1')

# enable vnc related features (boolean value)
nova.param('vnc_enabled', type='boolean', default='true')

# keymap for vnc (string value)
nova.param('vnc_keymap', type='string', default='en-us')

# Port that the XCP VNC proxy should bind to (integer value)
nova.param('xvpvncproxy_port', type='integer', default='6081')

# Address that the XCP VNC proxy should bind to (string value)
nova.param('xvpvncproxy_host', type='string', default='0.0.0.0')

# The full class name of the volume API class to use (string
# value)
nova.param('volume_api_class', type='string', default='nova.volume.cinder.API')

# Info to match when looking for cinder in the service
# catalog. Format is : separated values of the form:
# <service_type>:<service_name>:<endpoint_type> (string value)
nova.param('cinder_catalog_info', type='string', default='volume:cinder:publicURL')

# Override service catalog lookup with template for cinder
# endpoint e.g. http://localhost:8776/v1/%(project_id)s
# (string value)
nova.param('cinder_endpoint_template', type='project_id)s (string', default='<None>')

# region name of this node (string value)
nova.param('os_region_name', type='string', default='<None>')

# Number of cinderclient retries on failed http calls (integer
# value)
nova.param('cinder_http_retries', type='integer', default='3')

# Allow to perform insecure SSL requests to cinder (boolean
# value)
nova.param('cinder_api_insecure', type='boolean', default='false')

# Allow attach between instance and volume in different
# availability zones. (boolean value)
nova.param('cinder_cross_az_attach', type='boolean', default='true')

nova.section('HYPERV')

# The name of a Windows share name mapped to the
# "instances_path" dir and used by the resize feature to copy
# files to the target host. If left blank, an administrative
# share will be used, looking for the same "instances_path"
# used locally (string value)
nova.param('instances_path_share', type='string', default='')

nova.section('conductor')

# Perform nova-conductor operations locally (boolean value)
nova.param('use_local', type='boolean', default='false')

# the topic conductor nodes listen on (string value)
nova.param('topic', type='string', default='conductor')

# full class name for the Manager for conductor (string value)
nova.param('manager', type='string', default='nova.conductor.manager.ConductorManager')

nova.section('cells')

# Cells communication driver to use (string value)
nova.param('driver', type='string', default='nova.cells.rpc_driver.CellsRPCDriver')

# Number of seconds after an instance was updated or deleted
# to continue to update cells (integer value)
nova.param('instance_updated_at_threshold', type='integer', default='3600')

# Number of instances to update per periodic task run (integer
# value)
nova.param('instance_update_num_instances', type='integer', default='1')

# Maximum number of hops for cells routing. (integer value)
nova.param('max_hop_count', type='integer', default='10')

# Cells scheduler to use (string value)
nova.param('scheduler', type='string', default='nova.cells.scheduler.CellsScheduler')

# Enable cell functionality (boolean value)
nova.param('enable', type='boolean', default='false')

# the topic cells nodes listen on (string value)
nova.param('topic', type='string', default='cells')

# Manager for cells (string value)
nova.param('manager', type='string', default='nova.cells.manager.CellsManager')

# name of this cell (string value)
nova.param('name', type='string', default='nova')

# Key/Multi-value list with the capabilities of the cell (list
# value)
nova.param('capabilities', type='list', default='hypervisor')

# Seconds to wait for response from a call to a cell. (integer
# value)
nova.param('call_timeout', type='integer', default='60')

# Base queue name to use when communicating between cells.
# Various topics by message type will be appended to this.
# (string value)
nova.param('rpc_driver_queue_base', type='string', default='cells.intercell')

# How many retries when no cells are available. (integer
# value)
nova.param('scheduler_retries', type='integer', default='10')

# How often to retry in seconds when no cells are available.
# (integer value)
nova.param('scheduler_retry_delay', type='integer', default='2')

# Seconds between getting fresh cell info from db. (integer
# value)
nova.param('db_check_interval', type='integer', default='60')

nova.section('zookeeper')

# The ZooKeeper addresses for servicegroup service in the
# format of host1:port,host2:port,host3:port (string value)
nova.param('address', type='string', default='<None>')

# recv_timeout parameter for the zk session (integer value)
nova.param('recv_timeout', type='integer', default='4000')

# The prefix used in ZooKeeper to store ephemeral nodes
# (string value)
nova.param('sg_prefix', type='string', default='/servicegroups')

# Number of seconds to wait until retrying to join the session
# (integer value)
nova.param('sg_retry_interval', type='integer', default='5')

nova.section('baremetal')

# The backend to use for bare-metal database (string value)
nova.param('db_backend', type='string', default='sqlalchemy')

# The SQLAlchemy connection string used to connect to the
# bare-metal database (string value)
nova.param('sql_connection', type='string', default='sqlite:///$state_path/baremetal_$sqlite_db')

# Whether baremetal compute injects password or not (boolean
# value)
nova.param('inject_password', type='boolean', default='true')

# Template file for injected network (string value)
nova.param('injected_network_template', type='string', default='$pybasedir/nova/virt/baremetal/interfaces.template')

# Baremetal VIF driver. (string value)
nova.param('vif_driver', type='string', default='nova.virt.baremetal.vif_driver.BareMetalVIFDriver')

# Baremetal volume driver. (string value)
nova.param('volume_driver', type='string', default='nova.virt.baremetal.volume_driver.LibvirtVolumeDriver')

# a list of additional capabilities corresponding to
# instance_type_extra_specs for this compute host to
# advertise. Valid entries are name=value, pairs For example,
# "key1:val1, key2:val2" (list value)
nova.param('instance_type_extra_specs', type='list', default='')

# Baremetal driver back-end (pxe or tilera) (string value)
nova.param('driver', type='pxe or tilera) (string', default='nova.virt.baremetal.pxe.PXE')

# Baremetal power management method (string value)
nova.param('power_manager', type='string', default='nova.virt.baremetal.ipmi.IPMI')

# Baremetal compute node's tftp root path (string value)
nova.param('tftp_root', type='string', default='/tftpboot')

# path to baremetal terminal program (string value)
nova.param('terminal', type='string', default='shellinaboxd')

# path to baremetal terminal SSL cert(PEM) (string value)
nova.param('terminal_cert_dir', type='PEM) (string', default='<None>')

# path to directory stores pidfiles of baremetal_terminal
# (string value)
nova.param('terminal_pid_dir', type='string', default='$state_path/baremetal/console')

# maximal number of retries for IPMI operations (integer
# value)
nova.param('ipmi_power_retry', type='integer', default='5')

# Default kernel image ID used in deployment phase (string
# value)
nova.param('deploy_kernel', type='string', default='<None>')

# Default ramdisk image ID used in deployment phase (string
# value)
nova.param('deploy_ramdisk', type='string', default='<None>')

# Template file for injected network config (string value)
nova.param('net_config_template', type='string', default='$pybasedir/nova/virt/baremetal/net-dhcp.ubuntu.template')

# additional append parameters for baremetal PXE boot (string
# value)
nova.param('pxe_append_params', type='string', default='<None>')

# Template file for PXE configuration (string value)
nova.param('pxe_config_template', type='string', default='$pybasedir/nova/virt/baremetal/pxe_config.template')

# Timeout for PXE deployments. Default: 0 (unlimited) (integer
# value)
nova.param('pxe_deploy_timeout', type='unlimited) (integer', default='0')

# ip or name to virtual power host (string value)
nova.param('virtual_power_ssh_host', type='string', default='')

# base command to use for virtual power(vbox,virsh) (string
# value)
nova.param('virtual_power_type', type='vbox,virsh) (string', default='vbox')

# user to execute virtual power commands as (string value)
nova.param('virtual_power_host_user', type='string', default='')

# password for virtual power host_user (string value)
nova.param('virtual_power_host_pass', type='string', default='')

# Do not set this out of dev/test environments. If a node does
# not have a fixed PXE IP address, volumes are exported with
# globally opened ACL (boolean value)
nova.param('use_unsafe_iscsi', type='boolean', default='false')

# iSCSI IQN prefix used in baremetal volume connections.
# (string value)
nova.param('iscsi_iqn_prefix', type='string', default='iqn.2010-10.org.openstack.baremetal')

nova.section('rpc_notifier2')

# AMQP topic(s) used for openstack notifications (list value)
nova.param('topics', type='s) used for openstack notifications (list', default='notifications')

nova.section('trusted_computing')

# attestation server http (string value)
nova.param('attestation_server', type='string', default='<None>')

# attestation server Cert file for Identity verification
# (string value)
nova.param('attestation_server_ca_file', type='string', default='<None>')

# attestation server port (string value)
nova.param('attestation_port', type='string', default='8443')

# attestation web API URL (string value)
nova.param('attestation_api_url', type='string', default='/OpenAttestationWebServices/V1.0')

# attestation authorization blob - must change (string value)
nova.param('attestation_auth_blob', type='string', default='<None>')

# Attestation status cache valid period length (integer value)
nova.param('attestation_auth_timeout', type='integer', default='60')

nova.section('vmware')

# Name of Integration Bridge (string value)
nova.param('integration_bridge', type='string', default='br-int')

nova.section('spice')

# location of spice html5 console proxy, in the form
# "http://127.0.0.1:6082/spice_auto.html" (string value)
nova.param('html5proxy_base_url', type='string', default='http://127.0.0.1:6082/spice_auto.html')

# IP address on which instance spice server should listen
# (string value)
nova.param('server_listen', type='string', default='127.0.0.1')

# the address to which proxy clients (like nova-
# spicehtml5proxy) should connect (string value)
nova.param('server_proxyclient_address', type='like nova- spicehtml5proxy) should connect (string', default='127.0.0.1')

# enable spice related features (boolean value)
nova.param('enabled', type='boolean', default='false')

# enable spice guest agent support (boolean value)
nova.param('agent_enabled', type='boolean', default='true')

# keymap for spice (string value)
nova.param('keymap', type='string', default='en-us')

