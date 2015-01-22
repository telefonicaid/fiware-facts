__author__ = 'fla'

#!flask/bin/python
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask import Flask

app = Flask(__name__)

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(debug=True)
