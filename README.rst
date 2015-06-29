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
Version 1.0.0

* Initial release

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

