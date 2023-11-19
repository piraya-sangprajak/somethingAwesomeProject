from . import db # means "from website import db"
from flask_login import UserMixin
from sqlalchemy.sql import func


# structure of the database table for storing note information 
class Note(db.Model):
    # ID is a primary key (unique identifier)
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    # foreign key relationship (one-many)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# structure of the database table for storing user information 
class User(db.Model, UserMixin):
    # ID is a primary key (unique identifier)
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # user model is associated with note model via foreign key relationship
    notes = db.relationship('Note')