PRODUCTION RULES ENGINE
=======================

This document describes rules engine used for inspection and diagnostics of
OpenStack configuration.

----------------
Proposal Summary
----------------

With this proposal we want to introduce a project aimed to enhance and simplify
operatinal maintenance of OpenStack cloud. Project provides service which uses
rule-based engine to inspect configurations of OpenStack
platform and find all kinds of architecture- and configuration-level glitches
and inconsistencies.

*# describe motivation behind rules
# describe rules reuse
# desribe rule-based inspection
# example rule
# mandatory rules vs. best-practice rules*

This engine will provide hints and best practices to increase reliability and
operational resilience of the cloud.

#FIXME: move this part to document rules_engine.rst

Rules-based approach to diagnostics
-----------------------------------

The consistent configuration across all components is essential to OpenStack
cloud operation. If something is wrong with configuration, you as an operator
will know this immidiately either from monitoring or clients complaining. But
diagnosing the exact problem is always a challenge, given the number of
components and configuration options per component.

You could think about troubleshooting OpenStack as going through some scenarios
which can be expressed as sets of rules. Your configuration must comply to all those
rules to be operational. On the other hand, if you know rules which your
configuration breaks, you can identify incorrect parameters reliably and easy.
That is how production rules or diagnostic systems work.

Example production rule for OpenStack system could be::

  if (condition)parameter) is (value) then (check_parameter_1) must be (value) and
      (check_parameter_2) must be (value)

