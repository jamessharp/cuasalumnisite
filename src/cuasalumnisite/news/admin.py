from models import Article
from django.contrib import admin
import datetime

class ArticleAdmin(admin.ModelAdmin):
    exclude = ('author', 'time')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.time = datetime.datetime.now()
        obj.save()

admin.site.register(Article, ArticleAdmin)
    