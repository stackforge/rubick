= VALIDATOR INTEGRATION WITH OPENSTACK

== Overview

== Integration Points

=== TripleO integration points

::

package "Metadata services" {
        [Heat]
            [CFN]
                [EC2]
}

frame "TripleO" {
        package "diskimage-builder" {
                    [tripleo-image-elements] -- nova.conf
                            [tripleo-image-elements] -- keystone.conf
                                    [tripleo-image-elements] -- glance.conf
                                        }
                                            [os-collect-config] <-- [Heat]
                                                [os-collect-config] <-- [CFN]
                                                    [os-collect-config] <--
                                                    [EC2]
                                                        [os-collect-config]
                                                        -left-> JSON
                                                            JSON -->
                                                            [os-refresh-config]
}

frame "Tuskar" {
        [Tuskar] -right- Tuskar_API
}

[Tuskar] --> HOT
HOT --> [Heat]

cloud {
        [Config Validator] << DarkKnight >>
}

JSON -up-> [Config Validator]
[tripleo-image-elements] -up-> [Config Validator]
