from django.shortcuts import render
from projects.models import Project, Review, Tag
from event.models import Event, EventCategory
from group.models import Room, Message

from django.db.models import Count, Q, F
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from datetime import datetime

def admin_dashboard(request):
    # Get date filters from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse dates and set default values if necessary
    start_date = parse_date(start_date) if start_date else datetime.min.date()
    end_date = parse_date(end_date) if end_date else datetime.max.date()

    # Filter projects by date, excluding invalid dates
    projects = Project.objects.filter(created_at__range=[start_date, end_date]).exclude(created_at=datetime.min)

    # Data for Most Used Tags
    most_used_tags = Tag.objects.filter(project__in=projects).annotate(project_count=Count('project')).order_by('-project_count')[:10].values('name', 'project_count')

    # Data for Projects Over Time (Daily)
    projects_over_time = (
        projects
        .annotate(project_date=TruncDate('created_at'))
        .values('project_date')
        .annotate(count=Count('id'))
        .order_by('project_date')
    )

    # Format the dates for JavaScript
    for project in projects_over_time:
        project['project_date'] = project['project_date'].strftime('%Y-%m-%d')

    # Data for Top 5 Most Voted Projects with Vote Ratios
    top_voted_projects = (
        projects.annotate(
            total_votes=Count('review'),
            up_votes=Count('review', filter=Q(review__value='up')),
            calculated_vote_ratio=100 * F('up_votes') / F('total_votes')
        )
        .filter(total_votes__gt=0)
        .order_by('-total_votes')[:5]
        .values('title', 'total_votes', 'calculated_vote_ratio')
    )

    # Data for Events Over Time
    events = Event.objects.filter(created_at__range=[start_date, end_date]).exclude(created_at=datetime.min)
    events_over_time = (
        events
        .annotate(event_date=TruncDate('created_at'))
        .values('event_date')
        .annotate(count=Count('id'))
        .order_by('event_date')
    )

    # Format the dates for JavaScript
    for event in events_over_time:
        event['event_date'] = event['event_date'].strftime('%Y-%m-%d')

    # Data for Most Used Categories
    most_used_categories = EventCategory.objects.filter(event__in=events).annotate(event_count=Count('event')).order_by('-event_count')[:10].values('name', 'event_count')

    # Data for Top 5 Most Messages in a Room
    top_rooms = (
        Message.objects.values('room__name')
        .annotate(message_count=Count('id'))
        .order_by('-message_count')[:5]
    )

    # Data for Rooms Over Time (Daily)
    rooms_over_time = (
        Room.objects.annotate(room_date=TruncDate('created'))
        .values('room_date')
        .annotate(count=Count('id'))
        .order_by('room_date')
    )

    # Format the dates for JavaScript
    for room in rooms_over_time:
        room['room_date'] = room['room_date'].strftime('%Y-%m-%d')




    context = {
        'most_used_tags': list(most_used_tags),
        'projects_over_time': list(projects_over_time),
        'top_voted_projects': list(top_voted_projects),
        'events_over_time': list(events_over_time),
        'most_used_categories': list(most_used_categories),
        'start_date': start_date,
        'end_date': end_date,

        'top_rooms': list(top_rooms),
        'rooms_over_time': list(rooms_over_time),
    }
    return render(request, 'analytics/admin_charts.html', context)
