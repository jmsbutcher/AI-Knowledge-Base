"""
James Butcher
4/18/24
"""
from flask import Flask
from .cms import DB_NAME, DB_URI, db, ContentPage, Topic
from .kb_graph import n, load_graph, graph, get_all_topics, \
    isolate_last_part_of_URI, triple_to_text
from .views import views
from os import path


def create_app():

    load_graph()

    # Initalize Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2948sciWEO8c28HeK02Kejg2'
    app.register_blueprint(views, url_prefix='/')


    # Current topics:
    topics = get_all_topics()
    print("\nCurrent topics:")
    for t in topics:
        print(t)
    print()


    # Initalize Database 
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    # db.init_app(app)
    # with app.app_context():

    #     db.drop_all()
    #     db.create_all()

    #     # Current topics:
    #     topics = db.session.execute(db.select(Topic)).scalars()
    #     print("\nCurrent topics:")
    #     for t in topics:
    #         print(t.name)
    #     print()

    #     # Add any topics not yet added to the database from the RDF graph
    #     topics = get_all_topics()

    #     existing_topics = set([t.name for t in Topic.query.all()])
    #     for topic in topics:
    #         if topic not in existing_topics:

    #             new_topic = Topic(
    #                 name=topic, 
    #                 textname=topic.replace("_", " ").title(),
    #                 description="[description]"
    #                 )
                
    #             db.session.add(new_topic)

        
    #     #Topic.query.filter(Topic.name == "Topic 2").delete()

    #     db.session.commit()

        

        # Add any custom stuff to database before startup



    return app
