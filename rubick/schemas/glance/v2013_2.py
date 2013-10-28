from rubick.schema import ConfigSchemaRegistry

glance = ConfigSchemaRegistry.register_schema(project='glance')

with glance.version('2013.2') as glance_2013_2:

    glance_2013_2.section('DEFAULT')

    glance_2013_2.param('verbose', type='string', default='False',
                        description="Show more verbose log output (sets INFO log level output)")

    glance_2013_2.param('debug', type='string', default='False',
                        description="Show debugging output in logs (sets DEBUG log level output)")

    glance_2013_2.param('default_store', type='string', default='file',
                        description="Which backend scheme should Glance use by default is not specified in a request to add a new image to Glance? Known schemes are determined by the known_stores option below. Default: 'file'")

    glance_2013_2.param(
        'known_stores', type='string', default='glance.store.filesystem.Store,',
        description="List of which store classes and store class locations are currently known to glance at startup.")

    glance_2013_2.param(
        'image_size_cap', type='string', default='1099511627776',
        description="Maximum image size (in bytes) that may be uploaded through the Glance API server. Defaults to 1 TB. WARNING: this value should only be increased after careful consideration and must be set to a value under 8 EB (9223372036854775808).")

    glance_2013_2.param('bind_host', type='host', default='0.0.0.0',
                        description="Address to bind the API server")

    glance_2013_2.param('bind_port', type='string',
                        default='9292', description="Port the bind the API server to")

    glance_2013_2.param(
        'log_file', type='string', default='/var/log/glance/api.log',
        description="Log to this file. Make sure you do not set the same log file for both the API and registry servers!")

    glance_2013_2.param('backlog', type='string', default='4096',
                        description="Backlog requests when creating socket")

    glance_2013_2.param('tcp_keepidle', type='string', default='600',
                        description="TCP_KEEPIDLE value in seconds when creating socket. Not supported on OS X.")

    glance_2013_2.param(
        'sql_connection', type='string', default='sqlite:///glance.sqlite',
        description="SQLAlchemy connection string for the reference implementation registry server. Any valid SQLAlchemy connection string is fine. See: http://www.sqlalchemy.org/docs/05/reference/sqlalchemy/connections.html#sqlalchemy.create_engine")

    glance_2013_2.param('sql_idle_timeout', type='string', default='3600',
                        description="MySQL uses a default `wait_timeout` of 8 hours, after which it will drop idle connections. This can result in 'MySQL Gone Away' exceptions. If you notice this, you can lower this value to ensure that SQLAlchemy reconnects before MySQL can drop the connection.")

    glance_2013_2.param('workers', type='string', default='1',
                        description="Number of Glance API worker processes to start. On machines with more than one CPU increasing this value may improve performance (especially if using SSL with compression turned on). It is typically recommended to set this value to the number of CPUs present on your machine.")

    glance_2013_2.param('admin_role', type='string', default='admin',
                        description="Role used to identify an authenticated user as administrator")

    glance_2013_2.param(
        'allow_anonymous_access', type='string', default='False',
        description="Allow unauthenticated users to access the API with read-only privileges. This only applies when using ContextMiddleware.")

    glance_2013_2.param('enable_v1_api', type='string', default='True',
                        description="Allow access to version 1 of glance api")

    glance_2013_2.param('enable_v2_api', type='string', default='True',
                        description="Allow access to version 2 of glance api")

    glance_2013_2.param(
        'show_image_direct_url', type='string', default='False',
        description="Return the URL that references where the data is stored on the backend storage system.  For example, if using the file system store a URL of 'file:///path/to/image' will be returned to the user in the 'direct_url' meta-data field. The default value is false.")

    glance_2013_2.param(
        'send_identity_headers', type='string', default='False',
        description="Send headers containing user and tenant information when making requests to the v1 glance registry. This allows the registry to function as if a user is authenticated without the need to authenticate a user itself using the auth_token middleware. The default value is false.")

    glance_2013_2.param(
        'container_formats', type='string', default='ami,ari,aki,bare,ovf',
        description="Supported values for the 'container_format' image attribute")

    glance_2013_2.param(
        'disk_formats', type='string', default='ami,ari,aki,vhd,vmdk,raw,qcow2,vdi,iso',
        description="Supported values for the 'disk_format' image attribute")

    glance_2013_2.param('lock_path', type='string', default=None,
                        description="Directory to use for lock files. Default to a temp directory (string value). This setting needs to be the same for both glance-scrubber and glance-api.")

    glance_2013_2.param('property_protection_file', type='string', default='',
                        description="Property Protections config file This file contains the rules for property protections and the roles associated with it. If this config value is not specified, by default, property protections won't be enforced. If a value is specified and the file is not found, then an HTTPInternalServerError will be thrown.")

    glance_2013_2.param('user_storage_quota', type='string', default='0',
                        description="Set a system wide quota for every user.  This value is the total number of bytes that a user can use across all storage systems.  A value of 0 means unlimited.")

    glance_2013_2.param('use_syslog', type='string', default='False',
                        description="Send logs to syslog (/dev/log) instead of to file specified by `log_file`")

    glance_2013_2.param(
        'syslog_log_facility', type='string', default='LOG_LOCAL0',
        description="Facility to use. If unset defaults to LOG_USER.")

    glance_2013_2.param(
        'cert_file', type='string', default='/path/to/certfile',
        description="Certificate file to use when starting API server securely")

    glance_2013_2.param('key_file', type='string', default='/path/to/keyfile',
                        description="Private key file to use when starting API server securely")

    glance_2013_2.param('ca_file', type='string', default='/path/to/cafile',
                        description="CA certificate file to use to verify connecting clients")

    glance_2013_2.param(
        'metadata_encryption_key', type='string', default='<16, 24 or 32 char registry metadata key>',
        description="AES key for encrypting store 'location' metadata, including -- if used -- Swift or S3 credentials Should be set to a random string of length 16, 24 or 32 bytes")

    glance_2013_2.param('registry_host', type='host', default='0.0.0.0',
                        description="Address to find the registry server")

    glance_2013_2.param('registry_port', type='string', default='9191',
                        description="Port the registry server is listening on")

    glance_2013_2.param(
        'registry_client_protocol', type='string', default='http',
        description="What protocol to use when connecting to the registry server? Set to https for secure HTTP communication")

    glance_2013_2.param(
        'registry_client_key_file', type='string', default='/path/to/key/file',
        description="The path to the key file to use in SSL connections to the registry server, if any. Alternately, you may set the GLANCE_CLIENT_KEY_FILE environ variable to a filepath of the key file")

    glance_2013_2.param(
        'registry_client_cert_file', type='string', default='/path/to/cert/file',
        description="The path to the cert file to use in SSL connections to the registry server, if any. Alternately, you may set the GLANCE_CLIENT_CERT_FILE environ variable to a filepath of the cert file")

    glance_2013_2.param(
        'registry_client_ca_file', type='string', default='/path/to/ca/file',
        description="The path to the certifying authority cert file to use in SSL connections to the registry server, if any. Alternately, you may set the GLANCE_CLIENT_CA_FILE environ variable to a filepath of the CA cert file")

    glance_2013_2.param(
        'registry_client_insecure', type='string', default='False',
        description="When using SSL in connections to the registry server, do not require validation via a certifying authority. This is the registry's equivalent of specifying --insecure on the command line using glanceclient for the API Default: False")

    glance_2013_2.param(
        'registry_client_timeout', type='string', default='600',
        description="The period of time, in seconds, that the API server will wait for a registry request to complete. A value of '0' implies no timeout. Default: 600")

    glance_2013_2.param('db_auto_create', type='string', default='False',
                        description="Whether to automatically create the database tables. Default: False")

    glance_2013_2.param('sqlalchemy_debug', type='string', default='True',
                        description="Enable DEBUG log messages from sqlalchemy which prints every database query and response. Default: False")

    glance_2013_2.param('notifier_strategy', type='string', default='noop',
                        description="Notifications can be sent when images are create, updated or deleted. There are three methods of sending notifications, logging (via the log_file directive), rabbit (via a rabbitmq queue), qpid (via a Qpid message queue), or noop (no notifications sent, the default)")

    glance_2013_2.param('rabbit_host', type='host', default='localhost',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param('rabbit_port', type='string', default='5672',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param('rabbit_use_ssl', type='string', default='false',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param('rabbit_userid', type='string', default='guest',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param('rabbit_password', type='string', default='guest',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param('rabbit_virtual_host', type='string', default='/',
                        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param(
        'rabbit_notification_exchange', type='string', default='glance',
        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param(
        'rabbit_notification_topic', type='string', default='notifications',
        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param(
        'rabbit_durable_queues', type='string', default='False',
        description="Configuration options if sending notifications via rabbitmq (these are the defaults)")

    glance_2013_2.param(
        'qpid_notification_exchange', type='string', default='glance',
        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param(
        'qpid_notification_topic', type='string', default='notifications',
        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_host', type='host', default='localhost',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_port', type='string', default='5672',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_username', type='string', default='',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_password', type='string', default='',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_sasl_mechanisms', type='string', default='',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_reconnect_timeout', type='string', default='0',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_reconnect_limit', type='string', default='0',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param(
        'qpid_reconnect_interval_min', type='string', default='0',
        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param(
        'qpid_reconnect_interval_max', type='string', default='0',
        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_reconnect_interval', type='string', default='0',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_heartbeat', type='string', default='5',
                        description="Configuration options if sending notifications via Qpid (these are the defaults)")

    glance_2013_2.param('qpid_protocol', type='string', default='tcp',
                        description="Configuration options if sending notifications via Qpid (these are the defaults) Set to 'ssl' to enable SSL")

    glance_2013_2.param('qpid_tcp_nodelay', type='string', default='True',
                        description="Configuration options if sending notifications via Qpid (these are the defaults) Set to 'ssl' to enable SSL")

    glance_2013_2.param(
        'filesystem_store_datadir', type='string', default='/var/lib/glance/images/',
        description="Directory that the Filesystem backend store writes image data to")

    glance_2013_2.param(
        'filesystem_store_metadata_file', type='string', default='None',
        description="A path to a JSON file that contains metadata describing the storage system.  When show_multiple_locations is True the information in this file will be returned with any location that is contained in this store.")

    glance_2013_2.param('swift_store_auth_version', type='string', default='2',
                        description="Version of the authentication service to use Valid versions are '2' for keystone and '1' for swauth and rackspace")

    glance_2013_2.param(
        'swift_store_auth_address', type='string', default='127.0.0.1:5000/v2.0/',
        description="Address where the Swift authentication service lives Valid schemes are 'http://' and 'https://' If no scheme specified,  default to 'https://' For swauth, use something like '127.0.0.1:8080/v1.0/'")

    glance_2013_2.param('swift_store_user', type='string', default='jdoe:jdoe',
                        description="User to authenticate against the Swift authentication service If you use Swift authentication service, set it to 'account':'user' where 'account' is a Swift storage account and 'user' is a user in that account")

    glance_2013_2.param(
        'swift_store_key', type='string', default='a86850deb2742ec3cb41518e26aa2d89',
        description="Auth key for the user authenticating against the Swift authentication service")

    glance_2013_2.param(
        'swift_store_container', type='string', default='glance',
        description="Container within the account that the account should use for storing images in Swift")

    glance_2013_2.param('swift_store_create_container_on_put', type='string',
                        default='False', description="Do we create the container if it does not exist?")

    glance_2013_2.param(
        'swift_store_large_object_size', type='string', default='5120',
        description="What size, in MB, should Glance start chunking image files and do a large object manifest in Swift? By default, this is the maximum object size in Swift, which is 5GB")

    glance_2013_2.param(
        'swift_store_large_object_chunk_size', type='string', default='200',
        description="When doing a large object manifest, what size, in MB, should Glance write chunks to Swift? This amount of data is written to a temporary disk buffer during the process of chunking the image file, and the default is 200MB")

    glance_2013_2.param('swift_enable_snet', type='string', default='False',
                        description="To use ServiceNET for authentication, prefix hostname of `swift_store_auth_address` with 'snet-'. Ex. https://example.com/v1.0/ -> https://snet-example.com/v1.0/")

    glance_2013_2.param(
        'swift_store_multi_tenant', type='string', default='False',
        description="If set to True enables multi-tenant storage mode which causes Glance images to be stored in tenant specific Swift accounts.")

    glance_2013_2.param('swift_store_admin_tenants', type='string', default='',
                        description="A list of swift ACL strings that will be applied as both read and write ACLs to the containers created by Glance in multi-tenant mode. This grants the specified tenants/users read and write access to all newly created image objects. The standard swift ACL string formats are allowed, including: <tenant_id>:<username> <tenant_name>:<username> *:<username> Multiple ACLs can be combined using a comma separated list, for example: swift_store_admin_tenants = service:glance,*:admin")

    glance_2013_2.param('swift_store_region', type='string', default='',
                        description="The region of the swift endpoint to be used for single tenant. This setting is only necessary if the tenant has multiple swift endpoints.")

    glance_2013_2.param(
        'swift_store_ssl_compression', type='string', default='True',
        description="If set to False, disables SSL layer compression of https swift requests. Setting to 'False' may improve performance for images which are already in a compressed format, eg qcow2. If set to True, enables SSL layer compression (provided it is supported by the target swift proxy).")

    glance_2013_2.param(
        's3_store_host', type='string', default='127.0.0.1:8080/v1.0/',
        description="Address where the S3 authentication service lives Valid schemes are 'http://' and 'https://' If no scheme specified,  default to 'http://'")

    glance_2013_2.param(
        's3_store_access_key', type='string', default='<20-char AWS access key>',
        description="User to authenticate against the S3 authentication service")

    glance_2013_2.param(
        's3_store_secret_key', type='string', default='<40-char AWS secret key>',
        description="Auth key for the user authenticating against the S3 authentication service")

    glance_2013_2.param(
        's3_store_bucket', type='string', default='<lowercased 20-char aws access key>glance',
        description="Container within the account that the account should use for storing images in S3. Note that S3 has a flat namespace, so you need a unique bucket name for your glance images. An easy way to do this is append your AWS access key to 'glance'. S3 buckets in AWS *must* be lowercased, so remember to lowercase your AWS access key if you use it in your bucket name below!")

    glance_2013_2.param('s3_store_create_bucket_on_put', type='string',
                        default='False', description="Do we create the bucket if it does not exist?")

    glance_2013_2.param(
        's3_store_object_buffer_dir', type='string', default='/path/to/dir',
        description="When sending images to S3, the data will first be written to a temporary buffer on disk. By default the platform's temporary directory will be used. If required, an alternative directory can be specified here.")

    glance_2013_2.param(
        's3_store_bucket_url_format', type='string', default='subdomain',
        description="When forming a bucket url, boto will either set the bucket name as the subdomain or as the first token of the path. Amazon's S3 service will accept it as the subdomain, but Swift's S3 middleware requires it be in the path. Set this to 'path' or 'subdomain' - defaults to 'subdomain'.")

    glance_2013_2.param(
        'rbd_store_ceph_conf', type='string', default='/etc/ceph/ceph.conf',
        description="Ceph configuration file path If using cephx authentication, this file should include a reference to the right keyring in a client.<USER> section")

    glance_2013_2.param('rbd_store_user', type='string', default='glance',
                        description="RADOS user to authenticate as (only applicable if using cephx)")

    glance_2013_2.param('rbd_store_pool', type='string', default='images',
                        description="RADOS pool in which images are stored")

    glance_2013_2.param('rbd_store_chunk_size', type='string', default='8',
                        description="Images will be chunked into objects of this size (in megabytes). For best performance, this should be a power of two")

    glance_2013_2.param('sheepdog_store_address',
                        type='string', default='localhost', description="")

    glance_2013_2.param(
        'sheepdog_store_port', type='string', default='7000', description="")

    glance_2013_2.param(
        'sheepdog_store_chunk_size', type='string', default='64',
        description="Images will be chunked into objects of this size (in megabytes). For best performance, this should be a power of two")

    glance_2013_2.param(
        'cinder_catalog_info', type='string', default='volume:cinder:publicURL',
        description="Info to match when looking for cinder in the service catalog Format is : separated values of the form: <service_type>:<service_name>:<endpoint_type> ")

    glance_2013_2.param(
        'cinder_endpoint_template', type='string', default=None,
        description="Override service catalog lookup with template for cinder endpoint e.g. http://localhost:8776/v1/%(project_id)s ")

    glance_2013_2.param('os_region_name', type='string',
                        default=None, description="Region name of this node ")

    glance_2013_2.param(
        'cinder_ca_certificates_file', type='string', default=None,
        description="Location of ca certicates file to use for cinder client requests ")

    glance_2013_2.param('cinder_http_retries', type='integer', default=3,
                        description="Number of cinderclient retries on failed http calls ")

    glance_2013_2.param('cinder_api_insecure', type='boolean', default=False,
                        description="Allow to perform insecure SSL requests to cinder ")

    glance_2013_2.param('delayed_delete', type='string',
                        default='False', description="Turn on/off delayed delete")

    glance_2013_2.param('scrub_time', type='string',
                        default='43200', description="Delayed delete time in seconds")

    glance_2013_2.param(
        'scrubber_datadir', type='string', default='/var/lib/glance/scrubber',
        description="Directory that the scrubber will use to remind itself of what to delete Make sure this is also set in glance-scrubber.conf")

    glance_2013_2.param(
        'image_cache_dir', type='string', default='/var/lib/glance/image-cache/',
        description="Base directory that the Image Cache uses")

    glance_2013_2.section('keystone_authtoken')

    glance_2013_2.param(
        'auth_host', type='host', default='127.0.0.1', description="")

    glance_2013_2.param(
        'auth_port', type='string', default='35357', description="")

    glance_2013_2.param(
        'auth_protocol', type='string', default='http', description="")

    glance_2013_2.param('admin_tenant_name', type='string',
                        default='%SERVICE_TENANT_NAME%', description="")

    glance_2013_2.param(
        'admin_user', type='string', default='%SERVICE_USER%', description="")

    glance_2013_2.param('admin_password', type='string',
                        default='%SERVICE_PASSWORD%', description="")

    glance_2013_2.section('paste_deploy')

    glance_2013_2.param(
        'config_file', type='string', default='glance-api-paste.ini',
        description="Name of the paste configuration file that defines the available pipelines")

    glance_2013_2.param('flavor', type='string', default='',
                        description="Partial name of a pipeline in your paste configuration file with the service name removed. For example, if your paste section name is [pipeline:glance-api-keystone], you would configure the flavor below as 'keystone'.")
