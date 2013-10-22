Production Rules Engine
=======================

This document describes rules engine used for inspection and diagnostics of
OpenStack configuration.

Summary
-------

The consistent configuration across all components is essential to OpenStack
cloud operation. If something is wrong with configuration, you as an operator
will know this immidiately either from monitoring or clients complaining. But
diagnosing the exact problem is always a challenge, given the number of
components and configuration options per component.

You could think about troubleshooting OpenStack as going through some scenarios
which can be expressed as sets of rules. Your configuration must comply to all 
those
rules to be operational. On the other hand, if you know rules which your
configuration breaks, you can identify incorrect parameters reliably and easy.
That is how production rules or diagnostic systems work.

Example production rule
-----------------------

Example production rule for OpenStack system would be::

  Given (condition_parameter_1) is (value) and
  (condition_parameter_2) is (value)
  then (check_parameter_1) must be (value)

Rule-based inspection
---------------------
All rule-based inspections are using pre-defined actions written on python, for 
now they defined in "steps.py" file in the directory: 
ostack_validator/inspections/lettuce. As you can see they are based on lettuce 
framework - bdd framework for python.
You can expand the rules definition by adding your own steps.py. As example:

#This decorator is for defining step for using them in the scenario.
@step(r'Nova has "(.+)" equal to "(.*)"')
def nova_has_property(step, name, value):
    name = subst(name)
        value = subst(value)

            for nova in [c for c in world.openstack.components if
            c.name.startswith('nova')]:
                    if not nova.config[name] == value:
                                stop()

New methods can use 2 classes from the inspections framework:
ostack_validator/model.py and ostack_validator/common.py. There are you can
find many adapters to the services configuration data and all additional
information collected from OpenStack nodes. After that you can use you brand
new rule in the scenarios as described above. In common.py you can find
Inspection, Issue, Mark, Error and Version classes for your comfortability in
rule defining. Model.py contains Openstack model based on configuration
schemas.

Store and reuse rules
---------------------
You can store your rules wherever you want and add it through the UI or simply 
putting it in directory ostack_validator/inspections/lettuce with name like 
this: *.feature. The main requirement is that all you actions in those files 
must be written according to the rules in steps.py.

Sanity checks vs best practices
-------------------------------
