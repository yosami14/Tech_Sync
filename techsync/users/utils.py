from django.db.models import Q
from .models import Profile
# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles

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