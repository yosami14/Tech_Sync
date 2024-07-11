from django.db.models import Q
from .models import Event
# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginateEvents(request, events, results):

    page = request.GET.get('page')
    paginator = Paginator(events, results)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        events = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        events = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, events

#Search Events
def get_event_search_results(search_query):
    if search_query:
        events = Event.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(organizer__name__icontains=search_query) |
            Q(speakers__name__icontains=search_query)

        )
    else:
        events = Event.objects.all()
    
    return events