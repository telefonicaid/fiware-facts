# -*- coding: utf-8 -*-

Feature: Signal Stability for fact notifications.
  As a scalability manager user
  I want to have a temporal window
  in order to reset the grouping when the period between facts is higher than the configured one.


  @happy_path @skip @bug @CLAUDIA-5528
  Scenario: Facts grouping by window size is reset when the time between facts is higher than the configured one (10 seconds by default) (1/3).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    When  I wait "15" seconds
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5559
  Scenario: Facts grouping by window size is reset when the time between facts is higher than the configured one (10 seconds by default) (2/3).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    When  I wait "15" seconds
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.3        | 0.3        | 0.3          | 0.3        |
          | 0.5        | 0.5        | 0.5          | 0.5        |
    Then  no messages have been received by RabbitMQ consumer


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5559
  Scenario: Facts grouping by window size is reset when the time between facts is higher than the configured one (10 seconds by default) (3/3).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    When  I wait "15" seconds
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.3        | 0.3        | 0.3          | 0.3        |
    And   I wait "15" seconds
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.5        | 0.5        | 0.5          | 0.5        |
    Then  no messages have been received by RabbitMQ consumer
