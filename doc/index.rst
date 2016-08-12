================================================
 Welcome to Bosun Policy Manager Server (Facts)
================================================

Introduction
============

Bosun is the reference implementation (GEri) of `FIWARE Policy Manager GE`_.
It comprises this Facts component to process the incoming "facts" (results
of server resources compsumption) from `Orion Context Broker`_ and publish
them into a RabbitMQ queue to be analysed by Cloto__ (the other component of
Bosun).

__ `FIWARE Cloto Documentation`_

Policy Manager provides the basic management of cloud resources based on rules,
as well as management of the corresponding resources within the FIWARE Cloud
instance like actions based on physical monitoring or infrastructure, security
monitoring of resources and services or whatever that could be defined by facts,
actions and rules. Policy Manager is a easy rule engine designed to be used in
the OpenStack ecosystem and, of course, inside the FIWARE Cloud.

IMPORTANT NOTE: This GE reference implementation product is only of interest
to potential FIWARE instance providers and therefore has been used to build
the basic FIWARE platform core infrastructure of FIWARE Lab. If you are an
application developer, you don't need to create a complete FIWARE instance
locally in order to start building applications based on FIWARE. You may rely
on instances of FIWARE GEris linked to the Data/Media Context Management, the
IoT Services Enablement and the Advanced Web-based User Interface chapters, or
some GEris of the Applications/Services Ecosystem and Delivery Framework chapter
(WireCloud) as well as the Security chapter (Access Control). Those instances
are either global instances or instances you can create on FIWARE Lab, but also
instances you may create by downloading, installing and configuring the
corresponding software in your own premises.

Bosun Policy Manager Server source code can be found here__.

__ `FIWARE Facts GitHub Repository`_


Documentation
=============

Please refer to GitHub's README__ for details about this component.

__ `FIWARE Facts GitHub README`_


.. title:: Home

.. toctree::
   :hidden:

   README <https://github.com/telefonicaid/fiware-facts/blob/master/README.rst>


.. REFERENCES

.. _FIWARE Policy Manager GE: https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/FIWARE.OpenSpecification.Cloud.PolicyManager
.. _FIWARE Facts GitHub Repository: https://github.com/telefonicaid/fiware-facts.git
.. _FIWARE Facts GitHub README: https://github.com/telefonicaid/fiware-facts/blob/master/README.rst
.. _FIWARE Cloto Documentation: http://catalogue.fiware.org/enablers/policy-manager-bosun/documentation
.. _Orion Context Broker: http://catalogue.fiware.org/enablers/publishsubscribe-context-broker-orion-context-broker
