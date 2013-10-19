Design & Architecture
=====================

This section describes design and architecture of OpenStack Diagnostics (Rubik)
service.

Service includes the following components:

* **openstack.model** is an OpenStack architecture model representation. It is a
  common format used by components of the system to exchange configuration of
  the inspected environment
* **Rubick API** is a web service which implements APIs to rules, inspections
  and OpenStack architecture model
* **Rule engine** is a logic which performs inspections on the data model. Rule
  engine will have an interface to the ruleset store in future.
* **Config data store** is a storage for architecture models
* **Config data extractor** creates OpenStack model based on data collected from
  different sources, implemented as pluggable back-ends
* **Heat metadata plugin** extracts configration metadata from Heat stacks
  created by TripleO/Tuskar service
* **SSH metadata plugin** extracts configuration metadata from actual nodes of
  OpenStack cloud via secure SSH connection

.. image:: images/service_architecture.png
