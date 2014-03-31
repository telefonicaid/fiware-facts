__author__ = 'fla'

from flask.ext.testing import LiveServerTestCase

from flask.ext.testing import TestCase
from flask import Flask
import urllib2

class MyTest(TestCase):
    def test_some_json(self):
        response = self.client.post("/v1.0/33/servers/44/")
        self.assertEquals(response.json, dict(success=True))
