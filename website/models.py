from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Photo', backref='user', passive_deletes=True)

    def __repr__(self):
        return "<User %r>" % (self.username)


class UserView(ModelView):
    form_columns = ["id", "email", "username", "password", "date_created", "posts"]


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        User.id, ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<Photo %r>" % (self.author)

class PhotoView(ModelView):
    form_columns = ["id", "img", "date_created", "author"]