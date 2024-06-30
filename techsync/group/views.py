from django.shortcuts import render,redirect,get_object_or_404
from .models import Room, Topic,Message
from users.models import User, Profile
from .forms import RoomForm,ChatRoomEditForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages


from django.db.models.functions import Lower

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q = q.lower()  # convert query to lowercase
    rooms = Room.objects.annotate(
        lower_topic=Lower('topic__name'),
        lower_name=Lower('name'),
        lower_description=Lower('description')
    ).filter(
        Q(lower_topic__icontains=q) |
        Q(lower_name__icontains=q) |
        Q(lower_description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'group/home.html', context)


# @login_required(login_url='login')
# def room(request, pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all()
#     participants = room.participants.all()

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user=request.user,
#             room=room,
#             body=request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room', pk=room.id)

#     context = {'room': room, 'room_messages': room_messages,
#                'participants': participants}
#     return render(request, 'group/room.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        context = {
            'message': message,
            'room': room,
            'request': request, 
        }
        return render(request, 'group/partial/room_messages_p.html', context)
    if room.name:
        if request.user not in room.participants.all():
            room.participants.add(request.user)
            
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'group/room.html', context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home-group')

    context = {
        'form': form,
        'topics': topics,
        }
    return render(request, 'group/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home-group')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'group/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to view this page.')
    if request.method == 'POST':
        room.delete()
        return redirect('home-group')
    context = {'object': room}
    return render (request, 'main/delete_template.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room_id = message.room.id  # get the id of the room
        message.delete()
        return redirect('room', pk=room_id)  # redirect to the room

    context = {'object': message}
    return render(request, 'main/delete_template.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'group/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'group/activity.html', {'room_messages': room_messages})


# def userProfile(request, pk):
#     user = User.objects.get(id=pk)
#     rooms = user.room_set.all()
#     room_messages = user.message_set.all()
#     topics = Topic.objects.all()
#     context = {'user': user, 'rooms': rooms,
#                'room_messages': room_messages, 'topics': topics}
#     return render(request, 'base/profile.html', context)


#Manage users




@login_required(login_url='login')
def manage_group(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        raise Http404()
    
    form = ChatRoomEditForm(instance=room) 
    
    if request.method == 'POST':
        remove_members = request.POST.getlist('remove_members')
        for member_id in remove_members:
            member = User.objects.get(id=member_id)
            room.participants.remove(member)  
                
        return redirect('room', pk=room.id) 
    
    context = {
        'room' : room
    }   
    return render(request, 'group/room_manage_group.html', context)

@login_required(login_url='login')
def leave_group(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user not in room.participants.all():
        raise Http404()

    if request.method == 'POST':
        room.participants.remove(request.user)
        messages.success(request, "You left the chat")
        return redirect('home-group')  # redirect to the room

    context = {'object': room}
    return render(request, 'main/delete_template.html', context)


# FILE UPLOAD
def room_file_upload(request, pk):
    room = get_object_or_404(Room, id=pk)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = Message.objects.create(
            file = file,
            user = request.user, 
            room = room,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'chat_message',
            'message': str(message.id),  # convert UUID to string
        }
        async_to_sync(channel_layer.group_send)(
            pk, 
            event
        )
    
    context = {'room': room, 'message': message}  # Add your context here
    html = render_to_string("group/partial/room_messages_p.html", context)
    return HttpResponse(html)