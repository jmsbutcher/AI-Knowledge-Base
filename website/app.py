"""
James Butcher
4/18/24
"""
from flask import Flask
from .kb_graph import load_graph, get_all_topics
from .views import views


def create_app():

    load_graph()

    # Initalize Flask
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')

    # Current topics:
    topics = get_all_topics()
    print("\nCurrent topics:")
    for t in topics:
        print(t)
    print()

    return app
