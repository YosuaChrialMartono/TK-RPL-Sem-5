from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import friendRequest
from authuser.models import User

def user_required(login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def friend_request_recipient(login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            friend_username = kwargs['username']
            friend = User.objects.get(username=friend_username)
            friend_request = friendRequest.objects.filter(user=friend, friend=request.user)
            if friend_request is not None and friend_request[0].friend == request.user:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator

def is_current_user(login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            username = kwargs['username']
            if request.user.username == username:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator