from .models import *
from group.models import Room, Topic,Message
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm,ProfileForm,SkillForm,InboxForm
from django.contrib import messages
from django.http import JsonResponse

from django.db.models import Q
from .utils import get_search_profile,paginateProfiles
from .decorators import redirect_based_on_role

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
                return redirect_based_on_role(user)
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
    
    
    rooms = Room.objects.filter(host=request.user)

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'rooms': rooms,
    }
    return render(request, 'users/account.html', context)


#cv creator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Profile

@login_required(login_url='login')
def download_cv(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    
    # Render the HTML template
    html = render_to_string('users/cv_template.html', context)
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response






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


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewInbox(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createInbox(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = InboxForm()
    sender = request.user.profile

    if request.method == 'POST':
        form = InboxForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender and sender.name and sender.user.email:
                message.senderName = sender.name
                message.email = sender.user.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    # Debugging wanted to check if the recipient and sender are correct
    print(f'Recipient: {recipient}') 
    print(f'Sender Name: {sender.name if sender else None}')
    print(f'Sender Email: {sender.user.email if sender else None}') 

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)