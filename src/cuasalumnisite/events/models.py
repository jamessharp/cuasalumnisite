from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
import cuasalumnisite.settings as settings

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = tinymce_models.HTMLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True)
    author = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
    
    class Admin:
        js = (
              '%sjs/tiny_mce/tiny_mce.js' % settings.MEDIA_URL,
              )
