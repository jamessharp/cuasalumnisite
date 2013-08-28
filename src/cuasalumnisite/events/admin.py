'''
Created on 17 Apr 2011

@author: James
'''

from models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        
        #Don't allow a null end_time - instead set it to the start time
        if not obj.end_time:
            obj.end_time = obj.start_time
            
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Event, EventAdmin)
