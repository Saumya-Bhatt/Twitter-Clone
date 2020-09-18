from flask import Flask,render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from run import app
from forms import createTweet
from login import *
import datetime

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user_tweet = createTweet()
    if user_tweet.validate_on_submit():
        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))
        return render_template('tweet.html',tweet = user_tweet.tweet.data, user = current_user.username, stamp = currentTime)
    return render_template('dashboard.html',name = current_user.username,tweet = user_tweet)
