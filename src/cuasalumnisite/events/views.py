import datetime
import calendar
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from models import Event

class Month():
    
    def __init__(self, month):
        self.int = month
        self.str = calendar.month_name[month]

    def __str__(self):
        return self.str

class Year():
    
    def __init__(self, year):
        self.this = year
        self.prev = year - 1
        self.next = year + 1
    
    def __str__(self):
        return str(self.this)

def eventDict(year, month):
    
    # If we haven't been passed in a year use the current year
    if not year:
        year = datetime.date.today().year
        
    # if we haven't been passed in a month use the current month
    if not month:
        month = datetime.date.today().month
        
    month = int(month)
    year = int(year)
        
    # raise a 404 if the month is greater than 12
    if month > 12:
        raise Http404("%s is not a valid month" % month)
        
    # Get the full name of the current month
    current_month = Month(month)
    months = [Month(m) for m in range(1, 13)]
    
    # Get all events and those in the given month/year
    events_all = Event.objects.all().order_by('start_time')
    if month == 12:
        events_month = [e for e in events_all if ((e.start_time < datetime.datetime(year + 1, 1, 1)) and
                                                  (e.end_time >= datetime.datetime(year, month, 1)))]
    else:
        events_month = [e for e in events_all if ((e.start_time < datetime.datetime(year, month + 1, 1)) and
                                                  (e.end_time >= datetime.datetime(year, month, 1)))]
        
    # Lets put all future events into the list.
    events_future = [e for e in events_all if (e.end_time >= datetime.datetime.now())]
    
    return {"current_month" : current_month,
            "months" : months,
            "year" : Year(year),
            "events_all" : events_future,
            "events_month" : events_month}
    
def eventYearMonthView(request, year, month):
    return render_to_response("events/events_list.html",
                              eventDict(year, month),
                              context_instance=RequestContext(request))
    
def eventMonthView(request, month):
    return render_to_response("events/events_list.html",
                              eventDict(None, month),
                              context_instance=RequestContext(request))
    
def eventView(request):
    return render_to_response("events/events_list.html",
                              eventDict(None, None),
                              context_instance=RequestContext(request))
    
def eventYearView(request, year):
    return render_to_response("events/events_list.html",
                              eventDict(year, None),
                              context_instance=RequestContext(request))

def eventDetailView(request, event_id):
    # Get the event and look up its start date
    event = get_object_or_404(Event, id=event_id)
    
    start_date = event.start_time
    month = start_date.month
    year = start_date.year
    
    responseDict = eventDict(year, month)
    responseDict["event"] = event
    
    return render_to_response("events/events_detail.html",
                              responseDict,
                              context_instance=RequestContext(request))
    
    
    
    
    
