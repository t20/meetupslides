#!/usr/bin/env python
import redis
# import settings

'''
    source file copied from https://github.com/pims/retwis-py/blob/master/domain.py
'''


class Model(object):
  def __init__(self, id):
    self.__dict__['id'] = id

  def __eq__(self, other):
    return self.id == other.id

  def __setattr__(self, name, value):
    if name not in self.__dict__:
      klass = self.__class__.__name__.lower()
      key = '%s:id:%s:%s' % (klass, self.id, name.lower())
      r.set(key, value)
    else:
      self.__dict__[name] = value

  def __getattr__(self,name):
    if name not in self.__dict__:
      klass = self.__class__.__name__.lower()
      v = r.get('%s:id:%s:%s' % (klass, self.id, name.lower()))
      if v:
        return v
      raise AttributeError('%s doesn\'t exist' % name) 
    else:
      self.__dict__[name] = value

class User(Model):
  @staticmethod
  def find_by_username(username):
    _id = r.get("user:username:%s" % username)
    if _id is not None:
      return User(int(_id))
    else:
      return None

  @staticmethod
  def find_by_id(_id):
    if r.exists("user:id:%s:username" % _id):
      return User(int(_id))
    else:
      return None

  @staticmethod
  def create(username, password):
    user_id = r.incr("user:uid")
    if not r.get("user:username:%s" % username):
      r.set("user:id:%s:username" % user_id, username)
      r.set("user:username:%s" % username, user_id)
    
      #fake salting obviously :)
      salt = settings.SALT
      r.set("user:id:%s:password" % user_id, salt+password)
      r.lpush("users", user_id)
      return User(user_id)
    return None

  def posts(self, page=1):
    _from, _to = (page-1)*10, page*10
    posts = r.lrange("user:id:%s:posts" % self.id, _from, _to)
    if posts:
      return [Post(int(post_id)) for post_id in posts]
    return []

  def add_post(self, post):
    r.lpush("user:id:%s:posts" % self.id, post.id)
    r.sadd('posts:id', post.id)

  #added
  @property
  def slide_count(self):
    return r.llen("user:id:%s:posts" % self.id) or 0

class Post(Model):
  @staticmethod
  def create(user, content):
    post_id = r.incr("post:uid")
    post = Post(post_id)
    post.content = content
    post.user_id = user.id
    #post.created_at = Time.now.to_s
    user.add_post(post)

  @staticmethod
  def find_by_id(id):
    if r.sismember('posts:id', int(id)):
      return Post(id)
    return None
  
  @property
  def user(self):
    return User.find_by_id(r.get("post:id:%s:user_id" % self.id))
