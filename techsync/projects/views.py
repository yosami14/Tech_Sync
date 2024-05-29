from django.shortcuts import render,redirect
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
from .utils import get_project_search_results, paginateProjects
# projects
def projects(request):
    search_query = request.GET.get('search_query', '')
    projects = get_project_search_results(search_query)
    custom_range, projects = paginateProjects(request, projects,3 )

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range':custom_range,
    }
    return render(request,'projects/projects.html',context)

def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    context = {
        'project': project,
        'tags': tags,
    }
    return render(request, 'projects/project_detail.html', context)

# create user and assosiate user with the project
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save_m2m()  # Save the many-to-many data
            return redirect('projects')

    context = {
        'form': form,
    }
    return render(request, 'projects/project_form.html',context)

#UPDATE PROJECT
@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance = project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {
        'form': form,

    }
    return render(request, 'projects/project_form.html',context)

#DELETE PROJECT
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render (request, 'main/delete_template.html', context)


from django.http import JsonResponse
from .models import Tag

def get_tags(request):
    term = request.GET.get('q', '')
    tags = Tag.objects.filter(name__icontains=term)
    results = [{'value': tag.name, 'text': tag.name} for tag in tags]
    return JsonResponse(results, safe=False)
