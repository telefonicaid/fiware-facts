# -*- coding: utf-8 -*-

Feature: Update window size.
  As a scalability manager user
  I want to configure a window size for grouping facts
  in order to keep a 'stable' values before sending them (processed) to Fiware-CLOTO


  @happy_path
  Scenario: FACTS does not send messages when only one context notification is received (default window size value is 2).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    Then  no messages have been received by RabbitMQ consumer


  @happy_path @skip @bug @CLAUDIA-5528
  Scenario: FACTS sends one message when two context notifications are received (default window size value is 2). (1/4).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5531
  Scenario: FACTS sends two messages when three context notifications are received (default window size value is 2) (2/4).
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 1.0        | 1.0        | 1.0          | 1.0        |
    Then  "2" notifications are sent to RabbitMQ
    And   the messages sent to RabbitMQ have got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |
          | qatest     | 0.8        | 0.8          | 0.8        | 0.8      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5531
  Scenario: FACTS sends three messages when four context notifications are received (default window size value is 2) (3/4)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 1.0        | 1.0        | 1.0          | 1.0        |
          | 1.0        | 1.0        | 1.0          | 1.0        |
    Then  "3" notifications are sent to RabbitMQ
    And   the messages sent to RabbitMQ have got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |
          | qatest     | 0.8        | 0.8          | 0.8        | 0.8      |
          | qatest     | 1.0        | 1.0          | 1.0        | 1.0      |


  @happy_path @skip @bug @CLAUDIA-5528 @CLAUDIA-5531 @CLAUDIA-5532
  Scenario: FACTS sends messages with different context attribute values (default window size value is 2)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.2        | 0.6        | 0.6          | 0.6        |
          | 1.0        | 0.6        | 1.0          | 1.0        |
          | 1.0        | 1.0        | 0.2          | 1.0        |
          | 0.0        | 0.0        | 0.0          | 1.0        |
    Then  "4" notifications are sent to RabbitMQ
    And   the messages sent to RabbitMQ have got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.2        | 0.4          | 0.4        | 0.4      |
          | qatest     | 0.8        | 0.6          | 0.8        | 0.8      |
          | qatest     | 1.0        | 1.0          | 0.7        | 1.0      |
          | qatest     | 0.5        | 0.5          | 0.5        | 1.0      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530 @CLAUDIA-5531 @CLAUDIA-5533
  Scenario: Window size is set set to 1.
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  window size is set to "1"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    Then  "3" notifications are sent to RabbitMQ
    And   the messages sent to RabbitMQ have got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.2        | 0.2          | 0.2        | 0.2      |
          | qatest     | 0.3        | 0.3          | 0.3        | 0.3      |
          | qatest     | 0.4        | 0.4          | 0.4        | 0.4      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530 @CLAUDIA-5531
  Scenario: Window size is set set to 5. No messages (facts) are processed.
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  window size is set to "5"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
          | 0.5        | 0.5        | 0.5          | 0.5        |
    Then  no messages have been received by RabbitMQ consumer


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530 @CLAUDIA-5531
  Scenario: Window size is set set to 6. One message (fact) is processed.
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  window size is set to "6"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.3        | 0.3        | 0.3          | 0.3        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
          | 0.5        | 0.5        | 0.5          | 0.5        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
          | 1.0        | 1.0        | 1.0          | 1.0        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.5        | 0.5          | 0.5        | 0.5      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530
  Scenario: Window size is changed while receiving facts (1/4) (default window size is 2)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   window size is set to "3"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.5        | 0.5        | 0.5          | 0.5        |
    Then  no messages have been received by RabbitMQ consumer


  @happy_path @skip @bug @CLAUDIA-5528 @CLAUDIA-5530
  Scenario: Window size is changed while receiving facts (2/4) (default window size is 2)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   window size is set to "3"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.5        | 0.5        | 0.5          | 0.5        |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.3        | 0.3          | 0.3        | 0.3      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530
  Scenario: Window size is changed while receiving facts (3/4) (default window size is 2)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3"
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   window size is set to "1"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.5        | 0.5        | 0.5          | 0.5        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.5        | 0.5          | 0.5        | 0.5      |


  @skip @bug @CLAUDIA-5528 @CLAUDIA-5530
  Scenario: Window size is changed while receiving facts (4/4) (default window size is 2)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    And   window size is set to "3"
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    And   window size is set to "2"
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.5        | 0.5          | 0.5        | 0.5      |


  @happy_path @skip @bug @CLAUDIA-5528
  Scenario: Different server IDs are managed separately. No messages are processed by FACTS (default window size) (1/3)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   the following notifications are received for "qatest2" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    Then  no messages have been received by RabbitMQ consumer

  @happy_path @skip @bug @CLAUDIA-5528
  Scenario: Different server IDs are managed separately. One message is processed for a server (default window size) (2/3)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   the following notifications are received for "qatest2" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.4        | 0.4        | 0.4          | 0.4        |
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 1.0        | 1.0        | 1.0          | 1.0        |
    Then  "1" notification is sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.6        | 0.6          | 0.6        | 0.6      |


  @skip @bug @CLAUDIA-5528
  Scenario: Different server IDs are managed separately. One message is processed for each server (default window size) (3/3)
    Given the configured tenant-id is registered in CLOTO component
    And   RabbitMQ consumer is looking into the configured message bus
    And   the context notification has default context elements
    When  the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.2        | 0.2        | 0.2          | 0.2        |
    And   the following notifications are received for "qatest2" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 0.4        | 0.4        | 0.4          | 0.4        |
          | 0.6        | 0.6        | 0.6          | 0.6        |
    And   the following notifications are received for "qatest" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | 1.0        | 1.0        | 1.0          | 1.0        |
    Then  "2" notifications are sent to RabbitMQ
    And   the message sent to RabbitMQ has got the following monitoring attributes:
          | serverId   | cpu        | mem          | hdd        | net      |
          | qatest     | 0.6        | 0.6          | 0.6        | 0.6      |
          | qatest2    | 0.5        | 0.5          | 0.5        | 0.5      |
