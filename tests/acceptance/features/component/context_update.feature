# -*- coding: utf-8 -*-

Feature: Receive context update requests
  As a scalability manager user
  I want to receive data from the monitoring architecture through Context Broker notifications
  in order to manage facts, and group and send them to be processed.


  @happy_path
  Scenario Outline: Receive a context update notification with all context attributes.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has default context elements
    When  a context notification is received for "<server_id>" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | <cpu>      | <memory>   | <disk>       | <network>  |
    Then  the context is updated

    Examples:

      | server_id | cpu   | memory  | disk  | network |
      | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.00  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.0     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.0   | 0.15    |
      | qatest    | 0     | 0.8     | 0.1   | 0.0     |
      | qatest    | 0.75  | 0       | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0     | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.1   | 0       |
      | qatest    | 0.752 | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.857   | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.123 | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.1   | 0.151   |
      | qatest    | 0.75  | 0.8     | 0.1   | 1       |
      | qatest    | 0.75  | 0.8     | 1     | 0.151   |
      | qatest    | 0.75  | 1       | 0.1   | 0.151   |
      | qatest    | 1     | 0.8     | 0.1   | 0.151   |


  Scenario Outline: : Receive context with missing parameters. Notification must be processed.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has default context elements
    When  a context notification is received for "<server_id>" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | <cpu>      | <memory>   | <disk>       | <network>  |
    Then  I receive a HTTP "200" response code

    Examples:

      | server_id | cpu             | memory          | disk            | network           |
      | qatest    | [MISSING_PARAM] | 0.8             | 0.1             | 0.15              |
      | qatest    | 0.00            | [MISSING_PARAM] | 0.1             | 0.15              |
      | qatest    | 0.75            | 0.0             | [MISSING_PARAM] | 0.15              |
      | qatest    | 0.75            | 0.8             | 0.0             | [MISSING_PARAM]   |
      | qatest    | [MISSING_PARAM] | [MISSING_PARAM] | [MISSING_PARAM] | [MISSING_PARAM]   |
      | qatest    | [MISSING_PARAM] | 0               | [MISSING_PARAM] | 0.15              |


  Scenario: Receive context when subscription does not exist. Subscription must be processed.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has default context elements
    When  a context notification is received for "not_existing_server" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.73       | 030        | 0.1          | 0.15       |
    Then  I receive a HTTP "200" response code

  @test
  Scenario: Receive context when Tenant is not registered in CLOTO.
    Given a no registered Tentand-Id in CLOTO component "no_registered_tenant_id"
    And   the context notification has default context elements
    When  a context notification is received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.73       | 030        | 0.1          | 0.15       |
    Then  I receive a HTTP "404" response code


  Scenario Outline: Receive a context update notification with invalid context attribute values. Format.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has default context elements
    When  a context notification is received for "<server_id>" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | <cpu>      | <memory>   | <disk>       | <network>  |
    Then  I receive a HTTP "404" response code

    Examples:

      | server_id | cpu   | memory  | disk  | network |
      | qatest    | 0,05  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0,8     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0,1   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0.1   | 0,15    |
      | qatest    | hola  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05  | tel     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0.8     | qas   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0.1   | test    |
      | qatest    | 0. 05 | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0. 8    | 0.1   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0. 1  | 0.15    |
      | qatest    | 0.05  | 0.8     | 0.1   | 0. 15   |
      | qatest    | 0'05  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0'8     | 0.1   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0'1   | 0.15    |
      | qatest    | 0.05  | 0.8     | 0.1   | 0'15    |
      | qatest    |       | 0.8     | 0.1   | 0'15    |
      | qatest    | 0.05  |         | 0.1   | 0'15    |
      | qatest    | 0.05  | 0.8     |       | 0'15    |
      | qatest    | 0.05  | 0.8     | 0.1   |         |


  Scenario Outline: Receive a context update notification with invalid context attribute values. Value.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has default context elements
    When  a context notification is received for "<server_id>" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | <cpu>      | <memory>   | <disk>       | <network>  |
    Then  I receive a HTTP "400" response code

    Examples:

      | server_id | cpu    | memory  | disk  | network |
      | qatest    | 100.05 | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05   | 100.8   | 0.1   | 0.15    |
      | qatest    | 0.05   | 0.8     | 100.1 | 0.15    |
      | qatest    | 0.05   | 0.8     | 0.1   | 415.15  |
      | qatest    | -0.05  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.05   | -0.8    | 0.1   | 0.15    |
      | qatest    | 0.05   | 0.8     | -0.1  | 0.15    |
      | qatest    | 0.05   | 0.8     | 0.1   | -0.15   |


  Scenario Outline: Receive context notification with missing context elements.
    Given the configured tenant-id is registered in CLOTO component
    And   the context notification has these context elements:
          | id         | isPattern  | type         |
          | <id>       | <isPattern>| <type>       |
    When  a context notification is received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.73       | 030        | 0.1          | 0.15       |
    Then  I receive a HTTP "400" response code

    Examples:

          | id              | isPattern         | type            |
          | qatest          | [MISSING_PARAM]   | [MISSING_PARAM] |
          | [MISSING_PARAM] | false             | [MISSING_PARAM] |
          | [MISSING_PARAM] | [MISSING_PARAM]   | vm              |
          | [MISSING_PARAM] | [MISSING_PARAM]   | [MISSING_PARAM] |
          | qatest          | false             | [MISSING_PARAM] |
          | qatest          | [MISSING_PARAM]   | vm              |
          | [MISSING_PARAM] | false             | vm              |
