from django.shortcuts import redirect
from .models import User
from django.http import HttpResponse

def auth_required(function):
    def wrap(request, *args, **kwargs):

        session_user = request.session.get('user_id')
        user = User.objects.get(user_id=session_user)
 
        if user.level != '0':
            return HttpResponse('접근 제한')

        return function(request, *args, **kwargs)

    return wrap