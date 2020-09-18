from modules import db,app
from flask_login import UserMixin
from datetime import datetime

class User_mgmt(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)

class Post(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet = db.Column(db.String(500),nullable=False)
    stamp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user_mgmt.id'),nullable=False)