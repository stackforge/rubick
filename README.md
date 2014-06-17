# Rubick

Rubick is a tool to analyze OpenStack installation for possible problems. It is
a library that provides a representation of the OpenStack configuration and
inspection/validation/analysis actions on that representation.

## Config representation

The first step to create representation of OpenStack architecture and
configuration is a collection of data from an installation of the platform.
There are several ways to collect those data, including automated discovery from
different sources. The most simple way is to parse pre-populated directory
structure that contain configuration files of OpenStack services from different
nodes in a cluster.

With more complicated discovery engines, it is possible that those files are
collected automatically via SSH based on inspection of process list at every
node listed in hypervisor inventory of OpenStack Compute service, and even more
complicated scenarios. However, that is a scope of specialized discovery service
which Rubick is not at the moment.

The next step is to organize all the colleced data into single data structure,
called OpenStack configration model. This is an object model that includes
physical nodes of the cluster, OpenStack services and their instances,
configuration parameters, etc. See detailed description of the proposed model in
the documentation.

## Config analysis

Once the OpenStack configuration model is created, it could be used to validate
the correctness of static OpenStack settings, as well as the dynamic state of
OpenStack cluster.
