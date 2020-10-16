from modules import app
import secrets
import os

def save_profile_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def save_bg_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def delete_old_images(image, bg_image):
    profile_pic_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', image)
    bg_pic_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', bg_image)
    if image!='default.jpg' and image!='':
        try:
            os.remove(profile_pic_path)
        except OSError:
            pass
    if bg_image!='default_bg.jpg' and bg_image!='':
        try:
            os.remove(bg_pic_path)
        except OSError:
            pass

def save_tweet_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Tweets', picture_fn)
    form_pic.save(picture_path)
    return picture_fn