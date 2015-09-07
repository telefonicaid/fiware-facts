#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
from setuptools import setup, find_packages
from facts.server import __version__
setup(
  name='fiware-facts',
  packages=find_packages(exclude=['tests*']),
  install_requires=["redis==2.9.1",
  "Flask==0.10.1",
  "gevent==1.0.1",
  "pika==0.9.13",
  "python-dateutil==1.5",
  "gunicorn==19.1.1",
  "python-keystoneclient==1.3.0",
  "oslo.i18n==1.7.0",
  "MySQL-python==1.2.5"
  ],
  package_data = {
    'facts_conf': ['*.cfg']
  },
  version=__version__,
  description='Server to process the incoming facts from the Orion Context Broker',
  author='Fernando Lopez Aguilar, Guillermo Jimenez Prieto',
  author_email='fernando.lopezaguilar@telefonica.com, e.fiware.tid@telefonica.com',
  license='Apache 2.0',
  url='https://github.com/telefonicaid/fiware-facts',
  download_url='https://github.com/telefonicaid/fiware-facts/tarball/v%s' % __version__,
  keywords=['fiware', 'policy', 'manager', 'cloud'],
  classifiers=[
        "License :: OSI Approved :: Apache Software License", ],
)
