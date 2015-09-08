===============================
FIWARE Policy Manager GE: Facts
===============================

| |Build Status| |Coverage Status| |Pypi Version| |Pypi License|

.. contents:: :local:

Introduction
============

This is the code repository for **FIWARE Policy Manager GE - Facts**, a server to process the incoming facts from the
`Orion Context Broker <https://github.com/telefonicaid/fiware-orion>`__
and publish the result into a RabbitMQ queue to be analysed by Fiware-Cloto. The facts are the result of the server
resources consumption.

This project is part of FIWARE_.
Check also the `FIWARE Catalogue entry for Policy Manager`__

__ `FIWARE Policy Manager - Catalogue`_


Any feedback on this documentation is highly welcome, including bugs, typos or
things you think should be included but aren't. You can use `github issues`__
to provide feedback.

__ `Fiware-facts - GitHub issues`_

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

GEi overall description
=======================
Bosun GEri is the reference implementation of Policy Manager GE.

Bosun GEri offers decision-making ability, independently of the type of resource (physical/virtual resources,
network, service, etc.)  being able to solve complex problems within the Cloud field by reasoning about the knowledge
base, represented by facts and rules.
Bosun GEri provides the basic management of cloud resources based on rules, as well as management of the corresponding
resources within FIWARE Cloud instances based on infrastructure physical monitoring, resources and services
security monitoring or whatever that could be defined by facts, actions and rules.

The baseline for the Bosun GEri is PyCLIPS, which is a module to interact with CLIPS expert system implemented in
python language. The reason to take PyCLIPS is to extend the OpenStack ecosystem with an expert system, written in
the same language as the rest of the OpenStack services.
Besides, It provides notification service to your own HTTP server where you can define your
own actions based on the notifications launched by Policy Manager.
Last but not least, Bosun is integrated with the Monitoring GEri in order to recover the information of the (virtual)
system and calculate any possible change on it based on the knowledge database defined for it.

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Components
----------

Fiware-Cloto
    Fiware-cloto is part of FIWARE Policy Manager. It provides an API-REST to create rules associated to servers,
    subscribe servers to Context Broker to get information about resources consumption of that servers and launch actions
    described in rules when conditions are given.

Fiware-Facts
    Server to process the incoming facts from the
    `Orion Context Broker <https://github.com/telefonicaid/fiware-orion>`__
    and publish the result into a RabbitMQ queue to be analysed by Fiware-Cloto. The facts are the result of the server
    resources consumption.

For more information, please refer to the `documentation <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/README.rst>`_.

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Build and Install
=================

Requirements
------------

- Operating systems: CentOS (RedHat) and Ubuntu (Debian), being CentOS 6.3 the
  reference operating system.

To install this module you have to install some components:

- Python 2.7
- Fiware-cloto module (https://github.com/telefonicaid/fiware-cloto)
- Redis 2.9.1 or above
- RabbitMQ Server 3.3.0 or above (http://www.rabbitmq.com/download.html)

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Installation
------------

**Using pip**
Install the component by executing the following instruction:
::

    pip install fiware-facts

This operation will install the component in your python site-packages folder.


`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Configuration file
------------------
The configuration used by the fiware-facts component is read from the file
``facts_conf/fiware-facts.cfg``

MYSQL cloto configuration must be filled before starting fiware-facts component, user and password are empty by default.
If you run the server without filling those values, the server will ask you to provide them.

Options that user could define:
::

    [common]
     brokerPort: 5000       # Port listening fiware-facts
     clotoPort:  8000       # Port listening fiware-cloto
     redisPort:  6379       # Port listening redis-server
     redisHost:  localhost  # Address of redis-server
     rabbitMQ:   localhost  # Address of RabbitMQ server
     cloto:      127.0.0.1  # Address of fiware-cloto

    [mysql]
     host: localhost        # address of mysql that fiware-cloto is using
     user:                  # mysql user
     password:              # mysql password

    [logger_root]
     level: INFO            # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Running
=======

Execute command:

::

    gunicorn facts.server:app


`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

API Overview
============

Servers will update their context. The context information contains the description of the CPU, Memory, Disk and
Network usages.

An example of this operation could be:

::

        curl --include \
             --request POST \
             --header "Content-Type: application/json" \
             --data-binary "{
            "contextResponses": [
                {
                    "contextElement": {
                       "attributes": [
                           {
                               "value": "0.12",
                               "name": "usedMemPct",
                               "type": "string"
                           },
                           {
                               "value": "0.14",
                               "name": "cpuLoadPct",
                               "type": "string"
                           },
                           {
                               "value": "0.856240",
                               "name": "freeSpacePct",
                               "type": "string"
                           },
                           {
                               "value": "0.8122",
                               "name": "netLoadPct",
                               "type": "string"
                           }
                       ],
                       "id": "Trento:193.205.211.69",
                       "isPattern": "false",
                       "type": "host"
                   },
                   "statusCode": {
                       "code": "200",
                       "reasonPhrase": "OK"
                   }
               }
            ]
        }" \
        'http://policymanager-host.org:5000/v1.0/d3fdddc6324c439780a6fd963a9fa148/servers/52415800-8b69-11e0-9b19-734f6af67565'

This message follows the NGSI-10 information model but using JSON format.


The response has no body and should return 200 OK.

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

API Reference Documentation
---------------------------

- `FIWARE Policy Manager v1 (Apiary)`__

__ `FIWARE Policy Manager - Apiary`_

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Testing
=======

Unit tests
----------

To execute the unit tests you must have a redis-server and a rabbitmq-server up and running.
Please take a look to the installation manual in order to configure those components.

After that, you can execute this folloing commands:

::
    $ pip install -r requirements_dev.txt
    $ export PYTHONPATH=$PWD
    $ nosetests -s -v --cover-package=facts --with-cover

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

End-to-end tests
----------------

Once you have fiware-facts running you can check the server executing:

::

    $ curl http://$HOST:5000/v1.0

Where:

**$HOST**: is the url/IP of the machine where fiware facts is installed, for example: (policymanager-host.org, 127.0.0.1, etc)

The request before should return a response with this body if everything is ok:

::

    {"fiware-facts":"Up and running..."}


Please refer to the `Installation and administration guide
<https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/admin_guide.rst#end-to-end-testing>`_ for details.

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Acceptance tests
----------------

Fiware-facts acceptance tests are included into fiware-cloto repository (https://github.com/telefonicaid/fiware-cloto).

Requirements

- Python 2.7 or newer
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)
- virtualenv installed (pip install virtalenv)
- Git installed (yum install git-core / apt-get install git)

Environment preparation:

- Create a virtual environment somewhere, e.g. in ENV (virtualenv ENV)
- Activate the virtual environment (source ENV/bin/activate)
- Change to the test/acceptance folder of the project
- Install the requirements for the acceptance tests in the virtual environment (pip install -r requirements.txt --allow-all-external).
- Configure file in fiware-cloto/tests/acceptance_tests/commons/configuration.py adding the keystone url, and a valid, user, password and tenant ID.

Tests execution

Change to the fiware-cloto/tests/acceptance_tests folder of the project if not already on it and execute:
::

     $ lettuce_tools -ft features/context_update.feature --tags=skip


In the following document you will find the steps to execute automated
tests for the Policy Manager GE:

- `Policy Manager acceptance tests <https://github.com/telefonicaid/fiware-cloto/tree/develop/cloto/tests/acceptance_tests/README.md>`_

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Advanced topics
===============

- `Installation and administration <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/admin_guide.rst>`_
- `User and programmers guide <https://github.com/telefonicaid/fiware-cloto/doc/tree/develop/doc/user_guide.rst>`_
- `Open RESTful API Specification <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/open_spec.rst>`_
- `Architecture Description <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/architecture.rst>`_

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

Support
=======

Ask your thorough programming questions using stackoverflow and your general questions on FIWARE Q&A.
In both cases please use the tag fiware-bosun

`Top`__.

__ `FIWARE Policy Manager GE: Facts`_

License
=======

\(c) 2014 Telefónica Investigación y Desarrollo S.A.U., Apache License 2.0

.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-facts.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-facts
.. |Coverage Status| image:: https://img.shields.io/coveralls/telefonicaid/fiware-facts/develop.svg
    :target: https://coveralls.io/r/telefonicaid/fiware-facts
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/
.. |Pypi License| image:: https://img.shields.io/pypi/l/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/


.. REFERENCES

.. _FIWARE: https://www.fiware.org/
.. _FIWARE Ops: https://www.fiware.org/fiware-operations/
.. _FIWARE Policy Manager - Apiary: https://jsapi.apiary.io/apis/policymanager/reference.html
.. _Fiware-facts - GitHub issues: https://github.com/telefonicaid/fiware-facts/issues/new
.. _FIWARE Policy Manager - Catalogue: http://catalogue.fiware.org/enablers/policy-manager-bosun
