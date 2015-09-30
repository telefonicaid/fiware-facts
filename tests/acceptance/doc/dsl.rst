========================================
FIWARE | FACTS | Acceptance test project
========================================

This page describes the DSL implemented for building features (step catalog).
All available steps can be used as part of following test elements:

- Given
- When
- Then
- And
- But

Although all steps can be used as part of any group above, in next sections we have grouped them by the typical test
element you are going to use with them.


Component testing DSL
=====================

Given clauses
-------------

::

    >> the fiware-facts service properly deployed

    >> the configured tenant-id is registered in CLOTO component
    >> the main tenant-id configured is registered in CLOTO component
    >> the secondary tenant-id configured is registered in CLOTO component

    >> a no registered Tentand-Id in CLOTO component "(?P<tenant_id>.*)"

    >> the context notification has default context elements
    >> the context notification has these context elements

    >> RabbitMQ consumer is looking into the configured message bus
    >> a new secondary RabbitMQ consumer is looking into the configured message bus


When clauses
------------

::

    >> I request the service info

    >> a context notification is received for "(?P<server_id>.*)" with values
    >> a context notification is received for "(?P<server_id>.*)" and main tenant-id with values
    >> a context notification is received for "(?P<server_id>.*)" and secondary tenant-id with values

    >> the following notifications are received for "(?P<server_id>.*)" with values
    >> the following notifications are received for "(?P<server_id>.*)" and main tenant-id with values
    >> the following notifications are received for "(?P<server_id>.*)" and secondary tenant-id with values

    >> window size is set to "(?P<window_size>.*)"
    >> window size is set to "(?P<window_size>.*)" for the main tenant
    >> window size is set to "(?P<window_size>.*)" for the secondary tenant

    >> I wait "(?P<seconds>\d*)" seconds

Then clauses
------------

::

    >> the context is updated

    >> I receive a HTTP "(?P<status_code>.*)" response code
    >> response contains "(.*)

    >> "(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ
    >> "(?P<number_of_notifications>.*)" notification is sent to RabbitMQ
    >> "(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ with the main tenant
    >> "(?P<number_of_notifications>.*)" notification is sent to RabbitMQ with the main tenant
    >> "(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ with the secondary tenant
    >> "(?P<number_of_notifications>.*)" notification is sent to RabbitMQ with the secondary tenant

    >> the messages sent to RabbitMQ have got the following monitoring attributes
    >> the messages sent to RabbitMQ with the main tenant have got the following monitoring attributes
    >> the messages sent to RabbitMQ with the secondary tenant have got the following monitoring attributes
    >> the message sent to RabbitMQ has got the following monitoring attributes
    >> the message sent to RabbitMQ with the main tenant has got the following monitoring attributes
    >> the message sent to RabbitMQ with the secondary tenant has got the following monitoring attributes

    >> no messages have been received by RabbitMQ consumer
    >> no messages have been received by the main RabbitMQ consumer
    >> no messages have been received by the secondary RabbitMQ consumer
