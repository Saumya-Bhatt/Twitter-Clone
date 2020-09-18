from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class Signup(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    signup = SubmitField('Sign up')

class Login(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =  BooleanField('Remember me')
    login = SubmitField('Login')

class createTweet(FlaskForm):
    tweet = TextAreaField('What is on your mind?',validators=[DataRequired()])
    submit = SubmitField('Tweet')