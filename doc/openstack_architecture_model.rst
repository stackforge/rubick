Architecture Data Model
=======================

Overview
--------

We want to introduce unified data structure which contains all information
necessary to inspect, analyze, describe and visualize OpenStack architecture.

This Architecture data model could be consumed and processed by configuration
analysis and diagnostics tool (**Rubick**).

Arhictecture data model must include all information necessary to deployment
systems (e.g. **Fuel** or **TripleO**). We will implement simple conversion
tools which will allow to configure these deployment systems and effectively
support 'portable' clouds.

This model could be reused by Rally project to compare benchmarking results for
different architectures.

The model can be used to inspect existing clouds for subsequent upgrade.

The model suits as base for questionaire to assess existing installations for
support contract pricing purposes.

The model could be used to perform automated/guided hardening of OpenStack
architecture and configuration.

Data Format
-----------

This section proposes data model format which allows to describe an OpenStack
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
