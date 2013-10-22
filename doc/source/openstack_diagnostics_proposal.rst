==============================
OPENSTACK DIAGNOSTICS PROPOSAL
==============================

.. contents::

Project Name
============

**Official:** OpenStack Diagnostics

**Codename:** Rubick

OVERVIEW
========

The typical OpenStack cloud life cycle consists of 2 phases:

- initial deployment and
- operation maintenance

OpenStack cloud operators usually rely on deploymnet tools to configure all the
platform components correctly and efficiently in **initial deployment** phase.
Multiple OpenStack projects cover that area: TripleO/Tuskar, Fuel and Devstack,
to name a few.

However, once you installed and kicked off the cloud, platform configurations
and operational conditions begin to change. These changes could break
consistency and integration of cloud platform components. Keeping cloud up and
running is the essense of **operation maintenance** phase.

Cloud operator must quickly and efficiently identify and respond to the root
cause of such failures. To do so, he must check if his OpenStack configuration
is sane and consistent. These checks could be thought of as rules of diagnostic
system.

There are not many projects in OpenStack ecosystem aimed to increase reliability
and resilience of the cloud at the operation stage. With this proposal we want
to introduce a project which will help operators to diagnose their OpenStack
platform, reduce response time to known and unknown failures and effectively
support the desired SLA.

Mission
-------

Diagnostics' mission is to **provide OpenStack cloud operators with tools which
minimize time and effort needed to identify and fix errors in operations
maintenance phase of cloud life cycle.**

User Stories
-----------

- As a **cloud operator**, I want to make sure that my OpenStack architecture
  and configuration is sane and consistent across all platform components and
  services.
- As a **cloud architect**, I want to make sure that my OpenStack architecture
  and configuration are compliant to best practices.
- As a **cloud architect**, I need a knowledge base of sanity checks and best
  practices for troubleshooting my OpenStack cloud which I can reuse and update
  with my own checks and rules.
- As a **cloud operator**, I want to be able to automatically extract
  configuration parameters from all OpenStack components to verify their
  correctness, consistency and integrity.
- As a **cloud operator**, I want automatic diagnostics tool which can inspect
  configuration of my OpenStack cloud and report if it is sane and/or compliant
  toc community-defined best practices.
- As a **cloud operator**, I want to be able to define rules used to inspect
  and verify configuration of OpenStack components and store them to use for
  verification of future configuration changes.

Roadmap
-------

Proof of concept implementation - end October 2013. PoC implementation includes:

#. Open source code in stackforge repository
#. Standalone service with REST API v0.1
#. Simple SSH-based configuration data extraction
#. Rules engine with grammatic analysis
#. Basic healthcheck ruleset v0.1 with example rules of different types
#. Filesystem-based ruleset store

PoC scope does not include:

#. Basic integration with OpenStack Deployment program projects (Tuskar,
   TripleO)
#. Extraction of configuration data from Heat metadata
#. Extended ruleset with example best practices
#. Healthcheck ruleset v1.0
#. Ruleset store back-ends

Assumptions
-----------

We assume that we must reuse as much as possible from OpenStack Deployment
program in terms of platform configuration and architecture definitions (i.e.
TripleO Heat and configuration files templates).

DESIGN
======

.. include:: service_architecture.rst

.. include:: rules_engine.rst

.. include:: openstack_integration.rst

.. include:: openstack_architecture_model.rst
