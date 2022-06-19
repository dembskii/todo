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
- requirements -> make requirements up do date +
- readme.md +
- create login and registration +
- create database tables :  +
        - User +
        - Lists -> user child + 
- if user logged in show todo list, otherwise show login and register buttons +
- wtf.quick_form -> to handmade form +
- navbar -> align +
- navbar -> color +
- homepage +
- remove task +
- add task +
- change state of task +
- sort css +
- make website mobile friendly and fully responsible +
- footer is bugged on smartphones +
- make summary how much tasks are done +
- add complete button when all tasks are completed and make functionality -> clear +
- fluent srollbar  + 
- update preview -
- rework icon
"""

#FIXME: bug connected with icons on right when text is too long

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

class User(db.Model,UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40),nullable=False,unique=True)   # email
    login = db.Column(db.String(20),nullable=False,unique=True)   # login
    password = db.Column(db.String,nullable=False)     #password encoded
    created_at = db.Column(db.Integer,nullable=False)   #created_at - timestamp

    tasks = db.relationship("Todo",backref='user')



class Todo(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(150),nullable=False)
    is_active = db.Column(db.Boolean,nullable=False)

    # user_id relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    user_tasks = current_user.tasks
    tasks_done = 0
    for task in user_tasks:
        if task.is_active == 1:
            tasks_done += 1


    return render_template('todo.html',logged_in= current_user,form=task_form,tasks_done=tasks_done,tasks_total=len(user_tasks))

# route /remove_element 
@app.route('/remove/<int:task_id>')
@login_required
def remove_task(task_id):
    
    task = Todo.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('todo'))

# route /add element
@app.route('/add',methods=["POST","GET"])
@login_required
def add_task():

    if request.method=="POST":
        task = Todo(
            task=request.form['task'],
            is_active=False,
            user=User.query.filter_by(id=current_user.id).first()
                   )
        
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('todo'))

# route /change state of element
@app.route('/change_state/<int:task_id>')
@login_required
def change_task_state(task_id):

    task = Todo.query.filter_by(id=task_id).first()

    if task.is_active == False:
        task.is_active = True
    
    elif task.is_active == True:
        task.is_active = False

    
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/complete')
@login_required
def complete():
    
    for task in current_user.tasks:
        db.session.delete(task)

    db.session.commit()

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

