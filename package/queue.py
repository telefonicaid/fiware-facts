__author__ = 'fla'

#import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
import datetime
import sys

# params 1) tenantId   2)serverId

class myqueue(object):
    #!/usr/bin/env python
    import pika

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='130.206.81.71'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange="update_" + sys.argv[1],
                             type='fanout')

    def publish_message(self, message):
        self.channel.basic_publish(exchange="update_" + sys.argv[1],
                          routing_key='',
                          body=message)
        print('Sent: %s' % message)
        self.connection.close()
