from rubick.schema import ConfigSchemaRegistry

neutron_openvswitch_agent = ConfigSchemaRegistry.register_schema(
    project='neutron_openvswitch_agent')

with neutron_openvswitch_agent.version('2013.2.1') as neutron_openvswitch_agent_2013_2_1:

    neutron_openvswitch_agent_2013_2_1.section('ml2')

    neutron_openvswitch_agent_2013_2_1.param(
        'type_drivers', type='string', default='local,flat,vlan,gre,vxlan')

    neutron_openvswitch_agent_2013_2_1.param(
        'tenant_network_types', type='string', default='local')

    neutron_openvswitch_agent_2013_2_1.param(
        'mechanism_drivers', type='string', default='',
        description="(ListOpt) Ordered list of networking mechanism driver entrypoints to be loaded from the neutron.ml2.mechanism_drivers namespace.")

    neutron_openvswitch_agent_2013_2_1.section('ml2_type_flat')

    neutron_openvswitch_agent_2013_2_1.param(
        'flat_networks', type='string', default='')

    neutron_openvswitch_agent_2013_2_1.section('ml2_type_vlan')

    neutron_openvswitch_agent_2013_2_1.param(
        'network_vlan_ranges', type='string', default='')

    neutron_openvswitch_agent_2013_2_1.section('ml2_type_gre')

    neutron_openvswitch_agent_2013_2_1.param(
        'tunnel_id_ranges', type='string', default='',
        description="(ListOpt) Comma-separated list of <tun_min>:<tun_max> tuples enumerating ranges of GRE tunnel IDs that are available for tenant network allocation")

    neutron_openvswitch_agent_2013_2_1.section('ml2_type_vxlan')

    neutron_openvswitch_agent_2013_2_1.param(
        'vni_ranges', type='string', default='')

    neutron_openvswitch_agent_2013_2_1.param(
        'vxlan_group', type='string', default='')
