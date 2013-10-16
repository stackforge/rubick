Feature: Configuration consistency

  Scenario: Nova has proper Keystone host
    Given I use OpenStack 2013.1
    And Nova has "auth_strategy" equal to "keystone"
    And Keystone addresses are @X
    Then Nova should have "keystone_authtoken.auth_host" in "$X"

  Scenario: Nova has proper fixed_range settings for Grizzly release
    Given I use OpenStack 2013.1
    And Nova has "fixed_range" equal to ""

  Scenario: Nova has proper settings for NoVNC
    Given I use OpenStack 2013.1
    And Controller addresses are @X
    Then Nova should have "novncproxy_base_url" in "$X"
