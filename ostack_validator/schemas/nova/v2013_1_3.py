from ostack_validator.schema import ConfigSchemaRegistry

nova = ConfigSchemaRegistry.register_schema(project='nova')

nova.version('2013.1.3')

nova.section('DEFAULT')

nova.param('internal_service_availability_zone', type='string', default='internal', description="availability_zone to show internal services under")

nova.param('default_availability_zone', type='string', default='nova', description="default compute node availability_zone")

nova.param('ca_file', type='string', default='cacert.pem', description="Filename of root CA")

nova.param('key_file', type='string', default='private/cakey.pem', description="Filename of private key")

nova.param('crl_file', type='string', default='crl.pem', description="Filename of root Certificate Revocation List")

nova.param('keys_path', type='string', default='$state_path/keys', description="Where we keep our keys")

nova.param('ca_path', type='string', default='$state_path/CA', description="Where we keep our root CA")

nova.param('use_project_ca', type='boolean', default='false', description="Should we use a CA for each project?")

nova.param('user_cert_subject', type='string', default='/CUS/STCalifornia/OOpenStack/OUNovaDev/CN%.16s-%.16s-%s', description="Subject for certificate for users, %s for project, user, timestamp")

nova.param('project_cert_subject', type='string', default='/CUS/STCalifornia/OOpenStack/OUNovaDev/CNproject-ca-%.16s-%s', description="Subject for certificate for projects, %s for project, timestamp")

nova.param('fatal_exception_format_errors', type='boolean', default='false', description="make exception message format errors fatal")

nova.param('my_ip', type='string', default='10.0.0.1', description="ip address of this host")

nova.param('host', type='string', default='nova', description="Name of this node.  This can be an opaque identifier.  It is not necessarily a hostname, FQDN, or IP address. However, the node name must be valid within an AMQP key, and if using ZeroMQ, a valid hostname, FQDN, or IP address")

nova.param('use_ipv6', type='boolean', default='false', description="use ipv6")

nova.param('notify_on_state_change', type='string', default='<None>', description="If set, send compute.instance.update notifications on instance state changes.  Valid values are None for no notifications, 'vm_state' for notifications on VM state changes, or 'vm_and_task_state' for notifications on VM and task state changes.")

nova.param('notify_api_faults', type='boolean', default='false', description="If set, send api.fault notifications on caught exceptions in the API service.")

nova.param('pybasedir', type='string', default='/usr/lib/python/site-packages', description="Directory where the nova python module is installed")

nova.param('bindir', type='string', default='/usr/local/bin', description="Directory where nova binaries are installed")

nova.param('state_path', type='string', default='$pybasedir', description="Top-level directory for maintaining nova's state")

nova.param('policy_file', type='string', default='policy.json', description="JSON file representing policy")

nova.param('policy_default_rule', type='string', default='default', description="Rule checked when requested rule is not found")

nova.param('quota_instances', type='integer', default='10', description="number of instances allowed per project")

nova.param('quota_cores', type='integer', default='20', description="number of instance cores allowed per project")

nova.param('quota_ram', type='integer', default='51200', description="megabytes of instance ram allowed per project")

nova.param('quota_floating_ips', type='integer', default='10', description="number of floating ips allowed per project")

nova.param('quota_fixed_ips', type='integer', default='-1', description="number of fixed ips allowed per project")

nova.param('quota_metadata_items', type='integer', default='128', description="number of metadata items allowed per instance")

nova.param('quota_injected_files', type='integer', default='5', description="number of injected files allowed")

nova.param('quota_injected_file_content_bytes', type='integer', default='10240', description="number of bytes allowed per injected file")

nova.param('quota_injected_file_path_bytes', type='integer', default='255', description="number of bytes allowed per injected file path")

nova.param('quota_security_groups', type='integer', default='10', description="number of security groups per project")

nova.param('quota_security_group_rules', type='integer', default='20', description="number of security rules per security group")

nova.param('quota_key_pairs', type='integer', default='100', description="number of key pairs per user")

nova.param('reservation_expire', type='integer', default='86400', description="number of seconds until a reservation expires")

nova.param('until_refresh', type='integer', default='0', description="count of reservations until usage is refreshed")

nova.param('max_age', type='integer', default='0', description="number of seconds between subsequent usage refreshes")

nova.param('quota_driver', type='string', default='nova.quota.DbQuotaDriver', description="default driver to use for quota checks")

nova.param('report_interval', type='integer', default='10', description="seconds between nodes reporting state to datastore")

nova.param('periodic_enable', type='boolean', default='true', description="enable periodic tasks")

nova.param('periodic_fuzzy_delay', type='integer', default='60', description="range of seconds to randomly delay when starting the periodic task scheduler to reduce stampeding.")

nova.param('enabled_apis', type='list', default='ec2,osapi_compute,metadata', description="a list of APIs to enable by default")

nova.param('enabled_ssl_apis', type='list', default='', description="a list of APIs with enabled SSL")

nova.param('ec2_listen', type='string', default='0.0.0.0', description="IP address for EC2 API to listen")

nova.param('ec2_listen_port', type='integer', default='8773', description="port for ec2 api to listen")

nova.param('ec2_workers', type='integer', default='<None>', description="Number of workers for EC2 API service")

nova.param('osapi_compute_listen', type='string', default='0.0.0.0', description="IP address for OpenStack API to listen")

nova.param('osapi_compute_listen_port', type='integer', default='8774', description="list port for osapi compute")

nova.param('osapi_compute_workers', type='integer', default='<None>', description="Number of workers for OpenStack API service")

nova.param('metadata_manager', type='string', default='nova.api.manager.MetadataManager', description="OpenStack metadata service manager")

nova.param('metadata_listen', type='string', default='0.0.0.0', description="IP address for metadata api to listen")

nova.param('metadata_listen_port', type='integer', default='8775', description="port for metadata api to listen")

nova.param('metadata_workers', type='integer', default='<None>', description="Number of workers for metadata service")

nova.param('compute_manager', type='string', default='nova.compute.manager.ComputeManager', description="full class name for the Manager for compute")

nova.param('console_manager', type='string', default='nova.console.manager.ConsoleProxyManager', description="full class name for the Manager for console proxy")

nova.param('cert_manager', type='string', default='nova.cert.manager.CertManager', description="full class name for the Manager for cert")

nova.param('network_manager', type='string', default='nova.network.manager.VlanManager', description="full class name for the Manager for network")

nova.param('scheduler_manager', type='string', default='nova.scheduler.manager.SchedulerManager', description="full class name for the Manager for scheduler")

nova.param('service_down_time', type='integer', default='60', description="maximum time since last check-in for up service")

nova.param('sqlite_clean_db', type='string', default='clean.sqlite', description="File name of clean sqlite db")

nova.param('monkey_patch', type='boolean', default='false', description="Whether to log monkey patching")

nova.param('monkey_patch_modules', type='list', default='nova.api.ec2.cloud:nova.notifications.notify_decorator,nova.compute.api:nova.notifications.notify_decorator', description="List of modules/decorators to monkey patch")

nova.param('password_length', type='integer', default='12', description="Length of generated instance admin passwords")

nova.param('instance_usage_audit_period', type='string', default='month', description="time period to generate instance usages for.  Time period must be hour, day, month or year")

nova.param('rootwrap_config', type='string', default='/etc/nova/rootwrap.conf', description="Path to the rootwrap configuration file to use for running commands as root")

nova.param('tempdir', type='string', default='<None>', description="Explicitly specify the temporary working directory")

nova.param('api_paste_config', type='string', default='api-paste.ini', description="File name for the paste.deploy config for nova-api")

nova.param('wsgi_log_format', type='string', default='%(client_ip)s "%(request_line)s" status: %(status_code)s len: %(body_length)s time: %(wall_seconds).7f', description="A python format string that is used as the template to generate log lines. The following values can be formatted into it: client_ip, date_time, request_line, status_code, body_length, wall_seconds.")

nova.param('ssl_ca_file', type='string', default='<None>', description="CA certificate file to use to verify connecting clients")

nova.param('ssl_cert_file', type='string', default='<None>', description="SSL certificate of API server")

nova.param('ssl_key_file', type='string', default='<None>', description="SSL private key of API server")

nova.param('tcp_keepidle', type='integer', default='600', description="Sets the value of TCP_KEEPIDLE in seconds for each server socket. Not supported on OS X.")

nova.param('api_rate_limit', type='boolean', default='false', description="whether to use per-user rate limiting for the api.")

nova.param('auth_strategy', type='string', default='noauth', description="The strategy to use for auth: noauth or keystone.")

nova.param('use_forwarded_for', type='boolean', default='false', description="Treat X-Forwarded-For as the canonical remote address. Only enable this if you have a sanitizing proxy.")

nova.param('lockout_attempts', type='integer', default='5', description="Number of failed auths before lockout.")

nova.param('lockout_minutes', type='integer', default='15', description="Number of minutes to lockout if triggered.")

nova.param('lockout_window', type='integer', default='15', description="Number of minutes for lockout window.")

nova.param('keystone_ec2_url', type='string', default='http://localhost:5000/v2.0/ec2tokens', description="URL to get token from ec2 request.")

nova.param('ec2_private_dns_show_ip', type='boolean', default='false', description="Return the IP address as private dns hostname in describe instances")

nova.param('ec2_strict_validation', type='boolean', default='true', description="Validate security group names according to EC2 specification")

nova.param('ec2_timestamp_expiry', type='integer', default='300', description="Time in seconds before ec2 timestamp expires")

nova.param('ec2_host', type='string', default='$my_ip', description="the ip of the ec2 api server")

nova.param('ec2_dmz_host', type='string', default='$my_ip', description="the internal ip of the ec2 api server")

nova.param('ec2_port', type='integer', default='8773', description="the port of the ec2 api server")

nova.param('ec2_scheme', type='string', default='http', description="the protocol to use when connecting to the ec2 api server")

nova.param('ec2_path', type='string', default='/services/Cloud', description="the path prefix used to call the ec2 api server")

nova.param('region_list', type='list', default='', description="list of region=fqdn pairs separated by commas")

nova.param('config_drive_skip_versions', type='string', default='1.0 2007-01-19 2007-03-01 2007-08-29 2007-10-10 2007-12-15 2008-02-01 2008-09-01', description="List of metadata versions to skip placing into the config drive")

nova.param('vendordata_driver', type='string', default='nova.api.metadata.vendordata_json.JsonFileVendorData', description="Driver to use for vendor data")

nova.param('service_neutron_metadata_proxy', type='boolean', default='false', description="Set flag to indicate Neutron will proxy metadata requests and resolve instance ids.")

nova.param('neutron_metadata_proxy_shared_secret', type='string', default='', description="Shared secret to validate proxies Neutron metadata requests")

nova.param('vendordata_jsonfile_path', type='string', default='<None>', description="File to load json formated vendor data from")

nova.param('osapi_max_limit', type='integer', default='1000', description="the maximum number of items returned in a single response from a collection resource")

nova.param('osapi_compute_link_prefix', type='string', default='<None>', description="Base URL that will be presented to users in links to the OpenStack Compute API")

nova.param('osapi_glance_link_prefix', type='string', default='<None>', description="Base URL that will be presented to users in links to glance resources")

nova.param('allow_instance_snapshots', type='boolean', default='true', description="Permit instance snapshot operations.")

nova.param('osapi_compute_ext_list', type='list', default='', description="Specify list of extensions to load when using osapi_compute_extension option with nova.api.openstack.compute.contrib.select_extensions")

nova.param('fping_path', type='string', default='/usr/sbin/fping', description="Full path to fping.")

nova.param('enable_network_quota', type='boolean', default='false', description="Enables or disables quota checking for tenant networks")

nova.param('use_neutron_default_nets', type='string', default='False', description="Control for checking for default networks")

nova.param('neutron_default_tenant_id', type='string', default='default', description="Default tenant id when creating neutron networks")

nova.param('osapi_compute_extension', type='multi', default='nova.api.openstack.compute.contrib.standard_extensions', description="osapi compute extension to load")

nova.param('osapi_hide_server_address_states', type='list', default='building', description="List of instance states that should hide network info")

nova.param('enable_instance_password', type='boolean', default='true', description="Allows use of instance password during server creation")

nova.param('osapi_max_request_body_size', type='integer', default='114688', description="the maximum body size per each osapi request(bytes)")

nova.param('compute_api_class', type='string', default='nova.compute.api.API', description="The full class name of the compute API class to use")

nova.param('cert_topic', type='string', default='cert', description="the topic cert nodes listen on")

nova.param('vpn_image_id', type='string', default='0', description="image id used when starting up a cloudpipe vpn server")

nova.param('vpn_flavor', type='string', default='m1.tiny', description="Flavor for vpn instances")

nova.param('boot_script_template', type='string', default='$pybasedir/nova/cloudpipe/bootscript.template', description="Template for cloudpipe instance boot script")

nova.param('dmz_net', type='string', default='10.0.0.0', description="Network to push into openvpn config")

nova.param('dmz_mask', type='string', default='255.255.255.0', description="Netmask to push into openvpn config")

nova.param('vpn_key_suffix', type='string', default='-vpn', description="Suffix to add to project name for vpn key and secgroups")

nova.param('record', type='boolean', default='false', description="Record sessions to FILE.[session_number]")

nova.param('daemon', type='boolean', default='false', description="Become a daemon")

nova.param('ssl_only', type='boolean', default='false', description="Disallow non-encrypted connections")

nova.param('source_is_ipv6', type='boolean', default='false', description="Source is ipv6")

nova.param('cert', type='string', default='self.pem', description="SSL certificate file")

nova.param('key', type='string', default='<None>', description="SSL key file")

nova.param('web', type='string', default='/usr/share/spice-html5', description="Run webserver on same port. Serve files from DIR.")

nova.param('novncproxy_host', type='string', default='0.0.0.0', description="Host on which to listen for incoming requests")

nova.param('novncproxy_port', type='integer', default='6080', description="Port on which to listen for incoming requests")

nova.param('spicehtml5proxy_host', type='string', default='0.0.0.0', description="Host on which to listen for incoming requests")

nova.param('spicehtml5proxy_port', type='integer', default='6082', description="Port on which to listen for incoming requests")

nova.param('allow_resize_to_same_host', type='boolean', default='false', description="Allow destination machine to match source for resize. Useful when testing in single-host environments.")

nova.param('allow_migrate_to_same_host', type='boolean', default='false', description="Allow migrate machine to the same host. Useful when testing in single-host environments.")

nova.param('default_schedule_zone', type='string', default='<None>', description="availability zone to use when user doesn't specify one")

nova.param('non_inheritable_image_properties', type='list', default='cache_in_nova,bittorrent', description="These are image properties which a snapshot should not inherit from an instance")

nova.param('null_kernel', type='string', default='nokernel', description="kernel image that indicates not to use a kernel, but to use a raw disk image instead")

nova.param('multi_instance_display_name_template', type='string', default='%(name)s-%(uuid)s', description="When creating multiple instances with a single request using the os-multiple-create API extension, this template will be used to build the display name for each instance. The benefit is that the instances end up with different hostnames. To restore legacy behavior of every instance having the same name, set this option to '%(name)s'.  Valid keys for the template are: name, uuid, count.")

nova.param('max_local_block_devices', type='integer', default='3', description="Maximum number of devices that will result in a local image being created on the hypervisor node. Setting this to 0 means nova will allow only boot from volume. A negative number means unlimited.")

nova.param('default_flavor', type='string', default='m1.small', description="default flavor to use for the EC2 API only. The Nova API does not support a default flavor.")

nova.param('console_host', type='string', default='nova', description="Console proxy host to use to connect to instances on this host.")

nova.param('default_access_ip_network_name', type='string', default='<None>', description="Name of network to use to set access ips for instances")

nova.param('defer_iptables_apply', type='boolean', default='false', description="Whether to batch up the application of IPTables rules during a host restart and apply all at the end of the init phase")

nova.param('instances_path', type='string', default='$state_path/instances', description="where instances are stored on disk")

nova.param('instance_usage_audit', type='boolean', default='false', description="Generate periodic compute.instance.exists notifications")

nova.param('live_migration_retry_count', type='integer', default='30', description="Number of 1 second retries needed in live_migration")

nova.param('resume_guests_state_on_host_boot', type='boolean', default='false', description="Whether to start guests that were running before the host rebooted")

nova.param('network_allocate_retries', type='integer', default='0', description="Number of times to retry network allocation on failures")

nova.param('maximum_instance_delete_attempts', type='integer', default='5', description="The number of times to attempt to reap an instance's files.")

nova.param('bandwidth_poll_interval', type='integer', default='600', description="interval to pull bandwidth usage info")

nova.param('sync_power_state_interval', type='integer', default='600', description="interval to sync power states between the database and the hypervisor")

nova.param('heal_instance_info_cache_interval', type='integer', default='60', description="Number of seconds between instance info_cache self healing updates")

nova.param('host_state_interval', type='integer', default='120', description="Interval in seconds for querying the host status")

nova.param('image_cache_manager_interval', type='integer', default='2400', description="Number of seconds to wait between runs of the image cache manager")

nova.param('reclaim_instance_interval', type='integer', default='0', description="Interval in seconds for reclaiming deleted instances")

nova.param('volume_usage_poll_interval', type='integer', default='0', description="Interval in seconds for gathering volume usages")

nova.param('shelved_poll_interval', type='integer', default='3600', description="Interval in seconds for polling shelved instances to offload")

nova.param('shelved_offload_time', type='integer', default='0', description="Time in seconds before a shelved instance is eligible for removing from a host.  -1 never offload, 0 offload when shelved")

nova.param('instance_delete_interval', type='integer', default='300', description="Interval in seconds for retrying failed instance file deletes")

nova.param('running_deleted_instance_action', type='string', default='log', description="Action to take if a running deleted instance is detected.Valid options are 'noop', 'log' and 'reap'. Set to 'noop' to disable.")

nova.param('running_deleted_instance_poll_interval', type='integer', default='1800', description="Number of seconds to wait between runs of the cleanup task.")

nova.param('running_deleted_instance_timeout', type='integer', default='0', description="Number of seconds after being deleted when a running instance should be considered eligible for cleanup.")

nova.param('reboot_timeout', type='integer', default='0', description="Automatically hard reboot an instance if it has been stuck in a rebooting state longer than N seconds. Set to 0 to disable.")

nova.param('instance_build_timeout', type='integer', default='0', description="Amount of time in seconds an instance can be in BUILD before going into ERROR status.Set to 0 to disable.")

nova.param('rescue_timeout', type='integer', default='0', description="Automatically unrescue an instance after N seconds. Set to 0 to disable.")

nova.param('resize_confirm_window', type='integer', default='0', description="Automatically confirm resizes after N seconds. Set to 0 to disable.")

nova.param('reserved_host_disk_mb', type='integer', default='0', description="Amount of disk in MB to reserve for the host")

nova.param('reserved_host_memory_mb', type='integer', default='512', description="Amount of memory in MB to reserve for the host")

nova.param('compute_stats_class', type='string', default='nova.compute.stats.Stats', description="Class that will manage stats for the local compute host")

nova.param('compute_topic', type='string', default='compute', description="the topic compute nodes listen on")

nova.param('migrate_max_retries', type='integer', default='-1', description="Number of times to retry live-migration before failing. If == -1, try until out of hosts. If == 0, only try once, no retries.")

nova.param('console_driver', type='string', default='nova.console.xvp.XVPConsoleProxy', description="Driver to use for the console proxy")

nova.param('stub_compute', type='boolean', default='false', description="Stub calls to compute worker for tests")

nova.param('console_public_hostname', type='string', default='nova', description="Publicly visible name for this console host")

nova.param('console_topic', type='string', default='console', description="the topic console proxy nodes listen on")

nova.param('console_vmrc_port', type='integer', default='443', description="port for VMware VMRC connections")

nova.param('console_vmrc_error_retries', type='integer', default='10', description="number of retries for retrieving VMRC information")

nova.param('console_xvp_conf_template', type='string', default='$pybasedir/nova/console/xvp.conf.template', description="XVP conf template")

nova.param('console_xvp_conf', type='string', default='/etc/xvp.conf', description="generated XVP conf file")

nova.param('console_xvp_pid', type='string', default='/var/run/xvp.pid', description="XVP master process pid file")

nova.param('console_xvp_log', type='string', default='/var/log/xvp.log', description="XVP log file")

nova.param('console_xvp_multiplex_port', type='integer', default='5900', description="port for XVP to multiplex VNC connections on")

nova.param('consoleauth_topic', type='string', default='consoleauth', description="the topic console auth proxy nodes listen on")

nova.param('console_token_ttl', type='integer', default='600', description="How many seconds before deleting tokens")

nova.param('consoleauth_manager', type='string', default='nova.consoleauth.manager.ConsoleAuthManager', description="Manager for console auth")

nova.param('enable_new_services', type='boolean', default='true', description="Services to be added to the available pool on create")

nova.param('instance_name_template', type='string', default='instance-%08x', description="Template string to be used to generate instance names")

nova.param('snapshot_name_template', type='string', default='snapshot-%s', description="Template string to be used to generate snapshot names")

nova.param('db_driver', type='string', default='nova.db', description="driver to use for database access")

nova.param('osapi_compute_unique_server_name_scope', type='string', default='', description="When set, compute API will consider duplicate hostnames invalid within the specified scope, regardless of case. Should be empty, 'project' or 'global'.")

nova.param('glance_host', type='string', default='$my_ip', description="default glance hostname or ip")

nova.param('glance_port', type='integer', default='9292', description="default glance port")

nova.param('glance_protocol', type='string', default='http', description="Default protocol to use when connecting to glance. Set to https for SSL.")

nova.param('glance_api_servers', type='list', default='$glance_host:$glance_port', description="A list of the glance api servers available to nova. Prefix with https:// for ssl-based glance api servers.")

nova.param('glance_api_insecure', type='boolean', default='false', description="Allow to perform insecure SSL")

nova.param('glance_num_retries', type='integer', default='0', description="Number retries when downloading an image from glance")

nova.param('allowed_direct_url_schemes', type='list', default='', description="A list of url scheme that can be downloaded directly via the direct_url.  Currently supported schemes: [file].")

nova.param('image_decryption_dir', type='string', default='/tmp', description="parent dir for tempdir used for image decryption")

nova.param('s3_host', type='string', default='$my_ip', description="hostname or ip for OpenStack to use when accessing the s3 api")

nova.param('s3_port', type='integer', default='3333', description="port used when accessing the s3 api")

nova.param('s3_access_key', type='string', default='notchecked', description="access key to use for s3 server for images")

nova.param('s3_secret_key', type='string', default='notchecked', description="secret key to use for s3 server for images")

nova.param('s3_use_ssl', type='boolean', default='false', description="whether to use ssl when talking to s3")

nova.param('s3_affix_tenant', type='boolean', default='false', description="whether to affix the tenant id to the access key when downloading from s3")

nova.param('ipv6_backend', type='string', default='rfc2462', description="Backend to use for IPv6 generation")

nova.param('network_api_class', type='string', default='nova.network.api.API', description="The full class name of the network API class to use")

nova.param('network_driver', type='string', default='nova.network.linux_net', description="Driver to use for network creation")

nova.param('default_floating_pool', type='string', default='nova', description="Default pool for floating ips")

nova.param('auto_assign_floating_ip', type='boolean', default='false', description="Autoassigning floating ip to VM")

nova.param('floating_ip_dns_manager', type='string', default='nova.network.noop_dns_driver.NoopDNSDriver', description="full class name for the DNS Manager for floating IPs")

nova.param('instance_dns_manager', type='string', default='nova.network.noop_dns_driver.NoopDNSDriver', description="full class name for the DNS Manager for instance IPs")

nova.param('instance_dns_domain', type='string', default='', description="full class name for the DNS Zone for instance IPs")

nova.param('ldap_dns_url', type='string', default='ldap://ldap.example.com:389', description="URL for ldap server which will store dns entries")

nova.param('ldap_dns_user', type='string', default='uidadmin,oupeople,dcexample,dcorg', description="user for ldap DNS")

nova.param('ldap_dns_password', type='string', default='password', description="password for ldap DNS")

nova.param('ldap_dns_soa_hostmaster', type='string', default='hostmaster@example.org', description="Hostmaster for ldap dns driver Statement of Authority")

nova.param('ldap_dns_servers', type='multi', default='dns.example.org', description="DNS Servers for ldap dns driver")

nova.param('ldap_dns_base_dn', type='string', default='ouhosts,dcexample,dcorg', description="Base DN for DNS entries in ldap")

nova.param('ldap_dns_soa_refresh', type='string', default='1800', description="Refresh interval")

nova.param('ldap_dns_soa_retry', type='string', default='3600', description="Retry interval")

nova.param('ldap_dns_soa_expiry', type='string', default='86400', description="Expiry interval")

nova.param('ldap_dns_soa_minimum', type='string', default='7200', description="Minimum interval")

nova.param('dhcpbridge_flagfile', type='multi', default='/etc/nova/nova-dhcpbridge.conf', description="location of flagfiles for dhcpbridge")

nova.param('networks_path', type='string', default='$state_path/networks', description="Location to keep network config files")

nova.param('public_interface', type='string', default='eth0', description="Interface for public IP addresses")

nova.param('network_device_mtu', type='string', default='<None>', description="MTU setting for vlan")

nova.param('dhcpbridge', type='string', default='$bindir/nova-dhcpbridge', description="location of nova-dhcpbridge")

nova.param('routing_source_ip', type='string', default='$my_ip', description="Public IP of network host")

nova.param('dhcp_lease_time', type='integer', default='120', description="Lifetime of a DHCP lease in seconds")

nova.param('dns_server', type='multi', default='', description="if set, uses specific dns server for dnsmasq. Canbe specified multiple times.")

nova.param('use_network_dns_servers', type='boolean', default='false', description="if set, uses the dns1 and dns2 from the network ref.as dns servers.")

nova.param('dmz_cidr', type='list', default='', description="A list of dmz range that should be accepted")

nova.param('force_snat_range', type='multi', default='', description="Traffic to this range will always be snatted to the fallback ip, even if it would normally be bridged out of the node. Can be specified multiple times.")

nova.param('dnsmasq_config_file', type='string', default='', description="Override the default dnsmasq settings with this file")

nova.param('linuxnet_interface_driver', type='string', default='nova.network.linux_net.LinuxBridgeInterfaceDriver', description="Driver used to create ethernet devices.")

nova.param('linuxnet_ovs_integration_bridge', type='string', default='br-int', description="Name of Open vSwitch bridge used with linuxnet")

nova.param('send_arp_for_ha', type='boolean', default='false', description="send gratuitous ARPs for HA setup")

nova.param('send_arp_for_ha_count', type='integer', default='3', description="send this many gratuitous ARPs for HA setup")

nova.param('use_single_default_gateway', type='boolean', default='false', description="Use single default gateway. Only first nic of vm will get default gateway from dhcp server")

nova.param('forward_bridge_interface', type='multi', default='all', description="An interface that bridges can forward to. If this is set to all then all traffic will be forwarded. Can be specified multiple times.")

nova.param('metadata_host', type='string', default='$my_ip', description="the ip for the metadata api server")

nova.param('metadata_port', type='integer', default='8775', description="the port for the metadata api port")

nova.param('iptables_top_regex', type='string', default='', description="Regular expression to match iptables rule that should always be on the top.")

nova.param('iptables_bottom_regex', type='string', default='', description="Regular expression to match iptables rule that should always be on the bottom.")

nova.param('iptables_drop_action', type='string', default='DROP', description="The table that iptables to jump to when a packet is to be dropped.")

nova.param('flat_network_bridge', type='string', default='<None>', description="Bridge for simple network instances")

nova.param('flat_network_dns', type='string', default='8.8.4.4', description="Dns for simple network")

nova.param('flat_injected', type='boolean', default='false', description="Whether to attempt to inject network setup into guest")

nova.param('flat_interface', type='string', default='<None>', description="FlatDhcp will bridge into this interface if set")

nova.param('vlan_start', type='integer', default='100', description="First VLAN for private networks")

nova.param('vlan_interface', type='string', default='<None>', description="vlans will bridge into this interface if set")

nova.param('num_networks', type='integer', default='1', description="Number of networks to support")

nova.param('vpn_ip', type='string', default='$my_ip', description="Public IP for the cloudpipe VPN servers")

nova.param('vpn_start', type='integer', default='1000', description="First Vpn port for private networks")

nova.param('network_size', type='integer', default='256', description="Number of addresses in each private subnet")

nova.param('fixed_range_v6', type='string', default='fd00::/48', description="Fixed IPv6 address block")

nova.param('gateway', type='string', default='<None>', description="Default IPv4 gateway")

nova.param('gateway_v6', type='string', default='<None>', description="Default IPv6 gateway")

nova.param('cnt_vpn_clients', type='integer', default='0', description="Number of addresses reserved for vpn clients")

nova.param('fixed_ip_disassociate_timeout', type='integer', default='600', description="Seconds after which a deallocated ip is disassociated")

nova.param('create_unique_mac_address_attempts', type='integer', default='5', description="Number of attempts to create unique mac address")

nova.param('fake_network', type='boolean', default='false', description="If passed, use fake network devices and addresses")

nova.param('fake_call', type='boolean', default='false', description="If True, skip using the queue and make local calls")

nova.param('teardown_unused_network_gateway', type='boolean', default='false', description="If True, unused gateway devices")

nova.param('force_dhcp_release', type='boolean', default='true', description="If True, send a dhcp release on instance termination")

nova.param('share_dhcp_address', type='boolean', default='false', description="If True in multi_host mode, all compute hosts share the same dhcp address. The same IP address used for DHCP will be added on each nova-network node which is only visible to the vms on the same host.")

nova.param('update_dns_entries', type='boolean', default='false', description="If True, when a DNS entry must be updated, it sends a fanout cast to all network hosts to update their DNS entries in multi host mode")

nova.param('dns_update_periodic_interval', type='integer', default='-1', description="Number of seconds to wait between runs of updates to DNS entries.")

nova.param('dhcp_domain', type='string', default='novalocal', description="domain to use for building the hostnames")

nova.param('l3_lib', type='string', default='nova.network.l3.LinuxNetL3', description="Indicates underlying L3 management library")

nova.param('neutron_url', type='string', default='http://127.0.0.1:9696', description="URL for connecting to neutron")

nova.param('neutron_url_timeout', type='integer', default='30', description="timeout value for connecting to neutron in seconds")

nova.param('neutron_admin_username', type='string', default='<None>', description="username for connecting to neutron in admin context")

nova.param('neutron_admin_password', type='string', default='<None>', description="password for connecting to neutron in admin context")

nova.param('neutron_admin_tenant_name', type='string', default='<None>', description="tenant name for connecting to neutron in admin context")

nova.param('neutron_region_name', type='string', default='<None>', description="region name for connecting to neutron in admin context")

nova.param('neutron_admin_auth_url', type='string', default='http://localhost:5000/v2.0', description="auth url for connecting to neutron in admin context")

nova.param('neutron_api_insecure', type='boolean', default='false', description="if set, ignore any SSL validation issues")

nova.param('neutron_auth_strategy', type='string', default='keystone', description="auth strategy for connecting to neutron in admin context")

nova.param('neutron_ovs_bridge', type='string', default='br-int', description="Name of Integration Bridge used by Open vSwitch")

nova.param('neutron_extension_sync_interval', type='integer', default='600', description="Number of seconds before querying neutron for extensions")

nova.param('neutron_ca_certificates_file', type='string', default='<None>', description="Location of ca certicates file to use for neutronclient requests.")

nova.param('dhcp_options_enabled', type='boolean', default='false', description="Use per-port DHCP options with Neutron")

nova.param('network_topic', type='string', default='network', description="the topic network nodes listen on")

nova.param('multi_host', type='boolean', default='false', description="Default value for multi_host in networks. Also, if set, some rpc network calls will be sent directly to host.")

nova.param('security_group_api', type='string', default='nova', description="The full class name of the security API class")

nova.param('buckets_path', type='string', default='$state_path/buckets', description="path to s3 buckets")

nova.param('s3_listen', type='string', default='0.0.0.0', description="IP address for S3 API to listen")

nova.param('s3_listen_port', type='integer', default='3333', description="port for s3 api to listen")

nova.param('sqlite_db', type='string', default='nova.sqlite', description="the filename to use with sqlite")

nova.param('sqlite_synchronous', type='boolean', default='true', description="If true, use synchronous mode for sqlite")

nova.param('backdoor_port', type='string', default='<None>', description="Enable eventlet backdoor. Acceptable values are 0, <port> and <start>:<end>, where 0 results in listening on a random tcp port number, <port> results in listening on the specified port number and not enabling backdoorif it is in use and <start>:<end> results in listening on the smallest unused port number within the specified range of port numbers. The chosen port is displayed in the service's log file.")

nova.param('disable_process_locking', type='boolean', default='false', description="Whether to disable inter-process locks")

nova.param('lock_path', type='string', default='<None>', description="Directory to use for lock files.")

nova.param('debug', type='boolean', default='false', description="Print debugging output")

nova.param('verbose', type='boolean', default='false', description="Print more verbose output")

nova.param('use_stderr', type='boolean', default='true', description="Log output to standard error")

nova.param('logging_context_format_string', type='string', default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user)s %(tenant)s] %(instance)s%(message)s', description="format string to use for log messages with context")

nova.param('logging_default_format_string', type='string', default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s', description="format string to use for log messages without context")

nova.param('logging_debug_format_suffix', type='string', default='%(funcName)s %(pathname)s:%(lineno)d', description="data to append to log format when level is DEBUG")

nova.param('logging_exception_prefix', type='string', default='%(asctime)s.%(msecs)03d %(process)d TRACE %(name)s %(instance)s', description="prefix each line of exception output with this format")

nova.param('default_log_levels', type='list', default='amqplibWARN,sqlalchemyWARN,botoWARN,sudsINFO,keystoneINFO,eventlet.wsgi.serverWARN', description="list of logger=LEVEL pairs")

nova.param('publish_errors', type='boolean', default='false', description="publish error events")

nova.param('fatal_deprecations', type='boolean', default='false', description="make deprecations fatal")

nova.param('instance_format', type='string', default='"[instance: %(uuid)s] "', description="If an instance is passed with the log message, format it like this")

nova.param('instance_uuid_format', type='string', default='"[instance: %(uuid)s] "', description="If an instance UUID is passed with the log message, format it like this")

nova.param('log_config', type='string', default='<None>', description="If this option is specified, the logging configuration file specified is used and overrides any other logging options specified. Please see the Python logging module documentation for details on logging configuration files.")

nova.param('log_format', type='string', default='<None>', description="DEPRECATED. A logging.Formatter log message format string which may use any of the available logging.LogRecord attributes. This option is deprecated.  Please use logging_context_format_string and logging_default_format_string instead.")

nova.param('log_date_format', type='string', default='%Y-%m-%d %H:%M:%S', description="Format string for %%(asctime)s in log records. Default: %(default)s")

nova.param('log_file', type='string', default='<None>', description="(Optional) Name of log file to output to. If no default is set, logging will go to stdout.")

nova.param('log_dir', type='string', default='<None>', description="(Optional) The base directory used for relative --log-file paths")

nova.param('use_syslog', type='boolean', default='false', description="Use syslog for logging.")

nova.param('syslog_log_facility', type='string', default='LOG_USER', description="syslog facility to receive log lines")

nova.param('memcached_servers', type='list', default='<None>', description="Memcached servers or None for in process cache.")

nova.param('notification_driver', type='multi', default='', description="Driver or drivers to handle sending notifications")

nova.param('default_notification_level', type='string', default='INFO', description="Default notification level for outgoing notifications")

nova.param('default_publisher_id', type='string', default='<None>', description="Default publisher_id for outgoing notifications")

nova.param('notification_topics', type='list', default='notifications', description="AMQP topic used for OpenStack notifications")

nova.param('run_external_periodic_tasks', type='boolean', default='true', description="Some periodic tasks can be run in a separate process. Should we run them here?")

nova.param('rpc_backend', type='string', default='nova.openstack.common.rpc.impl_kombu', description="The messaging module to use, defaults to kombu.")

nova.param('rpc_thread_pool_size', type='integer', default='64', description="Size of RPC thread pool")

nova.param('rpc_conn_pool_size', type='integer', default='30', description="Size of RPC connection pool")

nova.param('rpc_response_timeout', type='integer', default='60', description="Seconds to wait for a response from call or multicall")

nova.param('rpc_cast_timeout', type='integer', default='30', description="Seconds to wait before a cast expires")

nova.param('allowed_rpc_exception_modules', type='list', default='nova.exception,cinder.exception,exceptions', description="Modules of exceptions that are permitted to be recreatedupon receiving exception data from an rpc call.")

nova.param('fake_rabbit', type='boolean', default='false', description="If passed, use a fake RabbitMQ provider")

nova.param('control_exchange', type='string', default='openstack', description="AMQP exchange to connect to if using RabbitMQ or Qpid")

nova.param('amqp_durable_queues', type='boolean', default='false', description="Use durable queues in amqp.")

nova.param('amqp_auto_delete', type='boolean', default='false', description="Auto-delete queues in amqp.")

nova.param('kombu_ssl_version', type='string', default='', description="SSL version to use")

nova.param('kombu_ssl_keyfile', type='string', default='', description="SSL key file")

nova.param('kombu_ssl_certfile', type='string', default='', description="SSL cert file")

nova.param('kombu_ssl_ca_certs', type='string', default='', description="SSL certification authority file")

nova.param('rabbit_host', type='string', default='localhost', description="The RabbitMQ broker address where a single node is used")

nova.param('rabbit_port', type='integer', default='5672', description="The RabbitMQ broker port where a single node is used")

nova.param('rabbit_hosts', type='list', default='$rabbit_host:$rabbit_port', description="RabbitMQ HA cluster host:port pairs")

nova.param('rabbit_use_ssl', type='boolean', default='false', description="connect over SSL for RabbitMQ")

nova.param('rabbit_userid', type='string', default='guest', description="the RabbitMQ userid")

nova.param('rabbit_password', type='string', default='guest', description="the RabbitMQ password")

nova.param('rabbit_virtual_host', type='string', default='/', description="the RabbitMQ virtual host")

nova.param('rabbit_retry_interval', type='integer', default='1', description="how frequently to retry connecting with RabbitMQ")

nova.param('rabbit_retry_backoff', type='integer', default='2', description="how long to backoff for between retries when connecting to RabbitMQ")

nova.param('rabbit_max_retries', type='integer', default='0', description="maximum retries with trying to connect to RabbitMQ")

nova.param('rabbit_ha_queues', type='boolean', default='false', description="use H/A queues in RabbitMQ")

nova.param('qpid_hostname', type='string', default='localhost', description="Qpid broker hostname")

nova.param('qpid_port', type='integer', default='5672', description="Qpid broker port")

nova.param('qpid_hosts', type='list', default='$qpid_hostname:$qpid_port', description="Qpid HA cluster host:port pairs")

nova.param('qpid_username', type='string', default='', description="Username for qpid connection")

nova.param('qpid_password', type='string', default='', description="Password for qpid connection")

nova.param('qpid_sasl_mechanisms', type='string', default='', description="Space separated list of SASL mechanisms to use for auth")

nova.param('qpid_heartbeat', type='integer', default='60', description="Seconds between connection keepalive heartbeats")

nova.param('qpid_protocol', type='string', default='tcp', description="Transport to use, either 'tcp' or 'ssl'")

nova.param('qpid_tcp_nodelay', type='boolean', default='true', description="Disable Nagle algorithm")

nova.param('qpid_topology_version', type='integer', default='1', description="The qpid topology version to use.  Version 1 is what was originally used by impl_qpid.  Version 2 includes some backwards-incompatible changes that allow broker federation to work.  Users should update to version 2 when they are able to take everything down, as it requires a clean break.")

nova.param('rpc_zmq_bind_address', type='string', default='*', description="ZeroMQ bind address. Should be a wildcard")

nova.param('rpc_zmq_matchmaker', type='string', default='nova.openstack.common.rpc.matchmaker.MatchMakerLocalhost', description="MatchMaker driver")

nova.param('rpc_zmq_port', type='integer', default='9501', description="ZeroMQ receiver listening port")

nova.param('rpc_zmq_contexts', type='integer', default='1', description="Number of ZeroMQ contexts, defaults to 1")

nova.param('rpc_zmq_topic_backlog', type='integer', default='<None>', description="Maximum number of ingress messages to locally buffer per topic. Default is unlimited.")

nova.param('rpc_zmq_ipc_dir', type='string', default='/var/run/openstack', description="Directory for holding IPC sockets")

nova.param('rpc_zmq_host', type='string', default='nova', description="Name of this node. Must be a valid hostname, FQDN, or IP address. Must match 'host' option, if running Nova.")

nova.param('matchmaker_heartbeat_freq', type='integer', default='300', description="Heartbeat frequency")

nova.param('matchmaker_heartbeat_ttl', type='integer', default='600', description="Heartbeat time-to-live.")

nova.param('pci_alias', type='multi', default='', description="An alias for a PCI passthrough device requirement. This allows users to specify the alias in the extra_spec for a flavor, without needing to repeat all the PCI property requirements. For example: pci_alias = { 'name': 'QuicAssist',   'product_id': '0443',   'vendor_id': '8086', 'device_type': 'ACCEL' } defines an alias for the Intel QuickAssist card.")

nova.param('pci_passthrough_whitelist', type='multi', default='', description="White list of PCI devices available to VMs. For example: pci_passthrough_whitelist =  [{'vendor_id': '8086', 'product_id': '0443'}]")

nova.param('scheduler_host_manager', type='string', default='nova.scheduler.host_manager.HostManager', description="The scheduler host manager class to use")

nova.param('scheduler_max_attempts', type='integer', default='3', description="Maximum number of attempts to schedule an instance")

nova.param('scheduler_host_subset_size', type='integer', default='1', description="New instances will be scheduled on a host chosen randomly from a subset of the N best hosts. This property defines the subset size that a host is chosen from. A value of 1 chooses the first host returned by the weighing functions. This value must be at least 1. Any value less than 1 will be ignored, and 1 will be used instead")

nova.param('cpu_allocation_ratio', type='floating point', default='16.0', description="Virtual CPU to physical CPU allocation ratio which affects all CPU filters. This configuration specifies a global ratio for CoreFilter. For AggregateCoreFilter, it will fall back to this configuration value if no per-aggregate setting found.")

nova.param('disk_allocation_ratio', type='floating point', default='1.0', description="virtual disk to physical disk allocation ratio")

nova.param('max_io_ops_per_host', type='integer', default='8', description="Ignore hosts that have too many builds/resizes/snaps/migrations")

nova.param('isolated_images', type='list', default='', description="Images to run on isolated host")

nova.param('isolated_hosts', type='list', default='', description="Host reserved for specific images")

nova.param('restrict_isolated_hosts_to_isolated_images', type='boolean', default='true', description="Whether to force isolated hosts to run only isolated images")

nova.param('max_instances_per_host', type='integer', default='50', description="Ignore hosts that have too many instances")

nova.param('ram_allocation_ratio', type='floating point', default='1.5', description="Virtual ram to physical ram allocation ratio which affects all ram filters. This configuration specifies a global ratio for RamFilter. For AggregateRamFilter, it will fall back to this configuration value if no per-aggregate setting found.")

nova.param('scheduler_available_filters', type='multi', default='nova.scheduler.filters.all_filters', description="Filter classes available to the scheduler which may be specified more than once.  An entry of 'nova.scheduler.filters.standard_filters' maps to all filters included with nova.")

nova.param('scheduler_default_filters', type='list', default='RetryFilter,AvailabilityZoneFilter,RamFilter,ComputeFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter', description="Which filter class names to use for filtering hosts when not specified in the request.")

nova.param('scheduler_weight_classes', type='list', default='nova.scheduler.weights.all_weighers', description="Which weight class names to use for weighing hosts")

nova.param('scheduler_driver', type='string', default='nova.scheduler.filter_scheduler.FilterScheduler', description="Default driver to use for the scheduler")

nova.param('scheduler_topic', type='string', default='scheduler', description="the topic scheduler nodes listen on")

nova.param('scheduler_json_config_location', type='string', default='', description="Absolute path to scheduler configuration JSON file.")

nova.param('ram_weight_multiplier', type='floating point', default='1.0', description="Multiplier used for weighing ram.  Negative numbers mean to stack vs spread.")

nova.param('servicegroup_driver', type='string', default='db', description="The driver for servicegroup service")

nova.param('config_drive_format', type='string', default='iso9660', description="Config drive format. One of iso9660")

nova.param('config_drive_tempdir', type='string', default='<None>', description="Where to put temporary files associated with config drive creation")

nova.param('force_config_drive', type='string', default='<None>', description="Set to force injection to take place on a config drive")

nova.param('mkisofs_cmd', type='string', default='genisoimage', description="Name and optionally path of the tool used for ISO image creation")

nova.param('injected_network_template', type='string', default='$pybasedir/nova/virt/interfaces.template', description="Template file for injected network")

nova.param('virt_mkfs', type='multi', default='defaultmkfs.ext3 -L %(fs_label)s -F %(target)s', description="mkfs commands for ephemeral device. The format is <os_type>=<mkfs command>")

nova.param('virt_mkfs', type='string', default='linuxmkfs.ext3 -L %(fs_label)s -F %(target)s', description="")

nova.param('virt_mkfs', type='string', default='windowsmkfs.ntfs --force --fast --label %(fs_label)s %(target)s', description="")

nova.param('resize_fs_using_block_device', type='boolean', default='true', description="Attempt to resize the filesystem by accessing the image over a block device. This is done by the host and may not be necessary if the image contains a recent version of cloud- init. Possible mechanisms require the nbd driver")

nova.param('timeout_nbd', type='integer', default='10', description="time to wait for a NBD device coming up")

nova.param('docker_registry_default_port', type='integer', default='5042', description="Default TCP port to find the docker-registry container")

nova.param('compute_driver', type='string', default='<None>', description="Driver to use for controlling virtualization. Options include: libvirt.LibvirtDriver, xenapi.XenAPIDriver, fake.FakeDriver, baremetal.BareMetalDriver, vmwareapi.VMwareESXDriver, vmwareapi.VMwareVCDriver")

nova.param('default_ephemeral_format', type='string', default='<None>', description="The default format an ephemeral_volume will be formatted with on creation.")

nova.param('preallocate_images', type='string', default='none', description="VM image preallocation mode: 'none' => no storage provisioning is done up front, 'space' => storage is fully allocated at instance start")

nova.param('use_cow_images', type='boolean', default='true', description="Whether to use cow images")

nova.param('firewall_driver', type='string', default='<None>', description="Firewall driver")

nova.param('allow_same_net_traffic', type='boolean', default='true', description="Whether to allow network traffic from same network")

nova.param('force_raw_images', type='boolean', default='true', description="Force backing images to raw format")

nova.param('rescue_image_id', type='string', default='<None>', description="Rescue ami image")

nova.param('rescue_kernel_id', type='string', default='<None>', description="Rescue aki image")

nova.param('rescue_ramdisk_id', type='string', default='<None>', description="Rescue ari image")

nova.param('libvirt_type', type='string', default='kvm', description="Libvirt domain type")

nova.param('libvirt_uri', type='string', default='', description="Override the default libvirt URI")

nova.param('libvirt_inject_password', type='boolean', default='false', description="Inject the admin password at boot time, without an agent.")

nova.param('libvirt_inject_key', type='boolean', default='true', description="Inject the ssh public key at boot time")

nova.param('libvirt_inject_partition', type='integer', default='1', description="The partition to inject to : -2 => disable, -1 => inspect")

nova.param('use_usb_tablet', type='boolean', default='true', description="Sync virtual and real mouse cursors in Windows VMs")

nova.param('live_migration_uri', type='string', default='qemu+tcp://%s/system', description="Migration target URI")

nova.param('live_migration_flag', type='string', default='VIR_MIGRATE_UNDEFINE_SOURCE, VIR_MIGRATE_PEER2PEER', description="Migration flags to be set for live migration")

nova.param('block_migration_flag', type='string', default='VIR_MIGRATE_UNDEFINE_SOURCE, VIR_MIGRATE_PEER2PEER, VIR_MIGRATE_NON_SHARED_INC', description="Migration flags to be set for block migration")

nova.param('live_migration_bandwidth', type='integer', default='0', description="Maximum bandwidth to be used during migration, in Mbps")

nova.param('snapshot_image_format', type='string', default='<None>', description="Snapshot image format")

nova.param('libvirt_vif_driver', type='string', default='nova.virt.libvirt.vif.LibvirtGenericVIFDriver', description="The libvirt VIF driver to configure the VIFs.")

nova.param('libvirt_volume_drivers', type='list', default='iscsinova.virt.libvirt.volume.LibvirtISCSIVolumeDriver,isernova.virt.libvirt.volume.LibvirtISERVolumeDriver,localnova.virt.libvirt.volume.LibvirtVolumeDriver,fakenova.virt.libvirt.volume.LibvirtFakeVolumeDriver,rbdnova.virt.libvirt.volume.LibvirtNetVolumeDriver,sheepdognova.virt.libvirt.volume.LibvirtNetVolumeDriver,nfsnova.virt.libvirt.volume.LibvirtNFSVolumeDriver,aoenova.virt.libvirt.volume.LibvirtAOEVolumeDriver,glusterfsnova.virt.libvirt.volume.LibvirtGlusterfsVolumeDriver,fibre_channelnova.virt.libvirt.volume.LibvirtFibreChannelVolumeDriver,scalitynova.virt.libvirt.volume.LibvirtScalityVolumeDriver', description="Libvirt handlers for remote volumes.")

nova.param('libvirt_disk_prefix', type='string', default='<None>', description="Override the default disk prefix for the devices attached to a server, which is dependent on libvirt_type.")

nova.param('libvirt_wait_soft_reboot_seconds', type='integer', default='120', description="Number of seconds to wait for instance to shut down after soft reboot request is made. We fall back to hard reboot if instance does not shutdown within this window.")

nova.param('libvirt_nonblocking', type='boolean', default='true', description="Use a separated OS thread pool to realize non-blocking libvirt calls")

nova.param('libvirt_cpu_mode', type='string', default='<None>', description="Set to 'host-model' to clone the host CPU feature flags; to 'host-passthrough' to use the host CPU model exactly; to 'custom' to use a named CPU model; to 'none' to not set any CPU model. If libvirt_type='kvm|qemu', it will default to 'host-model', otherwise it will default to 'none'")

nova.param('libvirt_cpu_model', type='string', default='<None>', description="Set to a named libvirt CPU model")

nova.param('libvirt_snapshots_directory', type='string', default='$instances_path/snapshots', description="Location where libvirt driver will store snapshots before uploading them to image service")

nova.param('xen_hvmloader_path', type='string', default='/usr/lib/xen/boot/hvmloader', description="Location where the Xen hvmloader is kept")

nova.param('disk_cachemodes', type='list', default='', description="Specific cachemodes to use for different disk types e.g: ['file=directsync','block=none']")

nova.param('vcpu_pin_set', type='string', default='<None>', description="Which pcpus can be used by vcpus of instance e.g: '4-12,^8,15'")

nova.param('libvirt_images_type', type='string', default='default', description="VM Images format. Acceptable values are: raw, qcow2, lvm,rbd, default. If default is specified, then use_cow_images flag is used instead of this one.")

nova.param('libvirt_images_volume_group', type='string', default='<None>', description="LVM Volume Group that is used for VM images, when you specify libvirt_images_type=lvm.")

nova.param('libvirt_sparse_logical_volumes', type='boolean', default='false', description="Create sparse logical volumes")

nova.param('libvirt_lvm_snapshot_size', type='integer', default='1000', description="The amount of storage")

nova.param('libvirt_images_rbd_pool', type='string', default='rbd', description="the RADOS pool in which rbd volumes are stored")

nova.param('libvirt_images_rbd_ceph_conf', type='string', default='', description="path to the ceph configuration file to use")

nova.param('base_dir_name', type='string', default='_base', description="Where cached images are stored under $instances_path.This is NOT the full path - just a folder name.For per-compute-host cached images, set to _base_$my_ip")

nova.param('image_info_filename_pattern', type='string', default='$instances_path/$base_dir_name/%(image)s.info', description="Allows image information files to be stored in non-standard locations")

nova.param('remove_unused_base_images', type='boolean', default='true', description="Should unused base images be removed?")

nova.param('remove_unused_kernels', type='boolean', default='false', description="Should unused kernel images be removed? This is only safe to enable if all compute nodes have been updated to support this option. This will enabled by default in future.")

nova.param('remove_unused_resized_minimum_age_seconds', type='integer', default='3600', description="Unused resized base images younger than this will not be removed")

nova.param('remove_unused_original_minimum_age_seconds', type='integer', default='86400', description="Unused unresized base images younger than this will not be removed")

nova.param('checksum_base_images', type='boolean', default='false', description="Write a checksum for files in _base to disk")

nova.param('checksum_interval_seconds', type='integer', default='3600', description="How frequently to checksum base images")

nova.param('libvirt_snapshot_compression', type='boolean', default='false', description="Compress snapshot images when possible. This currently applies exclusively to qcow2 images")

nova.param('libvirt_ovs_bridge', type='string', default='br-int', description="Name of Integration Bridge used by Open vSwitch")

nova.param('libvirt_use_virtio_for_bridges', type='boolean', default='true', description="Use virtio for bridge interfaces with KVM/QEMU")

nova.param('num_iscsi_scan_tries', type='integer', default='3', description="number of times to rescan iSCSI target to find volume")

nova.param('num_iser_scan_tries', type='integer', default='3', description="number of times to rescan iSER target to find volume")

nova.param('rbd_user', type='string', default='<None>', description="the RADOS client name for accessing rbd volumes")

nova.param('rbd_secret_uuid', type='string', default='<None>', description="the libvirt uuid of the secret for the rbd_uservolumes")

nova.param('nfs_mount_point_base', type='string', default='$state_path/mnt', description="Dir where the nfs volume is mounted on the compute node")

nova.param('nfs_mount_options', type='string', default='<None>', description="Mount options passed to the nfs client. See section of the nfs man page for details")

nova.param('num_aoe_discover_tries', type='integer', default='3', description="number of times to rediscover AoE target to find volume")

nova.param('glusterfs_mount_point_base', type='string', default='$state_path/mnt', description="Dir where the glusterfs volume is mounted on the compute node")

nova.param('libvirt_iscsi_use_multipath', type='boolean', default='false', description="use multipath connection of the iSCSI volume")

nova.param('libvirt_iser_use_multipath', type='boolean', default='false', description="use multipath connection of the iSER volume")

nova.param('scality_sofs_config', type='string', default='<None>', description="Path or URL to Scality SOFS configuration file")

nova.param('scality_sofs_mount_point', type='string', default='$state_path/scality', description="Base dir where Scality SOFS shall be mounted")

nova.param('qemu_allowed_storage_drivers', type='list', default='', description="Protocols listed here will be accessed directly from QEMU. Currently supported protocols: [gluster]")

nova.param('powervm_mgr_type', type='string', default='ivm', description="PowerVM manager type")

nova.param('powervm_mgr', type='string', default='<None>', description="PowerVM manager host or ip")

nova.param('powervm_mgr_user', type='string', default='<None>', description="PowerVM manager user name")

nova.param('powervm_mgr_passwd', type='string', default='<None>', description="PowerVM manager user password")

nova.param('powervm_img_remote_path', type='string', default='/home/padmin', description="PowerVM image remote path where images will be moved. Make sure this path can fit your biggest image in glance")

nova.param('powervm_img_local_path', type='string', default='/tmp', description="Local directory to download glance images to. Make sure this path can fit your biggest image in glance")

nova.param('agent_timeout', type='integer', default='30', description="number of seconds to wait for agent reply")

nova.param('agent_version_timeout', type='integer', default='300', description="number of seconds to wait for agent to be fully operational")

nova.param('agent_resetnetwork_timeout', type='integer', default='60', description="number of seconds to wait for agent reply to resetnetwork request")

nova.param('xenapi_agent_path', type='string', default='usr/sbin/xe-update-networking', description="Specifies the path in which the xenapi guest agent should be located. If the agent is present, network configuration is not injected into the image. Used if compute_driver=xenapi.XenAPIDriver and  flat_injected=True")

nova.param('xenapi_disable_agent', type='boolean', default='false', description="Disables the use of the XenAPI agent in any image regardless of what image properties are present. ")

nova.param('xenapi_use_agent_default', type='boolean', default='false', description="Determines if the xenapi agent should be used when the image used does not contain a hint to declare if the agent is present or not. The hint is a glance property 'xenapi_use_agent' that has the value 'true' or 'false'. Note that waiting for the agent when it is not present will significantly increase server boot times.")

nova.param('xenapi_connection_url', type='string', default='<None>', description="URL for connection to XenServer/Xen Cloud Platform. A special value of unix://local can be used to connect to the local unix socket.  Required if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_connection_username', type='string', default='root', description="Username for connection to XenServer/Xen Cloud Platform. Used only if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_connection_password', type='string', default='<None>', description="Password for connection to XenServer/Xen Cloud Platform. Used only if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_connection_concurrent', type='integer', default='5', description="Maximum number of concurrent XenAPI connections. Used only if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_vhd_coalesce_poll_interval', type='floating point', default='5.0', description="The interval used for polling of coalescing vhds. Used only if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_check_host', type='boolean', default='true', description="Ensure compute service is running on host XenAPI connects to.")

nova.param('xenapi_vhd_coalesce_max_attempts', type='integer', default='5', description="Max number of times to poll for VHD to coalesce. Used only if compute_driver=xenapi.XenAPIDriver")

nova.param('xenapi_sr_base_path', type='string', default='/var/run/sr-mount', description="Base path to the storage repository")

nova.param('target_host', type='string', default='<None>', description="iSCSI Target Host")

nova.param('target_port', type='string', default='3260', description="iSCSI Target Port, 3260 Default")

nova.param('iqn_prefix', type='string', default='iqn.2010-10.org.openstack', description="IQN Prefix")

nova.param('xenapi_remap_vbd_dev', type='boolean', default='false', description="Used to enable the remapping of VBD dev")

nova.param('xenapi_remap_vbd_dev_prefix', type='string', default='sd', description="Specify prefix to remap VBD dev to")

nova.param('xenapi_login_timeout', type='integer', default='10', description="Timeout in seconds for XenAPI login.")

nova.param('xenapi_torrent_base_url', type='string', default='<None>', description="Base URL for torrent files.")

nova.param('xenapi_torrent_seed_chance', type='floating point', default='1.0', description="Probability that peer will become a seeder.")

nova.param('xenapi_torrent_seed_duration', type='integer', default='3600', description="Number of seconds after downloading an image via BitTorrent that it should be seeded for other peers.")

nova.param('xenapi_torrent_max_last_accessed', type='integer', default='86400', description="Cached torrent files not accessed within this number of seconds can be reaped")

nova.param('xenapi_torrent_listen_port_start', type='integer', default='6881', description="Beginning of port range to listen on")

nova.param('xenapi_torrent_listen_port_end', type='integer', default='6891', description="End of port range to listen on")

nova.param('xenapi_torrent_download_stall_cutoff', type='integer', default='600', description="Number of seconds a download can remain at the same progress percentage w/o being considered a stall")

nova.param('xenapi_torrent_max_seeder_processes_per_host', type='integer', default='1', description="Maximum number of seeder processes to run concurrently within a given dom0.")

nova.param('use_join_force', type='boolean', default='true', description="To use for hosts with different CPUs")

nova.param('xenapi_ovs_integration_bridge', type='string', default='xapi1', description="Name of Integration Bridge used by Open vSwitch")

nova.param('cache_images', type='string', default='all', description="Cache glance images locally. `all` will cache all images, `some` will only cache images that have the image_property `cache_in_nova=True`, and `none` turns off caching entirely")

nova.param('xenapi_image_compression_level', type='integer', default='<None>', description="Compression level for images, e.g., 9 for gzip -9. Range is 1-9, 9 being most compressed but most CPU intensive on dom0.")

nova.param('default_os_type', type='string', default='linux', description="Default OS type")

nova.param('block_device_creation_timeout', type='integer', default='10', description="Time to wait for a block device to be created")

nova.param('max_kernel_ramdisk_size', type='integer', default='16777216', description="Maximum size in bytes of kernel or ramdisk images")

nova.param('sr_matching_filter', type='string', default='default-sr:true', description="Filter for finding the SR to be used to install guest instances on. To use the Local Storage in default XenServer/XCP installations set this flag to other-config :i18n-key=local-storage. To select an SR with a different matching criteria, you could set it to other- config:my_favorite_sr=true. On the other hand, to fall back on the Default SR, as displayed by XenCenter, set this flag to: default-sr:true")

nova.param('xenapi_sparse_copy', type='boolean', default='true', description="Whether to use sparse_copy for copying data on a resize down")

nova.param('xenapi_num_vbd_unplug_retries', type='integer', default='10', description="Maximum number of retries to unplug VBD")

nova.param('xenapi_torrent_images', type='string', default='none', description="Whether or not to download images via Bit Torrent")

nova.param('xenapi_ipxe_network_name', type='string', default='<None>', description="Name of network to use for booting iPXE ISOs")

nova.param('xenapi_ipxe_boot_menu_url', type='string', default='<None>', description="URL to the iPXE boot menu")

nova.param('xenapi_ipxe_mkisofs_cmd', type='string', default='mkisofs', description="Name and optionally path of the tool used for ISO image creation")

nova.param('xenapi_running_timeout', type='integer', default='60', description="number of seconds to wait for instance to go to running state")

nova.param('xenapi_vif_driver', type='string', default='nova.virt.xenapi.vif.XenAPIBridgeDriver', description="The XenAPI VIF driver using XenServer Network APIs.")

nova.param('xenapi_image_upload_handler', type='string', default='nova.virt.xenapi.image.glance.GlanceStore', description="Dom0 plugin driver used to handle image uploads.")

nova.param('novncproxy_base_url', type='string', default='http://127.0.0.1:6080/vnc_auto.html', description="location of vnc console proxy, in the form 'http://127.0.0.1:6080/vnc_auto.html'")

nova.param('xvpvncproxy_base_url', type='string', default='http://127.0.0.1:6081/console', description="location of nova xvp vnc console proxy, in the form 'http://127.0.0.1:6081/console'")

nova.param('vncserver_listen', type='string', default='127.0.0.1', description="IP address on which instance vncservers should listen")

nova.param('vncserver_proxyclient_address', type='string', default='127.0.0.1', description="the address to which proxy clients")

nova.param('vnc_enabled', type='boolean', default='true', description="enable vnc related features")

nova.param('vnc_keymap', type='string', default='en-us', description="keymap for vnc")

nova.param('xvpvncproxy_port', type='integer', default='6081', description="Port that the XCP VNC proxy should bind to")

nova.param('xvpvncproxy_host', type='string', default='0.0.0.0', description="Address that the XCP VNC proxy should bind to")

nova.param('volume_api_class', type='string', default='nova.volume.cinder.API', description="The full class name of the volume API class to use")

nova.param('cinder_catalog_info', type='string', default='volume:cinder:publicURL', description="Info to match when looking for cinder in the service catalog. Format is : separated values of the form: <service_type>:<service_name>:<endpoint_type>")

nova.param('cinder_endpoint_template', type='string', default='<None>', description="Override service catalog lookup with template for cinder endpoint e.g. http://localhost:8776/v1/%(project_id)s")

nova.param('os_region_name', type='string', default='<None>', description="region name of this node")

nova.param('cinder_ca_certificates_file', type='string', default='<None>', description="Location of ca certicates file to use for cinder client requests.")

nova.param('cinder_http_retries', type='integer', default='3', description="Number of cinderclient retries on failed http calls")

nova.param('cinder_api_insecure', type='boolean', default='false', description="Allow to perform insecure SSL requests to cinder")

nova.param('cinder_cross_az_attach', type='boolean', default='true', description="Allow attach between instance and volume in different availability zones.")

nova.section('hyperv')

nova.param('instances_path_share', type='string', default='', description="The name of a Windows share name mapped to the 'instances_path' dir and used by the resize feature to copy files to the target host. If left blank, an administrative share will be used, looking for the same 'instances_path' used locally")

nova.param('force_hyperv_utils_v1', type='boolean', default='false', description="Force V1 WMI utility classes")

nova.param('force_volumeutils_v1', type='boolean', default='false', description="Force V1 volume utility class")

nova.param('vswitch_name', type='string', default='<None>', description="External virtual switch Name, if not provided, the first external virtual switch is used")

nova.param('limit_cpu_features', type='boolean', default='false', description="Required for live migration among hosts with different CPU features")

nova.param('config_drive_inject_password', type='boolean', default='false', description="Sets the admin password in the config drive image")

nova.param('qemu_img_cmd', type='string', default='qemu-img.exe', description="qemu-img is used to convert between different image types")

nova.param('config_drive_cdrom', type='boolean', default='false', description="Attaches the Config Drive image as a cdrom drive instead of a disk drive")

nova.param('enable_instance_metrics_collection', type='boolean', default='false', description="Enables metrics collections for an instance by using Hyper-V's metric APIs. Collected data can by retrieved by other apps and services, e.g.: Ceilometer. Requires Hyper-V / Windows Server 2012 and above")

nova.param('dynamic_memory_ratio', type='floating point', default='1.0', description="Enables dynamic memory allocation")

nova.param('volume_attach_retry_count', type='integer', default='10', description="The number of times to retry to attach a volume")

nova.param('volume_attach_retry_interval', type='integer', default='5', description="Interval between volume attachment attempts, in seconds")

nova.section('zookeeper')

nova.param('address', type='string', default='<None>', description="The ZooKeeper addresses for servicegroup service in the format of host1:port,host2:port,host3:port")

nova.param('recv_timeout', type='integer', default='4000', description="recv_timeout parameter for the zk session")

nova.param('sg_prefix', type='string', default='/servicegroups', description="The prefix used in ZooKeeper to store ephemeral nodes")

nova.param('sg_retry_interval', type='integer', default='5', description="Number of seconds to wait until retrying to join the session")

nova.section('osapi_v3')

nova.param('enabled', type='boolean', default='false', description="Whether the V3 API is enabled or not")

nova.param('extensions_blacklist', type='list', default='', description="A list of v3 API extensions to never load. Specify the extension aliases here.")

nova.param('extensions_whitelist', type='list', default='', description="If the list is not empty then a v3 API extension will only be loaded if it exists in this list. Specify the extension aliases here.")

nova.section('conductor')

nova.param('use_local', type='boolean', default='false', description="Perform nova-conductor operations locally")

nova.param('topic', type='string', default='conductor', description="the topic conductor nodes listen on")

nova.param('manager', type='string', default='nova.conductor.manager.ConductorManager', description="full class name for the Manager for conductor")

nova.param('workers', type='integer', default='<None>', description="Number of workers for OpenStack Conductor service")

nova.section('keymgr')

nova.param('api_class', type='string', default='nova.keymgr.conf_key_mgr.ConfKeyManager', description="The full class name of the key manager API class")

nova.param('fixed_key', type='string', default='<None>', description="Fixed key returned by key manager, specified in hex")

nova.section('cells')

nova.param('driver', type='string', default='nova.cells.rpc_driver.CellsRPCDriver', description="Cells communication driver to use")

nova.param('instance_updated_at_threshold', type='integer', default='3600', description="Number of seconds after an instance was updated or deleted to continue to update cells")

nova.param('instance_update_num_instances', type='integer', default='1', description="Number of instances to update per periodic task run")

nova.param('max_hop_count', type='integer', default='10', description="Maximum number of hops for cells routing.")

nova.param('scheduler', type='string', default='nova.cells.scheduler.CellsScheduler', description="Cells scheduler to use")

nova.param('enable', type='boolean', default='false', description="Enable cell functionality")

nova.param('topic', type='string', default='cells', description="the topic cells nodes listen on")

nova.param('manager', type='string', default='nova.cells.manager.CellsManager', description="Manager for cells")

nova.param('name', type='string', default='nova', description="name of this cell")

nova.param('capabilities', type='list', default='hypervisorxenserver;kvm,oslinux;windows', description="Key/Multi-value list with the capabilities of the cell")

nova.param('call_timeout', type='integer', default='60', description="Seconds to wait for response from a call to a cell.")

nova.param('reserve_percent', type='floating point', default='10.0', description="Percentage of cell capacity to hold in reserve. Affects both memory and disk utilization")

nova.param('cell_type', type='string', default='<None>', description="Type of cell: api or compute")

nova.param('mute_child_interval', type='integer', default='300', description="Number of seconds after which a lack of capability and capacity updates signals the child cell is to be treated as a mute.")

nova.param('bandwidth_update_interval', type='integer', default='600', description="Seconds between bandwidth updates for cells.")

nova.param('rpc_driver_queue_base', type='string', default='cells.intercell', description="Base queue name to use when communicating between cells. Various topics by message type will be appended to this.")

nova.param('scheduler_filter_classes', type='list', default='nova.cells.filters.all_filters', description="Filter classes the cells scheduler should use.  An entry of 'nova.cells.filters.all_filters'maps to all cells filters included with nova.")

nova.param('scheduler_weight_classes', type='list', default='nova.cells.weights.all_weighers', description="Weigher classes the cells scheduler should use.  An entry of 'nova.cells.weights.all_weighers'maps to all cell weighers included with nova.")

nova.param('scheduler_retries', type='integer', default='10', description="How many retries when no cells are available.")

nova.param('scheduler_retry_delay', type='integer', default='2', description="How often to retry in seconds when no cells are available.")

nova.param('db_check_interval', type='integer', default='60', description="Seconds between getting fresh cell info from db.")

nova.param('cells_config', type='string', default='<None>', description="Configuration file from which to read cells configuration. If given, overrides reading cells from the database.")

nova.param('mute_weight_multiplier', type='floating point', default='-10.0', description="Multiplier used to weigh mute children. ")

nova.param('mute_weight_value', type='floating point', default='1000.0', description="Weight value assigned to mute children. ")

nova.param('ram_weight_multiplier', type='floating point', default='10.0', description="Multiplier used for weighing ram.  Negative numbers mean to stack vs spread.")

nova.section('database')

nova.param('backend', type='string', default='sqlalchemy', description="The backend to use for db")

nova.param('use_tpool', type='boolean', default='false', description="Enable the experimental use of thread pooling for all DB API calls")

nova.param('connection', type='string', default='sqlite:////nova/openstack/common/db/$sqlite_db', description="The SQLAlchemy connection string used to connect to the database")

nova.param('slave_connection', type='string', default='', description="The SQLAlchemy connection string used to connect to the slave database")

nova.param('idle_timeout', type='integer', default='3600', description="timeout before idle sql connections are reaped")

nova.param('min_pool_size', type='integer', default='1', description="Minimum number of SQL connections to keep open in a pool")

nova.param('max_pool_size', type='integer', default='<None>', description="Maximum number of SQL connections to keep open in a pool")

nova.param('max_retries', type='integer', default='10', description="maximum db connection retries during startup.")

nova.param('retry_interval', type='integer', default='10', description="interval between retries of opening a sql connection")

nova.param('max_overflow', type='integer', default='<None>', description="If set, use this value for max_overflow with sqlalchemy")

nova.param('connection_debug', type='integer', default='0', description="Verbosity of SQL debugging information. 0=None, 100=Everything")

nova.param('connection_trace', type='boolean', default='false', description="Add python stack traces to SQL as comment strings")

nova.param('pool_timeout', type='integer', default='<None>', description="If set, use this value for pool_timeout with sqlalchemy")

nova.section('image_file_url')

nova.param('filesystems', type='list', default='', description="A list of filesystems that will be configured in this file under the sections image_file_url:<list entry name>")

nova.section('baremetal')

nova.param('db_backend', type='string', default='sqlalchemy', description="The backend to use for bare-metal database")

nova.param('sql_connection', type='string', default='sqlite:///$state_path/baremetal_$sqlite_db', description="The SQLAlchemy connection string used to connect to the bare-metal database")

nova.param('inject_password', type='boolean', default='true', description="Whether baremetal compute injects password or not")

nova.param('injected_network_template', type='string', default='$pybasedir/nova/virt/baremetal/interfaces.template', description="Template file for injected network")

nova.param('vif_driver', type='string', default='nova.virt.baremetal.vif_driver.BareMetalVIFDriver', description="Baremetal VIF driver.")

nova.param('volume_driver', type='string', default='nova.virt.baremetal.volume_driver.LibvirtVolumeDriver', description="Baremetal volume driver.")

nova.param('instance_type_extra_specs', type='list', default='', description="a list of additional capabilities corresponding to instance_type_extra_specs for this compute host to advertise. Valid entries are name=value, pairs For example, 'key1:val1, key2:val2'")

nova.param('driver', type='string', default='nova.virt.baremetal.pxe.PXE', description="Baremetal driver back-end")

nova.param('power_manager', type='string', default='nova.virt.baremetal.ipmi.IPMI', description="Baremetal power management method")

nova.param('tftp_root', type='string', default='/tftpboot', description="Baremetal compute node's tftp root path")

nova.param('terminal', type='string', default='shellinaboxd', description="path to baremetal terminal program")

nova.param('terminal_cert_dir', type='string', default='<None>', description="path to baremetal terminal SSL cert(PEM)")

nova.param('terminal_pid_dir', type='string', default='$state_path/baremetal/console', description="path to directory stores pidfiles of baremetal_terminal")

nova.param('ipmi_power_retry', type='integer', default='5', description="maximal number of retries for IPMI operations")

nova.param('deploy_kernel', type='string', default='<None>', description="Default kernel image ID used in deployment phase")

nova.param('deploy_ramdisk', type='string', default='<None>', description="Default ramdisk image ID used in deployment phase")

nova.param('net_config_template', type='string', default='$pybasedir/nova/virt/baremetal/net-dhcp.ubuntu.template', description="Template file for injected network config")

nova.param('pxe_append_params', type='string', default='<None>', description="additional append parameters for baremetal PXE boot")

nova.param('pxe_config_template', type='string', default='$pybasedir/nova/virt/baremetal/pxe_config.template', description="Template file for PXE configuration")

nova.param('pxe_deploy_timeout', type='integer', default='0', description="Timeout for PXE deployments. Default: 0")

nova.param('pxe_network_config', type='boolean', default='false', description="If set, pass the network configuration details to the initramfs via cmdline.")

nova.param('pxe_bootfile_name', type='string', default='pxelinux.0', description="This gets passed to Neutron as the bootfile dhcp parameter when the dhcp_options_enabled is set.")

nova.param('tile_pdu_ip', type='string', default='10.0.100.1', description="ip address of tilera pdu")

nova.param('tile_pdu_mgr', type='string', default='/tftpboot/pdu_mgr', description="management script for tilera pdu")

nova.param('tile_pdu_off', type='integer', default='2', description="power status of tilera PDU is OFF")

nova.param('tile_pdu_on', type='integer', default='1', description="power status of tilera PDU is ON")

nova.param('tile_pdu_status', type='integer', default='9', description="power status of tilera PDU")

nova.param('tile_power_wait', type='integer', default='9', description="wait time in seconds until check the result after tilera power operations")

nova.param('virtual_power_ssh_host', type='string', default='', description="ip or name to virtual power host")

nova.param('virtual_power_ssh_port', type='integer', default='22', description="Port to use for ssh to virtual power host")

nova.param('virtual_power_type', type='string', default='virsh', description="base command to use for virtual power(vbox,virsh)")

nova.param('virtual_power_host_user', type='string', default='', description="user to execute virtual power commands as")

nova.param('virtual_power_host_pass', type='string', default='', description="password for virtual power host_user")

nova.param('virtual_power_host_key', type='string', default='<None>', description="ssh key for virtual power host_user")

nova.param('use_unsafe_iscsi', type='boolean', default='false', description="Do not set this out of dev/test environments. If a node does not have a fixed PXE IP address, volumes are exported with globally opened ACL")

nova.param('iscsi_iqn_prefix', type='string', default='iqn.2010-10.org.openstack.baremetal', description="iSCSI IQN prefix used in baremetal volume connections.")

nova.section('rpc_notifier2')

nova.param('topics', type='list', default='notifications', description="AMQP topic(s) used for OpenStack notifications")

nova.section('matchmaker_redis')

nova.param('host', type='string', default='127.0.0.1', description="Host to locate redis")

nova.param('port', type='integer', default='6379', description="Use this port to connect to redis host.")

nova.param('password', type='string', default='<None>', description="Password for Redis server.")

nova.section('ssl')

nova.param('ca_file', type='string', default='<None>', description="CA certificate file to use to verify connecting clients")

nova.param('cert_file', type='string', default='<None>', description="Certificate file to use when starting the server securely")

nova.param('key_file', type='string', default='<None>', description="Private key file to use when starting the server securely")

nova.section('trusted_computing')

nova.param('attestation_server', type='string', default='<None>', description="attestation server http")

nova.param('attestation_server_ca_file', type='string', default='<None>', description="attestation server Cert file for Identity verification")

nova.param('attestation_port', type='string', default='8443', description="attestation server port")

nova.param('attestation_api_url', type='string', default='/OpenAttestationWebServices/V1.0', description="attestation web API URL")

nova.param('attestation_auth_blob', type='string', default='<None>', description="attestation authorization blob - must change")

nova.param('attestation_auth_timeout', type='integer', default='60', description="Attestation status cache valid period length")

nova.section('upgrade_levels')

nova.param('baseapi', type='string', default='<None>', description="Set a version cap for messages sent to the base api in any service")

nova.param('intercell', type='string', default='<None>', description="Set a version cap for messages sent between cells services")

nova.param('cells', type='string', default='<None>', description="Set a version cap for messages sent to local cells services")

nova.param('cert', type='string', default='<None>', description="Set a version cap for messages sent to cert services")

nova.param('compute', type='string', default='<None>', description="Set a version cap for messages sent to compute services")

nova.param('conductor', type='string', default='<None>', description="Set a version cap for messages sent to conductor services")

nova.param('console', type='string', default='<None>', description="Set a version cap for messages sent to console services")

nova.param('consoleauth', type='string', default='<None>', description="Set a version cap for messages sent to consoleauth services")

nova.param('network', type='string', default='<None>', description="Set a version cap for messages sent to network services")

nova.param('scheduler', type='string', default='<None>', description="Set a version cap for messages sent to scheduler services")

nova.section('matchmaker_ring')

nova.param('ringfile', type='string', default='/etc/oslo/matchmaker_ring.json', description="Matchmaker ring file")

nova.section('vmware')

nova.param('host_ip', type='string', default='<None>', description="URL for connection to VMware ESX/VC host. Required if compute_driver is vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.")

nova.param('host_username', type='string', default='<None>', description="Username for connection to VMware ESX/VC host. Used only if compute_driver is vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.")

nova.param('host_password', type='string', default='<None>', description="Password for connection to VMware ESX/VC host. Used only if compute_driver is vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.")

nova.param('cluster_name', type='multi', default='<None>', description="Name of a VMware Cluster ComputeResource. Used only if compute_driver is vmwareapi.VMwareVCDriver.")

nova.param('datastore_regex', type='string', default='<None>', description="Regex to match the name of a datastore. Used only if compute_driver is vmwareapi.VMwareVCDriver.")

nova.param('task_poll_interval', type='floating point', default='5.0', description="The interval used for polling of remote tasks. Used only if compute_driver is vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.")

nova.param('api_retry_count', type='integer', default='10', description="The number of times we retry on failures, e.g., socket error, etc. Used only if compute_driver is vmwareapi.VMwareESXDriver or vmwareapi.VMwareVCDriver.")

nova.param('vnc_port', type='integer', default='5900', description="VNC starting port")

nova.param('vnc_port_total', type='integer', default='10000', description="Total number of VNC ports")

nova.param('vnc_password', type='string', default='<None>', description="VNC password")

nova.param('use_linked_clone', type='boolean', default='true', description="Whether to use linked clone")

nova.param('vlan_interface', type='string', default='vmnic0', description="Physical ethernet adapter name for vlan networking")

nova.param('wsdl_location', type='string', default='<None>', description="Optional VIM Service WSDL Location e.g http://<server>/vimService.wsdl. Optional over-ride to default location for bug work-arounds")

nova.param('maximum_objects', type='integer', default='100', description="The maximum number of ObjectContent data objects that should be returned in a single result. A positive value will cause the operation to suspend the retrieval when the count of objects reaches the specified maximum. The server may still limit the count to something less than the configured value. Any remaining objects may be retrieved with additional requests.")

nova.param('integration_bridge', type='string', default='br-int', description="Name of Integration Bridge")

nova.section('spice')

nova.param('html5proxy_base_url', type='string', default='http://127.0.0.1:6082/spice_auto.html', description="location of spice html5 console proxy, in the form 'http://127.0.0.1:6082/spice_auto.html'")

nova.param('server_listen', type='string', default='127.0.0.1', description="IP address on which instance spice server should listen")

nova.param('server_proxyclient_address', type='string', default='127.0.0.1', description="the address to which proxy clients")

nova.param('enabled', type='boolean', default='false', description="enable spice related features")

nova.param('agent_enabled', type='boolean', default='true', description="enable spice guest agent support")

nova.param('keymap', type='string', default='en-us', description="keymap for spice")

