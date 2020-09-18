from flask import Flask,render_template, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from modules import app,db
from modules.modals import User_mgmt, Post
from modules.forms import Signup, Login


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User_mgmt.query.get(int(user_id))  

@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():

    form_sign = Signup()
    form_login = Login()

    if form_sign.validate_on_submit():
        hashed_password = generate_password_hash(form_sign.password.data, method='sha256')
        new_user = User_mgmt(username=form_sign.username.data, email=form_sign.email.data, password=hashed_password)
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))