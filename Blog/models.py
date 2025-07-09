from blog import db,login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60),unique=True)
    email=db.Column(db.String(120),index=True,unique=True) 
    password=db.Column(db.String(120),unique=True)
    profile_pic=db.Column(db.String(100),default="default.png")
    posts=db.relationship('Post',backref='author',lazy=True)
    comments=db.relationship('Comment',backref='commenter',lazy=True)

class Post(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120)) #120
    content=db.Column(db.String(1200)) #1200
    content_pic=db.Column(db.String(100),default="default.jpg")
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments=db.relationship('Comment',backref='post',lazy=True) 

class Comment(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(600)) 
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) 
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False) 
    