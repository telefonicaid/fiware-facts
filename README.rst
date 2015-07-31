FIWARE Policy Manager GE - Facts
____________________

| |Build Status| |Coverage Status| |Pypi Version| |Pypi License|

Description
===========

This module is part of FIWARE Policy Manager.

Server to process the incoming facts from the `Orion Context Broker <http://catalogue.fi-ware.org/enablers/publishsubscribe-context-broker-orion-context-broker>`__.

Prerequisites
=============
To install this module you have to install some components:

- Python 2.7
- Fiware-cloto module (https://github.com/telefonicaid/fiware-cloto)
- Redis 2.9.1 or above
- gunicorn 19.1.1 or above

Installation
============
Download the component by executing the following instruction:

git clone git@github.com:telefonicaid/fiware-facts.git

Usage
=====

Execute command "gunicorn --check-config server.py" inside the folder where you downloaded fiware-facts

Changelog
=========

v1.5.0 (2015-07-28)
-------------------

Fix
~~~

- Fixing imprecision while parsing from string to a number. [Guillermo
  Jimenez Prieto]

- Updating build.sh file to build in jenkins. [Guillermo Jimenez Prieto]

- Fixing context value. NGSI parameter is called value in the latest
  release of NGSI. [Guillermo Jimenez Prieto]

- Context value parameter is called value in the last specification of
  NGSI. [Guillermo Jimenez Prieto]

v1.4.0 (2015-06-29)
-------------------

Fix
~~~

- Checking if window size is instance of integer or long. [Guillermo
  Jimenez Prieto]

- Fixing tests about getting windowsizes from cloto component.
  [Guillermo Jimenez Prieto]

- Fixing Facts component cannot access to the tenant Windowsize without
  a valid tenant token via API. [Guillermo Jimenez Prieto]

- Adding new variables to the configuration for the new windowsize
  retriving method. [Guillermo Jimenez Prieto]

- Checking that connection to rabbitMQ is open before close it.
  [Guillermo Jimenez Prieto]

- Fixing some bugs with the windowsize representation. [Guillermo
  Jimenez Prieto]

- Checking that there is a connection before close it. [Guillermo
  Jimenez Prieto]

v1.3.0 (2015-06-01)
-------------------

New
~~~

- Added Windows Size support for tenants. [Guillermo Jimenez Prieto]

Fix
~~~

- Updated Readme File with new installation information. [Guillermo
  Jimenez Prieto]

v1.2.0 (2015-04-01)
-------------------

New
~~~

- New: dev: preparing release @release. [Guillermo Jimenez Prieto]

Fix
~~~

- Fixing some magic numbers. [Guillermo Jimenez Prieto]

- Fixing coverage. [Guillermo Jimenez Prieto]

- Improving signal stability checking each fact with the previous one.
  [Guillermo Jimenez Prieto]

- Fixing a multitenacy bug. [Guillermo Jimenez Prieto]

- Fixing a multitenacy bug. [Guillermo Jimenez Prieto]

- Repaired multitenacy bug with serverid in lists. [Guillermo Jimenez
  Prieto]

v1.1.0 (2015-03-04)
-------------------

New
~~~

- New: dev: preparing release @release. [Guillermo Jimenez Prieto]

v1.0.0 (2015-02-24)
-------------------

New
~~~

- Building travis. [Guillermo Jimenez Prieto]

Fix
~~~

- Fixing an acceptance test and cobertura. [Guillermo Jimenez Prieto]

- Updating unittests and adding new data to build.sh in order to build
  in jenkins. [Guillermo Jimenez Prieto]

- Fixing multitenacy bug and gunicorn deployment. [Guillermo Jimenez
  Prieto]


License
=======

\(c) 2014 Telefónica Investigación y Desarrollo S.A.U., Apache License 2.0

.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-facts.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-facts
.. |Coverage Status| image:: https://coveralls.io/repos/telefonicaid/fiware-facts/badge.png?branch=develop
    :target: https://coveralls.io/r/telefonicaid/fiware-facts
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/
.. |Pypi License| image:: https://img.shields.io/pypi/l/fiware-facts.svg
   :target: https://pypi.python.org/pypi/fiware-facts/

