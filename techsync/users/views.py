from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm,ProfileForm,SkillForm
from django.contrib import messages
from django.http import JsonResponse

from django.db.models import Q
from .utils import get_search_profile,paginateProfiles

#Authentication

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if email and password are provided
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                return redirect('profiles')  # Adjust the redirect URL as needed
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please provide both email and password.')
    
    # If not a POST request or if authentication failed, render the login page
    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('login')

# User Creation
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            messages.info(request, 'Please complete your profile.')
            return redirect('edit-account')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'users/register.html', context)








# Profile list


def Profiles(request):
    search_query = request.GET.get('search_query', '')
    profiles = get_search_profile(search_query)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/profiles.html', context)

#Single user profile data
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/user-profile.html', context) 


#User Account Main Page
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)

#Edit User Account
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)








@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



def get_skills(request):
    term = request.GET.get('q', '')
    skills = Skill.objects.filter(name__icontains=term)
    results = [{'value': skill.name, 'text': skill.name} for skill in skills]
    return JsonResponse(results, safe=False)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('user-account')

    context = {'object': skill}
    return render(request, 'main/delete_template.html', context)
