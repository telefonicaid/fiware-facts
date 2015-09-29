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
__version__ = '1.8.0'

from ConfigParser import SafeConfigParser
from sys import platform as _platform
import platform
import os.path
import datetime


"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/fiware-facts.cfg

Optionally, user can specify the file location manually using an Environment variable called FACTS_SETTINGS_FILE.
"""

name = 'fiware-facts'

cfg_dir = "/etc/fiware.d"

if os.environ.get("FACTS_SETTINGS_FILE"):
    cfg_filename = os.environ.get("FACTS_SETTINGS_FILE")

else:
    cfg_filename = os.path.join(cfg_dir, '%s.cfg' % name)

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

cfg_loggers_defaults = {
    'keys':   'root'
}

cfg_handlers_defaults = {
    'keys':   'console, file'
}

cfg_formatters_defaults = {
    'keys':   'standard',
}

cfg_formatter_standard_defaults = {
    'class':   'logging.Formatter',
    'format':    '%(asctime)s %(levelname)s policymanager.facts %(message)s',
}

cfg_logger_root_defaults = {
    'level':   'INFO',
    'handlers':    'console, file'
}

cfg_handler_console_defaults = {
    'level':   'DEBUG',
    'class':    'StreamHandler',
    'formatter':    'standard',
    'args': '(sys.stdout,)',
}

cfg_handler_file_defaults = {
    'level':   'DEBUG',
    'class':    'handlers.RotatingFileHandler',
    'formatter':    'standard',
    'logFilePath':    '/var/log/fiware-facts',
    'logFileName':    'fiware-facts.log',
    'logMaxFiles':    3,
    'logMaxSize':    '5*1024*1024  ; 5 MB',
    'args': "('%(logFilePath)s/%(logFileName)s', 'a', %(logMaxSize)s, %(logMaxFiles)s)",
}

config = SafeConfigParser(cfg_defaults)

# Create the common section in the same way that we have in the configuration file: fiware-facts.cfg
config.add_section('common')
config.add_section('mysql')
config.add_section('loggers')
config.add_section('handlers')
config.add_section('formatters')
config.add_section('formatter_standard')
config.add_section('logger_root')
config.add_section('handler_console')
config.add_section('handler_file')


# Initialize the content of the config parameters
for key, value in cfg_defaults.items():
    config.set('common', key, str(value))

for key, value in cfg_mysql_defaults.items():
    config.set('mysql', key, str(value))

for key, value in cfg_loggers_defaults.items():
    config.set('loggers', key, str(value))

for key, value in cfg_handlers_defaults.items():
    config.set('handlers', key, str(value))

for key, value in cfg_formatters_defaults.items():
    config.set('formatters', key, str(value))

for key, value in cfg_formatter_standard_defaults.items():
    config.set('formatter_standard', key, str(value))

for key, value in cfg_logger_root_defaults.items():
    config.set('logger_root', key, str(value))

for key, value in cfg_handler_console_defaults.items():
    config.set('handler_console', key, str(value))

for key, value in cfg_handler_file_defaults.items():
    config.set('handler_file', key, str(value))

config.set('common', 'cfg_file_path', str(cfg_filename))

windowsize_facts = datetime.timedelta(seconds=10)

fact_attributes = ['serverId', 'CpuValue', 'MemValue', 'HddValue', 'NetValue', 'DataTime']

windowsize_attributes = ['tenantId', 'value']
