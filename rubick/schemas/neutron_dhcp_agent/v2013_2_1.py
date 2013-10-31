from rubick.schema import ConfigSchemaRegistry

neutron_dhcp_agent = ConfigSchemaRegistry.register_schema(
    project='neutron_dhcp_agent')

with neutron_dhcp_agent.version('2013.2.1') as neutron_dhcp_agent_2013_2_1:

    neutron_dhcp_agent_2013_2_1.section('DEFAULT')

    neutron_dhcp_agent_2013_2_1.param('debug', type='string', default='False',
                                      description="Show debugging output in log (sets DEBUG log level output)")

    neutron_dhcp_agent_2013_2_1.param(
        'resync_interval', type='string', default='5',
        description="The DHCP agent will resync its state with Neutron to recover from any transient notification or rpc errors. The interval is number of seconds between attempts.")

    neutron_dhcp_agent_2013_2_1.param(
        'interface_driver', type='string', default='',
        description="The DHCP agent requires an interface driver be set. Choose the one that best matches your plugin.")

    neutron_dhcp_agent_2013_2_1.param(
        'interface_driver', type='string', default='neutron.agent.linux.interface.OVSInterfaceDriver',
        description="Example of interface_driver option for OVS based plugins(OVS, Ryu, NEC, NVP, BigSwitch/Floodlight)")

    neutron_dhcp_agent_2013_2_1.param(
        'ovs_use_veth', type='string', default='False',
        description="Use veth for an OVS interface or not. Support kernels with limited namespace support (e.g. RHEL 6.5) so long as ovs_use_veth is set to True.")

    neutron_dhcp_agent_2013_2_1.param(
        'interface_driver', type='string', default='neutron.agent.linux.interface.BridgeInterfaceDriver', description="Example of interface_driver option for LinuxBridge")

    neutron_dhcp_agent_2013_2_1.param(
        'dhcp_driver', type='string', default='neutron.agent.linux.dhcp.Dnsmasq',
        description="The agent can use other DHCP drivers.  Dnsmasq is the simplest and requires no additional setup of the DHCP server.")

    neutron_dhcp_agent_2013_2_1.param(
        'use_namespaces', type='string', default='True',
        description="Allow overlapping IP (Must have kernel build with CONFIG_NET_NS=y and iproute2 package that supports namespaces).")

    neutron_dhcp_agent_2013_2_1.param(
        'enable_isolated_metadata', type='string', default='False',
        description="The DHCP server can assist with providing metadata support on isolated networks. Setting this value to True will cause the DHCP server to append specific host routes to the DHCP request.  The metadata service will only be activated when the subnet gateway_ip is None.  The guest instance must be configured to request host routes via DHCP (Option 121).")

    neutron_dhcp_agent_2013_2_1.param(
        'enable_metadata_network', type='string', default='False',
        description="Allows for serving metadata requests coming from a dedicated metadata access network whose cidr is 169.254.169.254/16 (or larger prefix), and is connected to a Neutron router from which the VMs send metadata request. In this case DHCP Option 121 will not be injected in VMs, as they will be able to reach 169.254.169.254 through a router. This option requires enable_isolated_metadata = True")

    neutron_dhcp_agent_2013_2_1.param(
        'num_sync_threads', type='string', default='4',
        description="Number of threads to use during sync process. Should not exceed connection pool size configured on server.")

    neutron_dhcp_agent_2013_2_1.param(
        'dhcp_confs', type='string', default='$state_path/dhcp', description="Location to store DHCP server config files")

    neutron_dhcp_agent_2013_2_1.param(
        'dhcp_domain', type='string', default='openstacklocal', description="Domain to use for building the hostnames")

    neutron_dhcp_agent_2013_2_1.param('dnsmasq_config_file', type='string',
                                      default='', description="Override the default dnsmasq settings with this file")

    neutron_dhcp_agent_2013_2_1.param(
        'dnsmasq_dns_server', type='string', default='', description="Use another DNS server before any in /etc/resolv.conf.")

    neutron_dhcp_agent_2013_2_1.param(
        'dnsmasq_lease_max', type='string', default='16777216', description="Limit number of leases to prevent a denial-of-service.")

    neutron_dhcp_agent_2013_2_1.param('dhcp_lease_relay_socket', type='string',
                                      default='$state_path/dhcp/lease_relay', description="Location to DHCP lease relay UNIX domain socket")

    neutron_dhcp_agent_2013_2_1.param('metadata_proxy_socket', type='string',
                                      default='$state_path/metadata_proxy', description="Location of Metadata Proxy UNIX domain socket")
