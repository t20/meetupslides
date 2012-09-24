### Meetupslides
### https://github.com/teraom/meetupslides

from flask import Flask, render_template, request, redirect, url_for, flash
import redis

import settings
from models import *

from flask.ext.admin import Admin

################################
####### init and CONFIG ########
################################

app = Flask(__name__)
app.config.from_object('settings.Config')
app.secret_key = app.config['APP_SECRET_KEY']
admin = Admin(app)

REDIS_HOST = app.config['REDIS_HOST']
REDIS_PORT = app.config['REDIS_PORT']
REDIS_DB = app.config['REDIS_DB']

settings.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'pptx', 'zip', 'tar', 'rar'])

################################
####### helper methods #########
################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


################################
####### All router methods #####
################################


@app.route('/')
def index():
    posts = get_recent_posts()
    return render_template('index.html', posts=posts)


@app.route('/meetups')
def meetups():
    meetups = get_meetups()
    return render_template('meetups.html', meetups=meetups)


@app.route('/meetup/<meetup_id>')
def meetup(meetup_id):
    meetup = get_meetup(meetup_id)
    posts = get_posts(meetup_id)
    return render_template('meetup.html', meetup=meetup, posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        meetups = get_meetups()
        return render_template('add.html', meetups=meetups)
    # else - POST
    # TODO look into flask wtf
    # get post data and add to database
    title = request.form.get('title', 'No Title')
    desc = request.form.get('desc', 'No desc')
    slides = request.files['slides']
    user_id = request.form.get('user_id', 0)
    meetup_id = int(request.form.get('meetup_id', 0))
    p = Post(title=title, desc=desc, user_id=user_id, meetup_id=meetup_id)
    saved = p.save()
    # print 'Post saved?', saved
    post_id = p.id
    flash('Add new post.')
    return redirect(url_for('post', post_id=post_id))


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'GET':
        post = get_post(post_id)
        return render_template('post.html', post=post)
    # else  - POST
    # update_post()
    return render_template('post.html', post=post)


@app.route('/search')
def search():
    pass


@app.route('/user/<user_id>')
def user(user_id):
    pass


# TODO - research flask login
@app.route('/login')
def login():
    """docstring for login"""
    pass


@app.route('/logout')
def logout():
    """docstring for logout"""
    pass


@app.route('/register')
def register():
    """docstring for register"""
    pass


@app.route('/profile')
def profile():
    """docstring for profile"""
    pass


@app.route('/contact', methods=['GET', 'POST'])
def contact(post_id):
    if request.method == 'GET':
        return render_template('contact.html')


@app.route('/jobs')
def jobs():
    jobs = get_jobs()
    return render_template('jobs.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
