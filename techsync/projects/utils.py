from django.db.models import Q
from .models import Project

def get_project_search_results(search_query):
    if search_query:
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        )
    else:
        projects = Project.objects.all()
    
    return projects