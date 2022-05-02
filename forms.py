from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    login = StringField(label="Login",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    email = StringField(label="Email",validators=[DataRequired(),Email()])
    login = StringField(label="Login",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField("Sign Up")
    

class TaskForm(FlaskForm):
    task = StringField(label="",validators=[DataRequired()])
    submit = SubmitField("Add")