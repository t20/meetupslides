from redisco import models
redisco.connection_setup(host='localhost', port=6380, db=10)

class Person(models.Model):
    name = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fave_colors = models.ListField(str)

if __name__ == '__main__':
  xx = Person.objects.all()
  print 'Length:', len(xx)