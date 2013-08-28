from django.shortcuts import render_to_response
from django.template import RequestContext
from cuasalumnisite.news.models import Article
from cuasalumnisite.events.models import Event
from datetime import datetime

def index(request):
    articles = Article.objects.all().order_by('-time')[:3]
    events = Event.objects.filter(end_time__gt=datetime.now()).order_by('start_time')[:3]
    return render_to_response('home/index.html',
                              {'news_items' : articles,
                               'events_items': events}, 
                              context_instance=RequestContext(request))
