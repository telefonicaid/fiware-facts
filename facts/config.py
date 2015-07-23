# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
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

__author__ = 'fla'

from ConfigParser import SafeConfigParser
import os.path
import datetime


"""
Default configuration.

The configuration `cfg_defaults` can be superseded with that read from `cfg_filename`
(at path `../conf/<progname>.cfg`), if file exists.
"""

name = 'fiware-facts'
cfg_filename = os.path.join(os.path.dirname(__file__), '..', 'conf', '%s.cfg' % name)
cfg_defaults = {
    'brokerPort':   5000,                   # port of our facts broker
    'redisPort':    6379,                   # port of Redis
    'clotoPort':    8000,                   # port of fiware-cloto
    'clotoVersion': 'v1.0',                 # Cloto API version
    'redisHost':    'localhost',            # host of Redis
    'redisQueue':   'policymanager',        # name of the queue in redis
    'rabbitMQ':     'localhost',            # IP of the RabbitMQ server
    'cloto':        '127.0.0.1',            # IP of fiware-cloto component
    'clotoVersion': 'v1.0',                 # Cloto API version
    'name':         'policymanager.facts',  # name of the server
    'logLevel':     'INFO',
    'logFormat':    '%(asctime)s %(levelname)s policymanager.facts %(message)s'
}

cfg_mysql_defaults = {
    'host':   'localhost',                   # host of Cloto Mysql database
    'charset':    'utf8',                   # charset of the data base
    'user':    '',                   # user of cloto database
    'password': '',                 # password for the user
    'db':    'cloto',            # name of the cloto dataBase, default: cloto
}

config = SafeConfigParser(cfg_defaults)

# Create the common section in the same way that we have in the configuration file: fiware-facts.cfg
config.add_section('common')
config.add_section('mysql')

# Initialize the content of the config parameters
for key, value in cfg_defaults.items():
    config.set('common', key, str(value))

for key, value in cfg_mysql_defaults.items():
    config.set('mysql', key, str(value))

windowsize_facts = datetime.timedelta(seconds=10)

fact_attributes = ['serverId', 'CpuValue', 'MemValue', 'HddValue', 'NetValue', 'DataTime']

windowsize_attributes = ['tenantId', 'value']
