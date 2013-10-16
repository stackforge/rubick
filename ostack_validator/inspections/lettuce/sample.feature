Feature: Configuration consistency

  Scenario: Nova has proper Keystone host
    Given I use OpenStack 2013.1
    And Nova has "auth_strategy" equal to "keystone"
    And Keystone addresses are @X
    Then Nova should have "keystone_authtoken.auth_host" in "$X"

