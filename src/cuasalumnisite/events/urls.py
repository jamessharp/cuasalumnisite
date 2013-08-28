from django.conf.urls.defaults import *

urlpatterns = patterns('cuasalumnisite.events.views',
    url(r'^$', 'eventView', name='events_url'),
    url(r'^(\d{4})/$', 'eventYearView', name='event_year'),
    url(r'^(\d{2})/$', 'eventMonthView', name='event_month'),
    url(r'^(\d{4})/(\d{1,2})/$', 'eventYearMonthView', name='event_yearmonth'),
    url(r'^event/(\d+)/$', 'eventDetailView', name="event_detail"),
)