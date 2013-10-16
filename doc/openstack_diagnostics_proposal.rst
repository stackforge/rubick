OPENSTACK DIAGNOSTICS PROPOSAL
==============================

Project Name
------------

**Official:** OpenStack Diagnostics

**Codename:** Rubick

Overview
--------

OpenStack cloud operators usually rely on deploymnet tools to configure all the
platform components correctly and efficiently upfront. However, after initial
deployment platform configurations and operational conditions start to change.
These changes could break consistency and integration of cloud platform and its
components.

Mission
---------

Diagnostics' mission is to **provide OpenStack cloud operators with tools which
minimize time and effort needed to identify and fix errors in operations
maintenance phase of cloud life cycle.**

User Stories
------------

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

Requirements
------------

TBD

Scope
-----

As an MVP1, we create a service that includes:

#. Rules engine with grammatic analysis capabilities
#. Extensible implementation of rules
#. REST API for running inspections
#. Storage back-end implementation for OpenStack platform architecture and
   configuration data

Assumptions
-----------

We assume that we must reuse as much as possible from OpenStack Deployment
program in terms of platform configuration and architecture definitions (i.e.
TripleO Heat and configuration files templates).

Dependencies
------------

Design
------
