from django.db.models import Q
from .models import Profile

def get_search_profile(search_query):
    if search_query:
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(headline__icontains=search_query) |
            Q(skill__name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    else:
        profiles = Profile.objects.all()
    
    return profiles