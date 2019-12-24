from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import User


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/login'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('id')

        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')