from redisco import models

class Meetup(models.Model):
  name = models.Attribute(required=True)
  city = models.Attribute(required=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


class Post(models.Model):
  title = models.Attribute(required=True)
  desc = models.Attribute(required=True)
  meetup_id = models.IntegerField(required=True)
  user_id = models.IntegerField(required=True)
  author = models.Attribute(required=True)
  slides = models.ListField(str)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


class User(models.Model):
  name = models.Attribute(required=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
  name = models.Attribute(required=True)
  email = models.Attribute(required=True)
  subject = models.Attribute(required=True)
  message = models.Attribute(required=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


def get_meetup(meetup_id):
  return Meetup.objects.get_by_id(meetup_id)


def get_meetups():
  return Meetup.objects.all()


def get_posts(meetup_id):
  return Post.objects.filter(meetup_id=meetup_id)


def get_post(post_id):
  return Post.objects.get_by_id(post_id)


def get_recent_posts(limit=10):
    return Post.objects.all().limit(limit).order("-created")


def get_jobs():
    return []
    # return Job.objects.all()
