from django.shortcuts import render
from .models import Project

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,

    }
    return render(request,'projects/projects.html',context )

def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    context = {
        'project': project,
        'tags': tags,
    }
    return render(request, 'projects/project_detail.html', context)
