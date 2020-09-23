from flask import Flask,render_template, redirect, url_for, flash, request, abort
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from modules import app,db
from modules.modals import User_mgmt, Post
from modules.forms import Signup, Login, UpdateProfile, createTweet

import datetime
import secrets
import os

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
    all_posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.id))

    return render_template('account.html',profile=profile_pic,background=bg_pic,update=update,timeline=all_posts)

    

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user_tweet = createTweet()
    if user_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        post = Post(tweet=user_tweet.tweet.data, stamp=currentTime, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('The Tweet was added to your timeline!','success')
        return redirect(url_for('dashboard'))

    posts = Post.query.order_by(desc(Post.id))
    return render_template('dashboard.html',name = current_user.username,tweet = user_tweet, timeline=posts)


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

@app.route('/UpdateInfo',methods=['GET','POST'])
@login_required
def updateInfo():

    update = UpdateProfile()
    if update.validate_on_submit():
        if update.profile.data:
            profile_img = save_picture(update.profile.data)
            current_user.image_file = profile_img
        if update.profile_bg.data:
            profile_bg_img = save_picture(update.profile_bg.data)
            current_user.bg_file = profile_bg_img
        if update.bday.data:
            current_user.bday = update.bday.data

        current_user.username = update.username.data
        current_user.email = update.email.data
        current_user.bio = update.bio.data
        db.session.commit()

        flash('Your account has been updated!','success')
        return redirect(url_for('account'))

    elif request.method == 'GET':

        update.username.data = current_user.username
        update.email.data = current_user.email
        update.bio.data = current_user.bio

    return render_template('updateProfile.html',change_form=update)


@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('delete_post.html',post=post)

@app.route('/delete_post/<int:post_id>',methods=['POST'])
@login_required
def delete_tweet(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your tweet was deleted!','success')
    return redirect(url_for('dashboard'))


@app.route('/deactivate_confirmation')
@login_required
def deactivate_confirm():
    return render_template('deact_conf.html')

@app.route('/account_deleted/<int:account_id>',methods=['POST'])
@login_required
def delete_account(account_id):
    all_post = Post.query.filter_by(user_id=current_user.id)
    for i in all_post:
        db.session.delete(i)
    del_acc = User_mgmt.query.filter_by(id=account_id).first()
    db.session.delete(del_acc)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/view_profile/<int:account_id>',methods=['GET','POST'])
@login_required
def viewProfile(account_id):
    if account_id == current_user.id:
        return redirect(url_for('account'))
    get_user = User_mgmt.query.filter_by(id=account_id).first()
    profile_pic = url_for('static',filename='profile_pics/' + get_user.image_file)
    bg_pic = url_for('static',filename='profile_pics/' + get_user.bg_file)
    all_posts = Post.query.filter_by(user_id=get_user.id).order_by(desc(Post.id))

    return render_template('view_profile.html',profile=profile_pic,background=bg_pic,timeline=all_posts,user=get_user)


@app.route('/retweet/<int:post_id>',methods=['GET','POST'])
@login_required
def retweet(post_id):

    post = Post.query.get_or_404(post_id)
    new_tweet = createTweet()

    if new_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        retweet = Post(tweet=new_tweet.tweet.data,stamp=currentTime, author=current_user,retweet_tweet=post.tweet,retweet_stamp=post.stamp,retweet_author=post.author.username,retweet_id=post.author.id)
        db.session.add(retweet)
        db.session.commit()

        msg = 'You retweeted @'+post.author.username+"'s tweet!"
        flash(msg,'success')
        return redirect(url_for('dashboard'))

    return render_template('retweet.html',post=post, tweet=new_tweet)