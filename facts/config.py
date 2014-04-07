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
    'redisHost':    'localhost',            # host of Redis
    'redisQueue':   'policymanager',        # name of the queue in redis
    'rabbitMQ':     '130.206.81.71',        # IP of the RabbitMQ server
    'name':         'policymanager.facts',  # name of the server
    'logLevel':     'INFO',
    'logFormat':    '%(asctime)s %(levelname)s policymanager.facts %(message)s'
}

config = SafeConfigParser(cfg_defaults)

# Create the common section in the same way that we have in the configuration file: fiware-facts.cfg
config.add_section('common')

# Initialize the content of the config parameters
for key, value in cfg_defaults.items():
    config.set('common', key, str(value))
