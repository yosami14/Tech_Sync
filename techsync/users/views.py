from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
from django.contrib import messages


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
            return redirect('Profiles')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def Profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html',context)

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

def userAccount(request):
    context = {}
    return render(request, 'users/account.html', context)