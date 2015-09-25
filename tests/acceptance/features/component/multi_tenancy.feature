# -*- coding: utf-8 -*-

Feature: Multi-Tenancy solution
  As a Policy Manager user
  I want to send context notifications subscribed by different Tenants
  in order to group and send them to Fiware-CLOTO without Tenant interferences.


  @happy_path @skip @bug @CLAUDIA-5528
  Scenario Outline: Facts are grouped separately between different Tenants. Message is sent only to a one of them (default window size)
    Given the main tenant-id configured is registered in CLOTO component
    And   the secondary tenant-id configured is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   a new secondary RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "<main_server_id>" and main tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    And   the following notifications are received for "<secondaty_server_id>" and secondary tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.7        | 0.7        | 0.7          | 0.7        |
    Then  "1" notification is sent to RabbitMQ with the main tenant
    And   no messages have been received by the secondary RabbitMQ consumer
    And   the message sent to RabbitMQ with the main tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |

    Examples:

          | main_server_id | secondaty_server_id |
          | qatest         | qatest              |
          | qatest         | qatest2             |


  @skip @bug @CLAUDIA-5528
  Scenario: Facts are grouped separately between different Tenants. Message is sent to both of them (default window size)
    Given the main tenant-id configured is registered in CLOTO component
    And   the secondary tenant-id configured is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   a new secondary RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" and main tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    And   the following notifications are received for "qatest2" and secondary tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.7        | 0.7        | 0.7          | 0.7        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
    Then  "2" notifications are sent to RabbitMQ with the main tenant
    And   "1" notification is sent to RabbitMQ with the secondary tenant
    And   the message sent to RabbitMQ with the main tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |
          | qatest     | 0.6        | 0.6          | 0.6        | 0.6      |
    And   the message sent to RabbitMQ with the secondary tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest2    | 0.5        | 0.5          | 0.5        | 0.5      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530
  Scenario: Facts are grouped separately between different Tenants. Message is sent to both of them (default window size)
    Given the main tenant-id configured is registered in CLOTO component
    And   the secondary tenant-id configured is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   a new secondary RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3" for the main tenant
    When  the following notifications are received for "qatest" and main tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    And   the following notifications are received for "qatest2" and secondary tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.7        | 0.7        | 0.7          | 0.7        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
    Then  "1" notifications are sent to RabbitMQ with the main tenant
    And   "1" notification is sent to RabbitMQ with the secondary tenant
    And   the message sent to RabbitMQ with the main tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |
    And   the message sent to RabbitMQ with the secondary tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest2    | 0.5        | 0.5          | 0.5        | 0.5      |


  @happy_path @skip @bug @CLAUDIA-5528 @CLAUDIA-5530 @test
  Scenario: Facts are grouped separately between different Tenants. Message is sent to both of them (default window size)
    Given the main tenant-id configured is registered in CLOTO component
    And   the secondary tenant-id configured is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   a new secondary RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3" for the main tenant
    And   window size is set to "4" for the secondary tenant
    When  the following notifications are received for "qatest" and main tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    And   the following notifications are received for "qatest2" and secondary tenant-id with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.7        | 0.7        | 0.7          | 0.7        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
    Then  "1" notifications are sent to RabbitMQ with the main tenant
    And   no messages have been received by the secondary RabbitMQ consumer
    And   the message sent to RabbitMQ with the main tenant has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |
