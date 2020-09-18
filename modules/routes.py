from flask import Flask,render_template, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from modules import app,db
from modules.modals import User_mgmt, Post
from modules.forms import Signup, Login, UpdateProfile, createTweet

import datetime


@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():

    # add this to those routes which you want the user from going to if he/she is already logged in
    #if current_user.is_authenticated:
    #    return redirect(url_for(''))

    form_sign = Signup()
    form_login = Login()

    if form_sign.validate_on_submit():
        hashed_password = generate_password_hash(form_sign.password.data, method='sha256')
        x = datetime.datetime.now()
        creation = str(x.strftime("%B")) +" "+ str(x.strftime("%Y")) 
        new_user = User_mgmt(username=form_sign.username.data, email=form_sign.email.data, password=hashed_password, date=creation)
        db.session.add(new_user)
        db.session.commit()
        return render_template('sign.html')

    if form_login.validate_on_submit():
        user_info = User_mgmt.query.filter_by(username=form_login.username.data).first()
        if user_info:
            if check_password_hash(user_info.password, form_login.password.data):
                login_user(user_info, remember=form_login.remember.data)
                return redirect(url_for('dashboard'))
            else:
                return render_template('errorP.html')
        else:
            return render_template('errorU.html')

    return render_template('start.html',form1=form_sign,form2=form_login)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    update = UpdateProfile()
    profile_pic = url_for('static',filename='profile_pics/' + current_user.image_file)
    bg_pic = url_for('static',filename='profile_pics/' + current_user.bg_file)

    return render_template('account.html',profile=profile_pic,background=bg_pic,update=update)

    

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user_tweet = createTweet()
    if user_tweet.validate_on_submit():
        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))
        return render_template('tweet.html',tweet = user_tweet.tweet.data, user = current_user.username, stamp = currentTime)
    return render_template('dashboard.html',name = current_user.username,tweet = user_tweet)
