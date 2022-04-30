from asyncio import Task
from enum import unique
from flask import Flask, flash, redirect,render_template,url_for,request
from flask_bootstrap import Bootstrap
from werkzeug.security  import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm,RegisterForm,TaskForm
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
import datetime
"""
TODO: 
- gitignore +
- requirements /
- readme.md /
- create login and registration +
- create database tables :  /
        - User +
        - Lists -> user child
- if user logged in show todo list, otherwise show login and register buttons +
- wtf.quick_form -> to handmade form +
- navbar -> align +
- navbar -> color +
- homepage - 
- remove task -
- add task -
- change state of task -
- sort css -

"""

# create app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#DATABASE STRUCTURE

#FIXME:
class User(db.Model,UserMixin):
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
    is_active = db.Column(db.Boolean,nullable=False)

    # user_id relationship
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


db.create_all()



@app.route('/')
def home():
    return render_template('index.html',logged_in=current_user.is_authenticated)

#route /login

@app.route('/login',methods=["POST","GET"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        # Check if user is registered
        # if email found -> hash password and compare to password in db
        # if not registered -> flash message and redirect to register route
        user = User.query.filter_by(login=request.form['login']).first()
        if user:
            if check_password_hash(pwhash=user.password,password=request.form['password']):
                login_user(user)
                return redirect(url_for('todo'))
            else:
                flash("You have passed wrong password")
                return redirect(url_for('login'))
        else:
            flash("User with that login does not exist.")
            return redirect(url_for('login'))


    return render_template('login.html',form=login_form,logged_in=current_user.is_authenticated)


#route /register
@app.route('/register',methods=["POST","GET"])
def register():
    register_form = RegisterForm()
    if request.method == "POST":
        if User.query.filter_by(email=request.form['email']).first():
            flash("This email has been used.")
            return redirect(url_for('register'))
        else:
            if User.query.filter_by(login=request.form['login']).first():
                flash("This login has been used.")
            else:
                #generate password
                encoded_password = generate_password_hash(password=request.form['password'],method='pbkdf2:sha256',salt_length=8)

                user = User(
                    email = request.form['email'],
                    login = request.form['login'],
                    password = encoded_password,
                    created_at = datetime.datetime.now().timestamp( )
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('todo'))
        # Check if email is in db
        # if false
            #check if login is in db
            #if false -> add user to db
            # if true -> flash message login is taken, redirect /register
        # if true -> flash message email is taken, redirect /register


    return render_template('register.html',form=register_form,logged_in=current_user.is_authenticated)

    if register_form.validate_on_submit():
        print(register_form.data)

        if User.query.filter_by(email=register_form.data['email']).first():
            flash("This email has been used.")
            return redirect(url_for('register'))
        else:
            if User.query.filter_by(login=register_form.data['login']).first():
                flash("This login has been used.")
            else:
                #generate password
                encoded_password = generate_password_hash(password=register_form.data['password'],method='pbkdf2:sha256',salt_length=8)

                user = User(
                    email = register_form.data['email'],
                    login = register_form.data['login'],
                    password = encoded_password,
                    created_at = datetime.datetime.now().timestamp( )
                )
                db.session.add(user)
                db.session.commit()

# logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# todo route
@app.route('/todo',methods=["POST","GET"])
@login_required
def todo():
    task_form = TaskForm()

    if request.method=="POST":
        pass
    #     # add task to current user's tasks
    
    return render_template('todo.html',logged_in= current_user.is_authenticated,form=task_form)

# route /remove_element 

# route /add element

# route /change state of element

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)