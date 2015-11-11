.. _Top:
===============================
FIWARE Policy Manager GE: Facts
===============================

| |Build Status| |Coverage Status| |Pypi Version| |Pypi License| |StackOverflow|

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

Top_.


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

Top_.


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

Top_.


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
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)

Please, be sure you have installed mysql-devel package for development of MySQL applications.
You should be able to install it from yum or apt-get package managers.

Examples:

.. code::

    centos$ sudo yum install mysql-devel
    ubuntu$ sudo apt-get install mysql-devel

Top_.


Installation
------------

**Using pip**
Install the component by executing the following instruction:
::

    pip install fiware-facts

This operation will install the component in your python site-packages folder.


Top_.


Configuration file
------------------
The configuration used by the fiware-facts component is read from the configuration file.
This file is located here:

``/etc/fiware.d/fiware-facts.cfg``


MYSQL cloto configuration must be filled before starting fiware-facts component, user and password are empty by default.
You can copy the `default configuration file <facts_conf/fiware_facts.cfg>`_ to the folder defined for your OS, and
complete data about cloto MYSQL configuration (user and password).

In addition, user could have a copy of this file in other location and pass its location to the server in running
execution defining an environment variable called FACTS_SETTINGS_FILE.

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

Top_.


Running
=======

Execute command:

::

    gunicorn facts.server:app -b $IP:5000

Where $IP should be the IP assigned to the network interface that should be listening (ej. 192.168.1.33)

You can also execute the server with a different settings file providing an environment variable with the location
of the file:

::

    gunicorn facts.server:app -b $IP:5000 --env FACTS_SETTINGS_FILE=/home/user/fiware-facts.cfg

NOTE: if you want to see gunicorn log if something is going wrong, you could execute the command before adding
``--log-file=-`` at the end of the command. This option will show the logs in your prompt.


Finally, ensure that you create a folder for logs ``/var/log/fiware-facts/`` (by default), with the right permissions to write
in that folder.

::

    mkdir -m /var/log/fiware-facts

Top_.


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

Top_.


API Reference Documentation
---------------------------

- `FIWARE Policy Manager v1 (Apiary)`__

__ `FIWARE Policy Manager - Apiary`_

Top_.


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

Top_.


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

Top_.


Acceptance tests
----------------

All detailed documentation about acceptance tests can be consulted in `FACTS Acceptance Test Project <tests/acceptance>`_

**Requirements**

- `Python`_ or newer (2.x).
- `pip`_.
- `Virtualenv`_.
- `Fiware-Facts`_.

**Environment preparation**

1. Create a virtual environment somewhere::

      $> virtualenv $WORKON_HOME/venv

#. Activate the virtual environment::

      $> source $WORKON_HOME/venv/bin/activate)

#. Go to `$FACTS_HOME/tests/acceptance` folder in the project.
#. Install the requirements for the acceptance tests in the virtual environment::

      $> pip install -r requirements.txt --allow-all-external)

**Execution**

Execute the following command in the acceptance test project directory::

  $> cd $FACTS_HOME/tests/acceptance
  $> behave features/component --tags ~@skip

Before executing, you shoud configure properly the project settings file in `$FACTS_HOME/tests/acceptance/settings/settings.json`.
Take a look at the `FACTS Acceptance Test Project <tests/acceptance>`_ documentation.

Top_.


Advanced topics
===============

- `Installation and administration <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/admin_guide.rst>`_
- `User and programmers guide <https://github.com/telefonicaid/fiware-cloto/doc/tree/develop/doc/user_guide.rst>`_
- `Open RESTful API Specification <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/open_spec.rst>`_
- `Architecture Description <https://github.com/telefonicaid/fiware-cloto/tree/develop/doc/architecture.rst>`_

Top_.


Support
=======

Ask your thorough programming questions using `stackoverflow`_ and your general questions on `FIWARE Q&A`_.
In both cases please use the tag *fiware-bosun*.

Top_.


License
=======

\(c) 2014 Telefónica Investigación y Desarrollo S.A.U., Apache License 2.0

.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-facts.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-facts
   :alt Build status
.. |Coverage Status| image:: https://img.shields.io/coveralls/telefonicaid/fiware-facts/develop.svg
   :target: https://coveralls.io/r/telefonicaid/fiware-facts
   :alt Coverage status
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/
   :alt Version
.. |Pypi License| image:: https://img.shields.io/pypi/l/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/
   :alt License
.. |help stackoverflow| image:: http://b.repl.ca/v1/help-stackoverflow-orange.png
   :target: https://stackoverflow.com/questions/tagged/fiware-bosun
   :alt Help? Ask questions...

.. REFERENCES

.. _FIWARE: https://www.fiware.org/
.. _FIWARE Ops: https://www.fiware.org/fiware-operations/
.. _FIWARE Policy Manager - Apiary: https://jsapi.apiary.io/apis/policymanager/reference.html
.. _Fiware-facts - GitHub issues: https://github.com/telefonicaid/fiware-facts/issues/new
.. _FIWARE Policy Manager - Catalogue: http://catalogue.fiware.org/enablers/policy-manager-bosun
.. _Python: http://www.python.org/
.. _Behave: http://pythonhosted.org/behave/
.. _pip: https://pypi.python.org/pypi/pip
.. _Virtualenv: https://pypi.python.org/pypi/virtualenv
.. _Fiware-Facts: https://github.com/telefonicaid/fiware-facts
.. _stackoverflow: http://stackoverflow.com/questions/ask
.. _`FIWARE Q&A`: https://ask.fiware.org
