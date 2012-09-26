from flask.ext.admin import BaseView, expose
from models import *

class Dashboard(BaseView):
    @expose('/')
    def index(self):
        posts = get_recent_posts(10)
        x = len(Meetup.objects.all())
        y = len(Post.objects.all())
        return self.render('admin/index.html', posts=posts, x=x, y=y)