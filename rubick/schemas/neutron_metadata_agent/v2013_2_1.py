from rubick.schema import ConfigSchemaRegistry

neutron_metadata_agent = ConfigSchemaRegistry.register_schema(
    project='neutron_metadata_agent')

with neutron_metadata_agent.version('2013.2.1') as neutron_metadata_agent_2013_2_1:

    neutron_metadata_agent_2013_2_1.section('DEFAULT')

    neutron_metadata_agent_2013_2_1.param(
        'debug', type='string', default='True', description="Show debugging output in log (sets DEBUG log level output)")

    neutron_metadata_agent_2013_2_1.param(
        'auth_url', type='string', default='http://localhost:5000/v2.0', description="The Neutron user information for accessing the Neutron API.")

    neutron_metadata_agent_2013_2_1.param(
        'auth_region', type='string', default='RegionOne', description="The Neutron user information for accessing the Neutron API.")

    neutron_metadata_agent_2013_2_1.param(
        'admin_tenant_name', type='string', default='%SERVICE_TENANT_NAME%', description="The Neutron user information for accessing the Neutron API.")

    neutron_metadata_agent_2013_2_1.param(
        'admin_user', type='string', default='%SERVICE_USER%', description="The Neutron user information for accessing the Neutron API.")

    neutron_metadata_agent_2013_2_1.param(
        'admin_password', type='string', default='%SERVICE_PASSWORD%', description="The Neutron user information for accessing the Neutron API.")

    neutron_metadata_agent_2013_2_1.param(
        'endpoint_type', type='string', default='adminURL', description="Network service endpoint type to pull from the keystone catalog")

    neutron_metadata_agent_2013_2_1.param(
        'nova_metadata_ip', type='string', default='127.0.0.1', description="IP address used by Nova metadata server")

    neutron_metadata_agent_2013_2_1.param(
        'nova_metadata_port', type='string', default='8775', description="TCP Port used by Nova metadata server")

    neutron_metadata_agent_2013_2_1.param(
        'metadata_proxy_shared_secret', type='string', default='',
        description="When proxying metadata requests, Neutron signs the Instance-ID header with a shared secret to prevent spoofing.  You may select any string for a secret, but it must match here and in the configuration used by the Nova Metadata Server. NOTE: Nova uses a different key: neutron_metadata_proxy_shared_secret")

    neutron_metadata_agent_2013_2_1.param(
        'metadata_proxy_socket', type='string', default='$state_path/metadata_proxy', description="Location of Metadata Proxy UNIX domain socket")
