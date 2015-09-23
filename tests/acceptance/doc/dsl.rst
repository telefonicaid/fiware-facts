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

   >> the tenant-id registered in CLOTO component
   >> a no registered Tentand-Id in CLOTO component "(?P<tenant_id>.*)"

   >> the context notification has default context elements
   >> the context notification has these context elements

   >> RabbitMQ consumer is looking into the configured message bus

When clauses
------------

::

   >> I request the service info

   >> a context notification is received for "(?P<server_id>.*)" with values
   >> the following notifications are received for "(?P<server_id>.*)" with values

   >> window size is set to "(?P<window_size>.*)"

Then clauses
------------

::

   >> the context is updated
   >> the HTTP "(?P<status_code>.*)" is returned
   >> response contains "(.*)

   >> no messages have been received by RabbitMQ consumer
   >> "(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ
   >> "(?P<number_of_notifications>.*)" notification is sent to RabbitMQ
   >> the messages sent to RabbitMQ have got the following monitoring attributes
   >> the message sent to RabbitMQ has got the following monitoring attributes

