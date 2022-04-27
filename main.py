from flask import Flask, redirect,render_template,url_for
from flask_bootstrap import Bootstrap
from werkzeug.security  import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy


"""
TODO: 
- gitignore x
- requirements x
- readme.md x
- create login and registration x
- create database tables :  x
        - User
        - Lists -> user child

"""

# create app
app = Flask(__name__)
app.secret_key(os.environ.get('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

db = SQLAlchemy(app)



#DATABASE STRUCTURE

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    # email
    # login
    #password encoded
    #created_at - timestamp
    # list table relationship


# class Todo(db.Model):
#     __tablename__ = 'todos'
#     id = db.Column(db.Integer,primary_key=True)



