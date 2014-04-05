__author__ = 'fla'

from flask.ext.testing import TestCase
from flask import Flask
import urllib2
import json

class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def get_server_url(self):
        return 'http://127.0.0.1:5000/v1.0/33/servers/44'

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_some_json(self):
        """ Test that the POST operation over the API returns a error if
        content-type is not application/json.
        """
        #f = open('data.json', 'r')
        #json = f.read()

        data = {'ids': [12, 3, 4, 5, 6]}

        req = urllib2.Request(self.get_server_url())
        #req = urllib2.Request(self.get_server_url(), data='{"hola":"hola"}', headers={'Content-type': 'text/plain'})

        req.add_header('Content-Type', 'application/json')

        print req.get_method()

        print req.get_full_url()
        print req.data


        try:
            #req = urllib2.Request('http://www.example.com/', data="abc", headers={'Content-type': 'text/plain'})
            #response = urllib2.urlopen(req)
            response = urllib2.urlopen(req, json.dumps(data))

        except (ValueError), err:
            print "some error %s", err

        # response = urllib2.urlopen(self.get_server_url(), json)
        self.assertEquals(response.json, dict(success=True))
