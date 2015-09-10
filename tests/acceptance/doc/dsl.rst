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


When clauses
------------

::

   >> a context notification is received for "(?P<server_id>.*)" with values
   >> I request the service info

Then clauses
------------

::

   >> the context is updated
   >> I receive a HTTP "(\d*)" response code
   >> response contains "(.*)


