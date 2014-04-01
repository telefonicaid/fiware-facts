__author__ = 'fla'

import redis
from package.mylist import mylist
from redis.exceptions import ConnectionError
from package.log import logger


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

            logger.error(message)

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
