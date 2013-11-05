from rubick.schema import ConfigSchemaRegistry

neutron_l3_agent = ConfigSchemaRegistry.register_schema(
    project='neutron_l3_agent')

with neutron_l3_agent.version('2013.2.1') as neutron_l3_agent_2013_2_1:

    neutron_l3_agent_2013_2_1.section('DEFAULT')

    neutron_l3_agent_2013_2_1.param('debug', type='string', default='False',
                                    description="Show debugging output in log (sets DEBUG log level output)")

    neutron_l3_agent_2013_2_1.param(
        'interface_driver', type='string', default='',
        description="L3 requires that an interface driver be set. Choose the one that best matches your plugin.")

    neutron_l3_agent_2013_2_1.param(
        'interface_driver', type='string', default='neutron.agent.linux.interface.OVSInterfaceDriver',
        description="Example of interface_driver option for OVS based plugins (OVS, Ryu, NEC) that supports L3 agent")

    neutron_l3_agent_2013_2_1.param(
        'ovs_use_veth', type='string', default='False',
        description="Use veth for an OVS interface or not. Support kernels with limited namespace support (e.g. RHEL 6.5) so long as ovs_use_veth is set to True.")

    neutron_l3_agent_2013_2_1.param(
        'interface_driver', type='string', default='neutron.agent.linux.interface.BridgeInterfaceDriver', description="Example of interface_driver option for LinuxBridge")

    neutron_l3_agent_2013_2_1.param(
        'use_namespaces', type='string', default='True',
        description="Allow overlapping IP (Must have kernel build with CONFIG_NET_NS=y and iproute2 package that supports namespaces).")

    neutron_l3_agent_2013_2_1.param(
        'router_id', type='string', default='', description="This is done by setting the specific router_id.")

    neutron_l3_agent_2013_2_1.param(
        'gateway_external_network_id', type='string', default='',
        description="Each L3 agent can be associated with at most one external network.  This value should be set to the UUID of that external network.  If empty, the agent will enforce that only a single external networks exists and use that external network id")

    neutron_l3_agent_2013_2_1.param(
        'handle_internal_only_routers', type='string', default='True',
        description="Indicates that this L3 agent should also handle routers that do not have an external network gateway configured.  This option should be True only for a single agent in a Neutron deployment, and may be False for all agents if all routers must have an external network gateway")

    neutron_l3_agent_2013_2_1.param(
        'external_network_bridge', type='string', default='br-ex',
        description="Name of bridge used for external network traffic. This should be set to empty value for the linux bridge")

    neutron_l3_agent_2013_2_1.param(
        'metadata_port', type='string', default='9697', description="TCP Port used by Neutron metadata server")

    neutron_l3_agent_2013_2_1.param(
        'send_arp_for_ha', type='string', default='3',
        description="Send this many gratuitous ARPs for HA setup. Set it below or equal to 0 to disable this feature.")

    neutron_l3_agent_2013_2_1.param(
        'periodic_interval', type='string', default='40', description="seconds between re-sync routers' data if needed")

    neutron_l3_agent_2013_2_1.param(
        'periodic_fuzzy_delay', type='string', default='5',
        description="seconds to start to sync routers' data after starting agent")

    neutron_l3_agent_2013_2_1.param(
        'enable_metadata_proxy', type='string', default='True',
        description="enable_metadata_proxy, which is true by default, can be set to False if the Nova metadata server is not available")

    neutron_l3_agent_2013_2_1.param('metadata_proxy_socket', type='string',
                                    default='$state_path/metadata_proxy', description="Location of Metadata Proxy UNIX domain socket")
