from django.shortcuts import redirect
from .models import User

def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user_id')

        if user is None or not user:
            return redirect('/users/login')
        return function(request, *args, **kwargs)

    return wrap