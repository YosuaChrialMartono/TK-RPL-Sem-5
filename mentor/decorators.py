from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def mentor_required(login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            elif request.user.role != '1':
                return HttpResponseForbidden()
            try:
                request.user.mentor
            except:
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator