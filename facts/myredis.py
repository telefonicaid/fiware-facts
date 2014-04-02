# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
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

import redis
from mylist import mylist
from redis.exceptions import ConnectionError
import logging


class myredis(object):
    """ class to create lists on redis distribution. it is asumed
    that there is an installed version of redis in the localhost
    in the port 6379 (by default) and the server executed (redis-server).
    """
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

        try:
            self.r.delete('policymanager')
        except ConnectionError:
            message = "[{}] Cannot delete the list. Possiblely redis is down".format("-")

            logging.error(message)

    def insert(self, data):
        ''' we need to check that data is a list and the exact number of
        element is equal to 4
        '''
        if isinstance(data, list) and len(data) == 4:
            self.r.rpush('policymanager', data)
            self.r.ltrim('policymanager', -5, -1)
        else:
            return "error"

    def range(self):
        return self.r.lrange('policymanager', -100, 100)

    def media(self, lista):
        if len(lista) >= 5:
            return self.sum(lista) / len(lista)
        else:
            result = mylist()
            result.data = []
            return result

    def sum(self, lista):
        if len(lista) > 1:
            return mylist.sum(lista)
        elif len(lista) == 1:
            r1 = mylist()
            r1.insert(lista)
            return r1
        else:
            return '[]'

    def delete(self):
        self.r.delete('policymanager')
