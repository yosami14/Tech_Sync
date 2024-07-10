from users.models import Profile, EventOrganizer, EventModerator
def navbar_data(request):
    profile = event_organizer = event_moderator = None

    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
        if hasattr(request.user, 'eventorganizer'):
            event_organizer = request.user.eventorganizer
        if hasattr(request.user, 'eventmoderator'):
            event_moderator = request.user.eventmoderator

    return {
        'profile': profile,
        'event_organizer': event_organizer,
        'event_moderator': event_moderator,
    }