from flask import Flask

app = Flask(__name__)

from . import views, image 



def get_wsgi_app():
    return app.wsgi_app
