# decorators.py

# decorators.py

from django.shortcuts import redirect
from django.shortcuts import redirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
def redirect_based_on_role(user):
    if user.is_authenticated:
        if user.is_superuser: 
            return redirect('/admin-charts/')
        elif user.is_event_organizer: 
            return redirect('/event')
        else:
            return redirect('profiles') 
    else:
        return redirect('/login')  
    



from django.shortcuts import redirect

def admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not allowed to access this page.')
            return redirect('error403')  # or your custom error page
    return _wrapped_view

def event_organizer_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_event_organizer:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not allowed to access this page.')
            return redirect('error403')  # or your custom error page
    return _wrapped_view

def event_organizer_or_admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_event_organizer or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not allowed to access this page.')
            return redirect('error403')  # or your custom error page
    return _wrapped_view
