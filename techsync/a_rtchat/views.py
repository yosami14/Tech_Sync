from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404
from .models import *
from .forms import *
# Create your views here

@login_required(login_url='login')
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    # check if the chat is private
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    # if request.htmx:
    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,

            }
            return render(request,'a_rtchat/partial/chat_message_p.html',context)
        
    context = {
        # 'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        
    }
    return render(request, 'a_rtchat/chat.html',context)


# private chat

@login_required(login_url='login')
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)
   
    chatroom = ChatGroup.objects.create(is_private = True)
    chatroom.members.add(other_user, request.user)   
    return redirect('chatroom', chatroom.group_name)


@login_required(login_url='login')
def view_user_chatrooms(request):
    chatrooms = request.user.chat_groups.all()
    return render(request, 'a_rtchat/inbox.html', {'chatrooms': chatrooms})