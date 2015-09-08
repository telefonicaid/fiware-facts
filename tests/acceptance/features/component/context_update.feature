# -*- coding: utf-8 -*-

Feature: Receive context update requests
  As a scalability manager user
  I want to receive data from the monitoring architecture through Context Broker notifications
  In order to manage facts, and group and send them to be processed.

  @basic
  Scenario Outline: Receive a context update notification with all parameters
    Given the tenant-id registered in CLOTO component
    When  a context notification is received for "<server_id>" with values:
          | cpuLoadPct | usedMemPct | freeSpacePct | netLoadPct |
          | <cpu>      | <memory>   | <disk>       | <network>  |
    Then the context is updated

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
