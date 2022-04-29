from flask import Flask, redirect,render_template,url_for
from flask_bootstrap import Bootstrap
from werkzeug.security  import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy


"""
TODO: 
- gitignore +
- requirements /
- readme.md /
- create login and registration /
- create database tables :  /
        - User
        - Lists -> user child
- if user logged in show todo list, otherwise show login and register buttons

"""

# create app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

db = SQLAlchemy(app)



#DATABASE STRUCTURE

#FIXME:
class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40),nullable=False)   # email
    login = db.Column(db.String(20),nullable=False)   # login
    password = db.Column(db.String,nullable=False)     #password encoded
    created_at = db.Column(db.Integer,nullable=False)   #created_at - timestamp

    todo_list = db.relationship("Todo",backref='user')



class Todo(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    item = db.Column(db.String(150),nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    # author_id relationship


db.create_all()



@app.route('/')
def home():
    return "anything"

#route /login

#route /register

# route /remove_element

# route /add element

# route /change state of element

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)