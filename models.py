from redisco import Model

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
  slides = models.ListField(str)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


class User(models.Model):
  name = models.Attribute(required=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

