from django.shortcuts import render
from .models import *

# Create your views here.
def Profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html',context)