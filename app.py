### Meetupslides
### https://github.com/teraom/meetupslides

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import redis
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import urlparse

import settings
from models import *

from flask.ext.admin import Admin
from admin import *

################################
####### init and CONFIG ########
################################

app = Flask(__name__)
app.config.from_object('settings.Config')
app.secret_key = app.config['APP_SECRET_KEY']
# admin = Admin(app, index_view=Dashboard)
admin = Admin(app, name='Meetup Slides Admin')
# admin.index_view = Dashboard

# Load from config
REDIS_HOST = app.config['REDIS_HOST']
REDIS_PORT = app.config['REDIS_PORT']
REDIS_DB = app.config['REDIS_DB']
AWS_KEY = app.config['AWS_KEY']
AWS_SECRET_KEY = app.config['AWS_SECRET_KEY']
BUCKET_NAME = app.config['BUCKET_NAME']

redis_url = os.environ.get('REDISTOGO_URL', None)
if redis_url:
    redis_url = urlparse.urlparse(redis_url)
    settings.r = redis.Redis(host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)
else:
    settings.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'pptx', 'zip', 'tar', 'rar'])

# Admin views
admin.add_view(Dashboard(name='Dashboard'))

################################
####### helper methods #########
################################

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def secure_filename(filename):
    return filename


def upload_to_s3(filename, post_id, ext):
    conn = S3Connection(AWS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    k = Key(bucket)
    k.key = 'slides_{0}.{1}'.format(post_id, ext)
    print 'key:', k.key
    k.set_contents_from_filename(filename)
    k.make_public()
    print 'Done upload'
    filename = get_s3_filename(post_id, ext)
    return filename


def get_s3_filename(post_id, ext):
    return 'https://s3.amazonaws.com/{0}/post.{1}.{2}'.format(BUCKET_NAME, post_id, ext)
    


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


@app.route('/meetup/add', methods=['GET', 'POST'])
def meetup_add():
    if request.method == 'GET':
        return render_template('add_meetup.html')
    name = request.form.get('meetup_name', 'No Name')
    city = request.form.get('meetup_city', 'No City')
    ajax = request.form.get('ajax', 0)
    m = Meetup(name=name, city=city)
    saved = m.save()
    if not ajax:
        return redirect(url_for('meetup', meetup_id=m.id))
    # if this is an ajax call, return json response
    if saved:
        return jsonify(name=name, city=city, id=m.id)
    else:
        return jsonify(error=True)


@app.route('/meetup/<meetup_id>')
def meetup(meetup_id):
    meetup = get_meetup(meetup_id)
    posts = get_posts(meetup_id)
    return render_template('meetup.html', meetup=meetup, posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        meetups = get_meetups()
        selected_meetup_id = request.args.get('meetup_id', 0)
        return render_template('add.html', meetups=meetups, selected_meetup_id=selected_meetup_id)
    title = request.form.get('title', 'No Title')
    desc = request.form.get('desc', 'No desc')
    author = request.form.get('author', 'A developer')
    user_id = request.form.get('user_id', 0)
    meetup_id = int(request.form.get('meetup_id', 0))
    p = Post(title=title, desc=desc, user_id=user_id, meetup_id=meetup_id, author=author)
    saved = p.save()
    post_id = p.id
    # store s3 file path
    slides = request.files['slides']
    if slides and allowed_file(slides.filename):
        filename = secure_filename(slides.filename)
        # try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        slides.save(filepath)
        ext = filename.rsplit('.', 1)[1]
        s3_filename = upload_to_s3(filepath, post_id, ext)
        os.remove(filepath)
        p.slides = [s3_filename]
        p.save()
        # except Exception as e:
        #     print 'Exception'
    # print 'Post saved?', saved
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
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    subject = request.form.get('subject', None)
    message = request.form.get('message', None)
    m = Message(name=name, email=email, subject=subject, message=message)
    saved = m.save()
    if saved:
      flash('Thanks! We ll get back to you shortly')
    else:
      flash('Something went wrong! Could not send message.')
    return redirect(url_for(contact))


@app.route('/jobs')
def jobs():
    jobs = get_jobs()
    return render_template('jobs.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 0))
    if port:
        app.run(host='0.0.0.0', port=port)
    else:
        app.debug = True
        app.run()
