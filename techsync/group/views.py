from django.shortcuts import render,redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'group/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    chats = room.message_set.all()
    context = {
        'room': room,
        'participants': participants,
        'chats': chats,
    }
    return render(request, 'group/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-group')

    context = {
        'form': form,
        }
    return render(request, 'group/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed to view this page.')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home-group')


    context = {
        'room': room,
        'form': form,
        }
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
