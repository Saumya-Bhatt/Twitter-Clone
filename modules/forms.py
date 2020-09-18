from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from modules.modals import User_mgmt

class Signup(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    signup = SubmitField('Sign up')

    def validate_username(self,username):
        user = User_mgmt.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one')

    def validate_email(self,email):
        user = User_mgmt.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account with this email ID already exists')

class Login(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =  BooleanField('Remember me')
    login = SubmitField('Login')

class createTweet(FlaskForm):
    tweet = TextAreaField('What is on your mind?',validators=[DataRequired(),Length(max=500)])
    submit = SubmitField('Tweet')