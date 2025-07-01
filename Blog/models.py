from blog import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60),unique=True)
    email=db.Column(db.String(120),index=True,unique=True) 
    password=db.Column(db.String(120),unique=True)