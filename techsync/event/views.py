from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from users.models import User
from .forms import OrganizerForm,ProfileForm
from django.contrib.auth.decorators import login_required



# Create your views here.
# User Creation
def registerOrganizer(request):
    if request.user.is_authenticated:
        return redirect('organizer-dashboard')
    
    form = OrganizerForm()

    if request.method == 'POST':
        form = OrganizerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_event_organizer = True
            print("Orginizer user created")
            user.save()

            messages.success(request, 'Organizer account was created!')

            login(request, user)
            messages.info(request, 'Please complete your organization profile.')
            return redirect('edit-organizer-profile')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'event/register.html', context)


#Edit User Account
@login_required(login_url='login')
def editAccount(request):
    organization = request.user.eventorganizer
    form = ProfileForm(instance=organization)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()

            return redirect('organization-account')

    context = {'form': form}
    return render(request, 'event/profile_form.html', context)


#User Account Main Page
@login_required(login_url='login')
def userAccount(request):
    organization = request.user.eventorganizer
    events = organization.event_set.all()

    context = {
        'profile': organization, 
        'events': events
        }
    return render(request, 'event/account.html', context)


