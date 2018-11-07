from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def required_admin(func):
    def decorated(request, *args, **kwargs):
        # print (request.session['id_user'])
        if 'admin' not in request.session:
            return redirect('login2')
        else:
            return func(request, *args, **kwargs)
    # decorated.__doc__ = func.__doc__
    # decorated.__name__ = func.__name__
    return decorated

def required_client(func):
    def decorated(request, *args, **kwargs):
        # print (request.session['id_user'])
        if 'admin' not in request.session:
            return redirect('fr_login')
        else:
            return func(request, *args, **kwargs)
    # decorated.__doc__ = func.__doc__
    # decorated.__name__ = func.__name__
    return decorated

