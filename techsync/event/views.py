from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from users.models import User, Profile
from event.models import EventCategory,Event,EventOrganizer
from .forms import OrganizerForm,ProfileForm, EventForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


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


#Add Event
@login_required(login_url='login')
def addEvent(request):
    organizer = request.user.eventorganizer
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = organizer
            event.save()
            form.save_m2m()  # Save the many-to-many data
            messages.success(request, "Event added successfully.")
            return redirect('organization-account')
        else:
            # Handle form errors and display them
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f"Error with '{field_name}': {error}")

    context = {
        'form': form
    }
    return render(request, 'event/event_form.html', context)

# selectize 
def get_speakers(request):
    term = request.GET.get('q', '')
    speakers = Profile.objects.filter(user__username__icontains=term)
    results = [{'value': speaker.user.username, 'text': speaker.user.username} for speaker in speakers]
    return JsonResponse(results, safe=False)
# selectize 
def get_event_categories(request):
    term = request.GET.get('q', '')
    categorys = EventCategory.objects.filter(user__username__icontains=term)
    results = [{'value': category.name, 'text': category.name} for category in categorys]
    return JsonResponse(results, safe=False)


#UPDATE Event
@login_required(login_url='login')
def updateEvent(request, pk):
    organizer = request.user.eventorganizer
    event = organizer.event_set.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.verified_by = None
            event.is_verified = False
            event.save()
            messages.success(request, "Event updated successfully.")
            return redirect('organization-account')

    context = {
        'form': form
    }
    return render(request, 'event/event_form.html', context)

#DELETE PROJECT
@login_required(login_url="login")
def deleteEvent(request, pk):
    organizer = request.user.eventorganizer
    event = organizer.event_set.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('organization-account')
    context = {'object': event}
    return render (request, 'main/delete_template.html', context)









from datetime import timedelta

def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    #calculate the event duration
    duration = event.end_date - event.date
    total_seconds = duration.total_seconds()
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        duration_str = "{} day(s) {} hour(s)".format(int(days), int(hours))
    else:
        duration_str = "{} hour(s) {} minute(s)".format(int(hours), int(minutes))

    context = {
        'event': event,
        'duration': duration_str,
    }
    return render(request, 'event/event_detail.html', context)

#Organizer Profile
def organizerProfile(request, pk):
    organization = get_object_or_404(EventOrganizer, id=pk)
    events = organization.event_set.all()

    context = {
        'profile': organization, 
        'events': events
        }
    
    return render(request, 'event/organizer_profile.html', context)