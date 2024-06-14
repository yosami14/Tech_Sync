from django.shortcuts import render,redirect
from .models import Room, Topic
from .forms import RoomForm
def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
        # 'topics': topics,
    }
    return render(request, 'group/home.html',context)

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


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
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

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home-group')
    context = {'object': room}
    return render (request, 'main/delete_template.html', context)
