from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import User

def index(request):
    return render(request, 'users/index.html', { 'user_id': request.session.get('user_id') })

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            user_id = form.data.get('user_id'),
            password = make_password(form.data.get('password')),
            email = form.data.get('email'),
            hp = form.data.get('hp'),
            name = form.data.get('name'),
            student_id = form.data.get('student_id'),
            grade = form.data.get('grade'),
            level = '2'
        )
        user.save()

        return super().form_valid(form)

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