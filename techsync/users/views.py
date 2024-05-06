from django.shortcuts import render
from .models import *

# Create your views here.
def Profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html',context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    skills = profile.skill_set.all()
    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'users/user-profile.html', context) 