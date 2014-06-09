Architecture Data Model
=======================

Overview
--------

We want to introduce unified data structure which contains all information
necessary to inspect, analyze, describe and visualize OpenStack architecture.

Architecture data model serves multiple actual and potential use cases.

Diagnostics
^^^^^^^^^^^

Architecture data model provides necessary data for the configuration analysis
and diagnostics tool (**Rubick**).

Deployment
^^^^^^^^^^

Arhictecture data model must include all information necessary to deployment
systems (e.g. **Fuel** or **TripleO**). We will implement simple conversion
tools which will allow to configure these deployment systems and effectively
support 'portable' clouds.

Benchmarking
^^^^^^^^^^^^

This model could be reused by **Rally** project to compare benchmarking
results for different architectures. Definitions of architectures must be
comparable and portable, which is exactly what architecture model aimed to
solve.

Upgrade
^^^^^^^

Upgrade system could potentially utilize the model just in the way the
Deployment systems do. In addition, existing clouds could be inspected and
described for subsequent upgrade using this model.

Tech Support
^^^^^^^^^^^^

The model suits as base for questionaire to assess existing installations for
support contract pricing purposes.

Hardening
^^^^^^^^^

The model could be used to perform automated/guided hardening of OpenStack
architecture and configuration. This is achieved through use of 'best practice'
rulesets for the inspection of cloud.

Expert system
^^^^^^^^^^^^^

The model could be used as a part of production/reactive rules system capable
of automated reporting and handling of operational errors, based on combination
of *base* status of the cloud, logging messages and notifications.

Data Format
-----------

This section proposes data model format which allows to describe an OpenStack
installation. The model includes data regarding physical infrastructure, logical
topology of services and mapping between the two.

Current model of OpenStack architecture used in Rubick is defined in module
``rubick/model.py``. This module contains following classes in hierarchy below:

  OpenStack:
    hosts:
      - Host: hostname1
        components:
          - Service: NovaApiComponent
            config:
              - key: value
              - ...
          - Service: KeystoneComponent
            config:
              - key: value
              - ...
          - ...
        filesystem:
          - resource1: FileResource
          - resource2: DirectoryResource
          - ...
      - Host: hostname2
        components:
          - ...
        filesystem:
          - ...
      - ...
