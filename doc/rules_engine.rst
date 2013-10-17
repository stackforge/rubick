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
which can be expressed as sets of rules. Your configuration must comply to all those
rules to be operational. On the other hand, if you know rules which your
configuration breaks, you can identify incorrect parameters reliably and easy.
That is how production rules or diagnostic systems work.

Example production rule
-----------------------

Example production rule for OpenStack system could be::

  Given (condition_parameter_1) is (value) and
  (condition_parameter_2) is (value)
  then (check_parameter_1) must be (value)

Rule-based inspection
---------------------

Store and reuse rules
---------------------

Sanity checks vs best practices
-------------------------------
