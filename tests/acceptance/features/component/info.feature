# -*- coding: utf-8 -*-

Feature: Get 'fiware-facts' service info
  As a scalability manager user
  I want to check if fiware-facts is Up&Running
  So that I can use the service


  Scenario: Get info from Fiware-Facts service.
    Given the fiware-facts service properly deployed
    When  I request the service info
    Then  I receive a HTTP "200" response code
    And   and response contains "Up and running..."
