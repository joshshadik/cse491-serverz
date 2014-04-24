from flask import Flask
import socket

app = Flask(__name__)

# app.config['SERVER_NAME'] = 'msu.edu:9512' 

from . import views, image 

def get_wsgi_app():
    return app.wsgi_app
