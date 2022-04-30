from enum import unique
from flask import Flask, redirect,render_template,url_for
from flask_bootstrap import Bootstrap
from werkzeug.security  import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm,RegisterForm
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required

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
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

db = SQLAlchemy(app)


# login_manager = LoginManager()
# login_manager.init_app(app)


#DATABASE STRUCTURE

#FIXME:
class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40),nullable=False,unique=True)   # email
    login = db.Column(db.String(20),nullable=False,unique=True)   # login
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
    return render_template('index.html')

#route /login

@app.route('/login',methods=["POST","GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(login_form.data)

        # Check if user is registered
        # if email found -> hash password and compare to password in db
        # if not registered -> flash message and redirect to register route
    return render_template('login.html',form=login_form)


#route /register
@app.route('/register',methods=["POST","GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        print(register_form.data)
        # Check if email is in db
        # if false
            #check if login is in db
            #if false -> add user to db
            # if true -> flash message login is taken, redirect /register
        # if true -> flash message email is taken, redirect /register

    return render_template('register.html',form=register_form)
# route /remove_element

# route /add element

# route /change state of element

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)