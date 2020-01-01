from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import User

def index(request):
    return render(request, 'users/index.html', { 'user_id': request.session.get('user_id') })

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user_id'] = form.data.get('user_id')

        return super().form_valid(form)

def logout(request):
    if 'user_id' in request.session:
        del(request.session['user_id'])

    return redirect('/')