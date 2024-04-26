"""
James Butcher
4/18/24
"""
from flask import Flask
from .views import views
from .kb_graph import load_graph
import os

def create_app():

    

    for filename in os.listdir():
        print(filename)

    load_graph()

    app = Flask(__name__)

    app.config['SECRET_KEY'] = '2948sciWEO8c28HeK02Kejg2'

    app.register_blueprint(views, url_prefix='/')

    return app
