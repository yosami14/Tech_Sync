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
from .utils import  paginateEvents, get_event_search_results
from users.decorators import event_organizer_only

# Create your views here.

# event list
def events(request):
    search_query = request.GET.get('search_query', '')
    events = get_event_search_results(search_query)
    custom_range, events = paginateEvents(request, events,3 )
    context = {
        'events': events,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'event/events.html', context)






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
        'events': events,
        
        }
    
    return render(request, 'event/organizer_profile.html', context)


from django.core.mail import send_mail
from django.conf import settings

from urllib.parse import urlencode, quote
from urllib.parse import quote_plus
from django.urls import reverse
from django.utils import timezone
from .models import EventRegistration

import qrcode
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.utils import timezone
from io import BytesIO
from urllib.parse import urlencode, quote_plus

@login_required
def registerForEvent(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if EventRegistration.objects.filter(event=event, attendee=request.user).exists():
            messages.info(request, "You are already registered for this event.")
        elif event.attendees_limit <= 0:
            messages.info(request, "This event is full.")
        else:
            # Get additional fields from the form
            full_name = request.POST.get('text')
            email = request.POST.get('email')
            send_email = request.POST.get('send_email')
            google_calendar = request.POST.get('google_calendar')

            # Create an EventRegistration instance
            registration = EventRegistration.objects.create(event=event, attendee=request.user, registration_date=timezone.now())
            event.attendees_limit -= 1
            event.save()
            messages.success(request, "You have successfully registered for the event.")

            # Generate QR code with EventRegistration data
            qr_data = f"Event: {event.title}\nAttendee: {registration.attendee.username}\nRegistration ID: {registration.id}"
            qr_image = qrcode.make(qr_data)
            qr_buffer = BytesIO()
            qr_image.save(qr_buffer, format='PNG')
            qr_image_file = ContentFile(qr_buffer.getvalue(), 'event_qr_code.png')

            # Google Calendar link
            if google_calendar:
                event_details = {
                    'action': 'TEMPLATE',
                    'text': event.title,
                    'dates': f'{event.date.strftime("%Y%m%dT%H%M%S")}/{event.end_date.strftime("%Y%m%dT%H%M%S")}',
                    'location': f'https://www.google.com/maps/search/?api=1&query={quote_plus(event.venue_name)}',
                    'details': request.build_absolute_uri(reverse('event-detail', args=[event.pk])),
                }
                google_calendar_url = f'https://www.google.com/calendar/render?{urlencode(event_details)}'
                calendar_message = f"Add this event to your Google Calendar: {google_calendar_url}\n\n"
            else:
                calendar_message = ""

            # Email setup
            email_message = f"""
            Dear {full_name},

            Congratulations! You have successfully registered for the event: {event.title}.

            Event Details:
            Date: {event.date.strftime("%Y-%m-%d")}
            Time: {event.date.strftime("%H:%M")}
            Venue: {event.venue_name}

            {calendar_message}
            Here is your QR code for event entry:
            """
            email = EmailMessage(
                subject='Event Registration',
                body=email_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            email.attach('event_qr_code.png', qr_image_file.read(), 'image/png')

            if send_email:
                email.send(fail_silently=False)

        return redirect('event-detail', pk=event.pk)
    return redirect('event-detail', pk=event.pk)





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventRegistration

@event_organizer_only
def scanQrCode(request):
    context = {}
    scanned_data = None

    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')

        if qr_data:
            scanned_data = qr_data
            try:
                # Extract the registration ID from the QR code data
                registration_id = qr_data.split('Registration ID: ')[1].strip()

                # Check if the registration exists
                registration = EventRegistration.objects.get(id=registration_id)
                attendee = registration.attendee  # Get the associated attendee

                # Add attendee details to context
                context['attendee'] = {
                    'username': attendee.username,
                    'full_name': attendee.profile.name,
                    'email': attendee.email,
                    'profile_picture': attendee.profile.profile_image.url if attendee.profile.profile_image else None,
                    'registration_date': registration.registration_date,
                    'has_attended': registration.has_attended,
                }

                if not registration.has_attended:
                    # Mark as attended
                    registration.has_attended = True
                    registration.save()
                    messages.success(request, "Attendance marked successfully.")
                    context['attendance_status'] = "Success Valid ID Registration ID: {}".format(registration_id)
                else:
                    messages.info(request, "You have already marked attendance for this registration.")
                    context['attendance_status'] = "ID already marked for Registration ID: {}".format(registration_id)

            except (EventRegistration.DoesNotExist, IndexError):
                messages.error(request, "Invalid QR code or registration not found.")
                context['attendance_status'] = "Invalid QR code or registration not found."

    context['scanned_data'] = scanned_data

    return render(request, 'event/verify_attendee.html', context)




from django.db.models import Count
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Event, EventRegistration

def event_analytics(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = EventRegistration.objects.filter(event=event)

    attendee_count = registrations.count()
    
    # Prepare data for Chart.js with formatted date
    event_dates = (
        EventRegistration.objects
        .filter(event=event)
        .values('registration_date__date')
        .annotate(count=Count('id'))
        .order_by('registration_date__date')
    )

    # Convert to a list of dictionaries for JSON serialization
    event_dates_list = [
        {
            'date': date['registration_date__date'].strftime('%Y-%m-%d'),  # Format the date
            'count': date['count']
        }
        for date in event_dates
    ]

    context = {
        'event': event,
        'registrations': registrations,
        'attendee_count': attendee_count,
        'event_dates': event_dates_list,  # Pass the formatted data to the template
    }

    return render(request, 'event/event_analytics.html', context)


