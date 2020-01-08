from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm, CustomUserChangeForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'users/index.html')

# class RegisterView(FormView):
#     template_name = 'users/register.html'
#     form_class = RegisterForm
#     success_url = '/'

#     def form_valid(self, form):
#         user = User(
#             user_id = form.data.get('user_id'),
#             password = make_password(form.data.get('password')),
#             email = form.data.get('email'),
#             hp = form.data.get('hp'),
#             name = form.data.get('name'),
#             student_id = form.data.get('student_id'),
#             grade = form.data.get('grade'),
#             level = '2'
#         )
#         user.save()

#         return super().form_valid(form)

def register_view(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.level = 2
            user.save()
            return redirect('users:login')
    else:
        user_form = RegisterForm()

    return render(request, 'users/register.html', {'user_form':user_form})

@login_required
def profile_view(request):
    if request.method == 'GET':

        return render(request, 'users/profile.html')

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        # user_form = RegisterForm(request.POST)
        user_change_form = CustomUserChangeForm(request.POST, instance = request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            # return redirect('users:profile')
            return render(request, 'users/profile.html')
    else:
        user_change_form = CustomUserChangeForm(instance = request.user)    
        return render(request, 'users/profile_update.html', {'user_change_form':user_change_form})

@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/')
    return render(request, 'users/profile_delete.html')

# class LoginView(FormView):
#     template_name = 'users/login.html'
#     form_class = LoginForm
#     success_url = '/'

#     def form_valid(self, form):
#         self.request.session['user_id'] = form.data.get('user_id')

#         return super().form_valid(form)

# def logout_view(request):
#     if 'user_id' in request.session:
#         del(request.session['user_id'])

#     return redirect('/')

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# def login_view(request):
#     if request.method == 'POST':
#         login_form = AuthenticationForm(request, request.POST)  
        
#         if login_form.is_valid():
#             login(request, login_form.get_user())
#             return render(request, 'users/index.html')
#     else:
#         login_form = LoginForm()
    
#     return render(request, 'users/login.html', {'login_form' : login_form})

def logout_view(request):
    logout(request)
    return redirect('/')