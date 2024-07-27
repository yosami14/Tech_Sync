# decorators.py

# decorators.py

from django.shortcuts import redirect
from django.shortcuts import redirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def redirect_based_on_role(user):
    if user.is_authenticated:
        if user.is_superuser:  # Django's built-in admin check
            return redirect('/admin-charts/')
        elif user.is_event_organizer:  # Your custom event organizer check
            return redirect('/event')
        else:
            return redirect('profiles')  # or wherever you want normal users to go
    else:
        return redirect('')  # or wherever you want unauthenticated users to go
    




def admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def event_organizer_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_event_organizer:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def event_organizer_or_admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_event_organizer or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
