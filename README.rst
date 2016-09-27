.. _Top:

===============================
FIWARE Policy Manager GE: Facts
===============================

|License Badge| |Documentation Badge| |StackOverflow| |Build Status| |Coverage Status| |Docker badge| |Pypi Version|

.. contents:: :local:

Introduction
============

This is the code repository for **FIWARE Policy Manager GE - Facts**, a server
to process the incoming facts from the `Orion Context Broker`_ and publish the
result into a RabbitMQ queue to be analysed by Fiware-Cloto. The facts are the
result of the server resources consumption.

This project is part of FIWARE_.
Check also the `FIWARE Catalogue entry for Policy Manager`__

__ `FIWARE Policy Manager - Catalogue`_

Any feedback on this documentation is highly welcome, including bugs, typos or
things you think should be included but aren't. You can use `github issues`__
to provide feedback.

__ `FIWARE Facts - GitHub issues`_

Top_.


GEi overall description
=======================

Bosun GEri is the reference implementation of Policy Manager GE.

Bosun offers decision-making ability, independently of the type of resource
(physical/virtual resources, network, service, etc.) being able to solve
complex problems within the Cloud field by reasoning about the knowledge
base, represented by facts and rules. Bosun GEri provides the basic management
of cloud resources based on rules, as well as management of the corresponding
resources within FIWARE Cloud instances based on infrastructure physical
monitoring, resources and services security monitoring or whatever that
could be defined by facts, actions and rules.

The baseline for the Bosun GEri is PyCLIPS, which is a module to interact with
CLIPS expert system implemented in Python language. The reason to take PyCLIPS
is to extend the OpenStack ecosystem with an expert system, written in the same
language as the rest of the OpenStack services. Besides, It provides
notification service to your own HTTP server where you can define your
own actions based on the notifications launched by Policy Manager.
Last but not least, Bosun is integrated with the Monitoring GEri in order
to recover the information of the (virtual) system and calculate any possible
change on it based on the knowledge database defined for it.

Top_.


Components
----------

Fiware-Cloto
    Fiware-Cloto is part of FIWARE Policy Manager. It provides a REST API to
    create rules associated to servers, subscribe servers to Context Broker to
    get information about resources consumption of that servers and launch
    actions described in rules when conditions are met.

Fiware-Facts
    Server to process the incoming facts from `Orion Context Broker`_ and
    publish the result into a RabbitMQ queue to be analysed by Fiware-Cloto.
    The facts are the result of the server resources consumption.

For more information, please refer to the documentation__

__ `FIWARE Cloto - README`_


Top_.


Build and Install
=================

Requirements
------------

- Operating systems: CentOS (RedHat) and Ubuntu (Debian), being CentOS 6.3 the
  reference operating system.

To install this module you have to install some components:

- Python 2.7
- Fiware-Cloto module (https://github.com/telefonicaid/fiware-cloto)
- Redis 2.9.1 or above
- RabbitMQ Server 3.3.0 or above (http://www.rabbitmq.com/download.html)
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)


Please, be sure you have installed mysql-devel package for development of MySQL
applications. You should be able to install it from yum or apt-get package
managers.

Examples:

.. code::

    centos$ sudo yum install mysql-devel
    ubuntu$ sudo apt-get install mysql-devel

Top_.



Installation
------------

**Using pip**
Install the component by executing the following instruction:

.. code::

    $ sudo pip install fiware-facts

This operation will install the component in your python site-packages folder.

Top_.


Configuration file
------------------

The configuration used by the fiware-facts component is read from the file
located at ``/etc/fiware.d/fiware-facts.cfg``.

MySQL cloto configuration must be filled before starting fiware-facts component,
user and password are empty by default. You can copy the `default configuration
file <facts_conf/fiware_facts.cfg>`_ to the folder defined for your OS, and
complete data about Cloto MySQL configuration (user and password).

In addition, user could have a copy of this file in other location and pass its
location to the server in running execution defining an environment variable
called FACTS_SETTINGS_FILE.

Options that user could define:

::

   [common]
   brokerPort: 5000       # Port listening fiware-facts
   clotoPort:  8000       # Port listening fiware-cloto
   redisPort:  6379       # Port listening redis-server
   redisHost:  localhost  # Address of redis-server
   redisQueue: policymanager
   rabbitMQ:   localhost  # Address of RabbitMQ server
   cloto:      127.0.0.1  # Address of fiware-cloto
   clotoVersion: v1.0
   name:       policymanager.facts
   maxTimeWindowsize: 10

   [mysql]
   host: localhost        # address of mysql that fiware-cloto is using
   charset:    utf8
   db: cloto
   user:                  # mysql user
   password:              # mysql password

   [loggers]
   keys: root

   [handlers]
   keys: console, file

   [formatters]
   keys: standard

   [formatter_standard]
   class: logging.Formatter
   format: %(asctime)s %(levelname)s policymanager.facts %(message)s

   [logger_root]
   level: INFO            # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   handlers: console, file

   [handler_console]
   level: DEBUG
   class: StreamHandler
   formatter: standard
   args: (sys.stdout,)

   [handler_file]
   level: DEBUG
   class: handlers.RotatingFileHandler
   formatter: standard
   logFilePath: /var/log/fiware-facts
   logFileName: fiware-facts.log
   logMaxFiles: 3
   logMaxSize: 5*1024*1024  ; 5 MB
   args: ('%(logFilePath)s/%(logFileName)s', 'a', %(logMaxSize)s, %(logMaxFiles)s)


Top_.


Running
=======

Execute command:

.. code::

    $ gunicorn facts.server:app -b $IP:5000

Where $IP should be the IP assigned to the network interface that should be
listening (ej. 192.168.1.33)

You can also execute the server with a different settings file providing an
environment variable with the location of the file:

.. code::

    $ gunicorn facts.server:app -b $IP:5000 --env FACTS_SETTINGS_FILE=/home/user/fiware-facts.cfg

NOTE: if you want to see gunicorn log if something is going wrong, you could
execute the command before adding ``--log-file=-`` at the end of the command.
This option will show the logs in your prompt.

Finally, ensure that you create a folder for logs ``/var/log/fiware-facts/``
(by default), with the right permissions to write in that folder.

.. code::

    $ sudo mkdir -p /var/log/fiware-facts


Running with supervisor
-----------------------

Optionally you can add a new layer to manage gunicorn process with a supervisor.
Just install supervisor on your system:

.. code::

    $ sudo apt-get install supervisor

Copy the file ``utils/facts_start`` to ``/etc/fiware.d``.
Make this script executable:

.. code::

    $ sudo chmod a+x /etc/fiware.d/facts_start

Copy the file ``utils/fiware-facts.conf`` to ``/etc/supervisor/conf.d``.

Start fiware-facts using supervisor:

.. code::

    $ sudo supervisorctl reread
    $ sudo supervisorctl update
    $ sudo supervisorctl start fiware-facts

To stop fiware-facts just execute:

.. code::

    $ sudo supervisorctl stop fiware-facts

NOTE: Supervisor provides an “event listener” to subscribe to
“event notifications”. The purpose of the event notification/subscription
system is to provide a mechanism for arbitrary code to be run (e.g. send an
email, make an HTTP request, etc) when some condition is satisfied. That
condition usually has to do with subprocess state. For instance, you may
want to notify someone via email when a process crashes and is restarted
by Supervisor. For more information check also the `Supervisor Documentation`_.

Top_.


API Overview
============

Servers will update their context. The context information contains the
description of the CPU, Memory, Disk and Network usages.

An example of this operation could be:

.. code::

      $ curl --include \
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

To execute the unit tests you must have a redis-server and a rabbitmq-server up
and running. Please take a look to the installation manual in order to configure
those components.

After that, you can execute this folloing commands:

.. code::

    $ pip install -r requirements_dev.txt
    $ export PYTHONPATH=$PWD
    $ nosetests -s -v --cover-package=facts --with-cover


Top_.


End-to-end tests
----------------

Once you have fiware-facts running you can check the server executing:

.. code::

    $ curl http://$HOST:5000/v1.0

Where:

**$HOST**: is the url/IP of the machine where fiware facts is installed, for
example: (policymanager-host.org, 127.0.0.1, etc)

The request before should return a response with this body if everything is ok:

::

    {"fiware-facts":"Up and running..."}



Please refer to the `Installation and administration guide`__ for details.

__ `FIWARE Cloto - E2E tests`_

Top_.



Acceptance tests
----------------

All detailed documentation about acceptance tests can be consulted in
`FACTS Acceptance Test Project <tests/acceptance>`_

**Requirements**

- `Python`_ or newer (2.x).
- `pip`_.
- `Virtualenv`_.
- `FIWARE Facts`_.

**Environment preparation**

1. Create a virtual environment somewhere::

      $ virtualenv $WORKON_HOME/venv

#. Activate the virtual environment::



      $ source $WORKON_HOME/venv/bin/activate)



#. Go to `$FACTS_HOME/tests/acceptance` folder in the project.
#. Install the requirements for the acceptance tests in the virtual environment::

      $ pip install -r requirements.txt --allow-all-external)

**Execution**

Execute the following command in the acceptance test project directory::

      $ cd $FACTS_HOME/tests/acceptance
      $ behave features/component --tags ~@skip

Before executing, you shoud configure properly the project settings file in
``$FACTS_HOME/tests/acceptance/settings/settings.json``. Take a look at the
`FACTS Acceptance Test Project <tests/acceptance>`_ documentation.

Top_.


Advanced topics
===============

- `Installation and administration <https://github.com/telefonicaid/fiware-cloto/tree/master/doc/admin_guide.rst>`_
- `User and programmers guide <https://github.com/telefonicaid/fiware-cloto/doc/tree/master/doc/user_guide.rst>`_
- `Open RESTful API Specification <https://github.com/telefonicaid/fiware-cloto/tree/master/doc/open_spec.rst>`_
- `Architecture Description <https://github.com/telefonicaid/fiware-cloto/tree/master/doc/architecture.rst>`_

Top_.


Support
=======

Ask your thorough programming questions using stackoverflow_ and your general
questions on `FIWARE Q&A`_. In both cases please use the tag *fiware-bosun*.

Top_.


License
=======

\(c) 2014-2016 Telefónica Investigación y Desarrollo S.A.U., Apache License 2.0

.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-facts.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-facts
   :alt: Build status
.. |Coverage Status| image:: https://img.shields.io/coveralls/telefonicaid/fiware-facts/develop.svg
   :target: https://coveralls.io/r/telefonicaid/fiware-facts
   :alt: Coverage status
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/
   :alt: Version
.. |License Badge| image:: https://img.shields.io/badge/license-Apache_2.0-blue.svg
   :target: LICENSE.txt
   :alt: License
.. |StackOverflow| image:: https://img.shields.io/badge/support-sof-yellowgreen.svg
   :target: https://stackoverflow.com/questions/tagged/fiware-bosun
   :alt: Help? Ask questions...
.. |Documentation Badge| image:: https://readthedocs.org/projects/fiware-cloto/badge/?version=latest
   :target: http://fiware-cloto.readthedocs.org/en/latest/?badge=latest
.. |Docker badge| image:: https://img.shields.io/docker/pulls/fiware/bosun-facts.svg
   :target: https://hub.docker.com/r/fiware/bosun-facts
   :alt: Docker Pulls

.. REFERENCES

.. _FIWARE: https://www.fiware.org/
.. _FIWARE Q&A: https://ask.fiware.org
.. _FIWARE Ops: https://www.fiware.org/fiware-operations/
.. _FIWARE Policy Manager - Apiary: https://jsapi.apiary.io/apis/policymanager/reference.html
.. _FIWARE Facts: https://github.com/telefonicaid/fiware-facts
.. _FIWARE Facts - GitHub issues: https://github.com/telefonicaid/fiware-facts/issues/new
.. _FIWARE Cloto - README: https://github.com/telefonicaid/fiware-cloto/tree/master/doc/index.rst
.. _FIWARE Cloto - E2E tests: https://github.com/telefonicaid/fiware-cloto/tree/master/doc/admin_guide.rst#end-to-end-testing
.. _FIWARE Policy Manager - Catalogue: http://catalogue.fiware.org/enablers/policy-manager-bosun
.. _Orion Context Broker: http://catalogue.fiware.org/enablers/publishsubscribe-context-broker-orion-context-broker
.. _Python: http://www.python.org/
.. _Behave: http://pythonhosted.org/behave/
.. _pip: https://pypi.python.org/pypi/pip
.. _Virtualenv: https://pypi.python.org/pypi/virtualenv
.. _stackoverflow: http://stackoverflow.com/questions/ask
.. _Supervisor Documentation: http://supervisord.org/events.html
