# 5/5/24 - Content management system (database)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
DB_NAME = "kbdata.db"
DB_URI = "sqlite:///" + DB_NAME



class Topic(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    textname: Mapped[str] = mapped_column(db.String, unique=False, nullable=True)
    description: Mapped[str] = mapped_column(db.Text)

# class Topic(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True)
#     description = db.Column(db.Text)

class ContentPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    code_snippet = db.Column(db.Text)
    #links = db.relationship('Link', backref='content_page')

class Link(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    source_topic_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('topic.id'))
    target_topic_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('topic.id'))

# class Link(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     source_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
#     target_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

# class TopicForm(FlaskForm):
#     name = StringField('Topic Name')
#     description = TextAreaField('Topic Description')

# class ContentPageForm(FlaskForm):
#     title = StringField('Content Page Title')
#     content = TextAreaField('Content')
#     code_snippet = TextAreaField('Code Snippet')

