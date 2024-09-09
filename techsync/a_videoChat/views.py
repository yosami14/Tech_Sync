from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'conference/dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    return render(request, 'conference/videocall.html', {'name': request.user.first_name })

# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect("/login")

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        # Use an absolute path for redirection
        return redirect("/conference/meeting?roomID=" + roomID)
    return render(request, 'conference/joinroom.html')
