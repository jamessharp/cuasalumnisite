from django.db import models
from tinymce import models as tinymce_models

# Create your models here.

class Setting(models.Model):
    # These will be sent for use in every template for generic use.
    name = models.CharField(max_length=100, primary_key=True)
    value = tinymce_models.HTMLField()

    def __unicode__(self):
        return self.name
