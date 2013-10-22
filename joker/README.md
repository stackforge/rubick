Joker
=====

Joker is a configuration data collector framework for OpenStack-based clouds.
This framework inspects hardware and software configuration of cloud components.
The results of this inspection are used to create Architecture Data Model which
could be exported and used by external services.

Installation and configuration
------------------------------

Usage and integration
---------------------

Architecture data model produced by Joker could be consumed by configuration
validator tool (Dark Knight), by architecture graph (Stencil) and others. 

At some point it should be made convertible into format accepted by deployment
systems (e.g. Fuel or TripleO) which will allow to effectively 'clone' OpenStack
clouds using different deployment applications.

This model could be reused by Rally project to compare benchmarking results for
different architectures.

The model can be used to inspect existing clouds for subsequent upgrade.

The model suits as base for questionaire to assess existing installations for
support contract pricing purposes.

Architecture Data Model
-----------------------

This section proposes data model which allows to describe any OpenStack
installation. The model includes data regarding physical infrastructure, logical
topology of services and mapping between the two.

Architecture data model could be serialized as JSON or YaML document of the
following format::

    openstack
        nodes
            node1
                -param1: value
                -param2: value
        services
            nova
                configuration
                    -param1: value
                    -param2: value
