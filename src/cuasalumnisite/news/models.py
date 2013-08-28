from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length = 2000)
    time = models.DateTimeField('Date Published')
    author = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title