from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from .models import User
from .forms import CsRegisterForm, RegisterForm, LoginForm, CustomUserChangeForm, CheckPasswordForm, RecoveryIdForm, RecoveryPwForm
from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


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

def register_info_view(request):
    return render(request, 'users/register_info.html')

def cs_register_view(request):
    if request.method == 'POST':
        register_form = CsRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.level = '2'
            user.department = '컴퓨터공학부'
            user.save()
            messages.success(request, "회원가입 성공.")
            return redirect('users:login')
    else:
        register_form = CsRegisterForm()

    return render(request, 'users/register_cs.html', {'register_form':register_form})

def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.level = '3'
            user.save()
            messages.success(request, "회원가입 성공.")
            return redirect('users:login')
    else:
        register_form = RegisterForm()

    return render(request, 'users/register.html', {'register_form':register_form})

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

# @login_required
# def profile_delete_view(request):  # form 안쓰고 회원탈퇴 구현
#     if request.method == 'POST':
#         password_form = CheckPasswordForm(request.POST)
#         password = request.user.password

#         if password_form.is_valid():
#             confirm_password = password_form.cleaned_data.get('password')
#             check_pw = check_password(confirm_password, password)

#             if check_pw:
#                 request.user.delete()
#                 logout(request)
#                 return redirect('/')
#             else:
#                 pass
#     else:
#         password_form = CheckPasswordForm()

#     return render(request, 'users/profile_delete.html', {'password_form':password_form})


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴 완료.")
            return redirect('/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'users/profile_delete.html', {'password_form':password_form})

@login_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            # logout(request)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('users:profile')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)
       
    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")    

def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_pw = User.objects.get(user_id=user_id, name=name, email=email)
       
    return HttpResponse(json.dumps({"result_pw": result_pw.password}, cls=DjangoJSONEncoder), content_type = "application/json")    

class RecoveryView(View):
    template_name = 'users/recovery.html'
    recovery_id = RecoveryIdForm
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form_id = self.recovery_id(None)
            form_pw = self.recovery_pw(None)
            return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw })
    
    # def post(self, request):
    #     form_id = self.recovery_id(None)
    #     form_pw = self.recovery_pw(None)

    #     if request.method=='POST' and 'recovery_id' in request.POST:
    #         name = request.POST.get('name')
    #         email = request.POST.get('email')
    #         try:
    #             result_id = User.objects.get(name=name, email=email)
                
    #             return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw, 'result_id':result_id.user_id })
    #         except ObjectDoesNotExist:
    #             messages.info(request, "이름 또는 이메일이 일치하지 않습니다.")

    #             return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw }) 

        # if request.method=='POST' and 'recovery_pw' in request.POST:
        #     user_id = request.POST.get('user_id')
        #     name = request.POST.get('name')
        #     email = request.POST.get('email')
        #     try:
        #         result_pw = User.objects.get(user_id=user_id, name=name, email=email)
        #         messages.success(request, "회원님의 이메일로 인증코드를 발송하였습니다.")

        #         return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw, 'result_pw':result_pw.password })
        #     except ObjectDoesNotExist:
        #         messages.info(request, "아이디 또는 회원정보가 일치하지 않습니다.")

        #         return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw })

        # return render(request, self.template_name, { 'form_id':form_id, 'form_pw':form_pw, 'result_id':result_id })

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

            # Session Maintain Test

            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

            # try:
            #     remember_session = self.request.POST['remember_session']
            #     if remember_session:
            #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            # except MultiValueDictKeyError:
            #     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            
        return super().form_valid(form)


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