OPENSTACK DIAGNOSTICS PROPOSAL
==============================

Overview
--------

OpenStack cloud operators usually rely on deploymnet tools to configure all the
platform components correctly and efficiently upfront. However, after initial
deployment platform configurations and operational conditions start to change.
We propose a project that allows to analyze OpenStack architecture and diagnose
existing and potential problems using flexible set of rules.

Mission
---------

Diagnostics project mission is to **provide OpenStack cloud operators with
flexible way to inspect, analyze and diagnose architecture of the cloud and
configuration of components of the platform**.

User Stories
------------

As a **cloud operator**, I want to be able to automatically extract
configuration parameters from all OpenStack components to verify their
correctness, consistency and integrity.
As a **cloud architect**, I want to make sure that my OpenStack architecture and
configuration are compliant to 'best practices'.
As a **cloud operator**, I want automatic diagnostics tool which can tell me
what problems does my OpenStack architecture and/or configuration have or might
potentially have (e.g. at scale or if some component or node failed).
As a **cloud operator**, I want to be able to define rules used to inspect and
verify configuration of OpenStack components and store them to use for
verification of future configuration changes.

Requirements
------------

TBD

Scope
-----

As an MVP1, we create service that includes:

1. Rules engine with grammatic analysis capabilities
1. Extensible implementation of rules
1. REST API for running inspections
1. Storage back-end implementation for OpenStack platform architecture and
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
