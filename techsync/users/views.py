from django.shortcuts import render

# Create your views here.
def Profiles(request):
    return render(request, 'users/profiles.html')