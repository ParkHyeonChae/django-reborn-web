from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import auth_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View
# from django.contrib.auth.views import PasswordResetConfirmView
from .models import User
from .forms import CsRegisterForm, RegisterForm, LoginForm, CustomUserChangeForm, CheckPasswordForm, RecoveryIdForm, RecoveryPwForm, CustomSetPasswordForm
from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .helper import send_mail, email_auth_num
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.forms.utils import ErrorList

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator


def index(request):
    return render(request, 'users/index.html')

def register_success(request):
    return render(request, 'users/register_success.html')

def register_info_view(request):
    return render(request, 'users/register_info.html')

# def cs_register_view(request):
#     if request.method == 'POST':
#         register_form = CsRegisterForm(request.POST)

#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.set_password(register_form.cleaned_data['password'])
#             user.level = '2'
#             user.department = '컴퓨터공학부'
#             user.save()
#             messages.success(request, "회원가입 성공.")
#             return redirect('users:login')
#     else:
#         register_form = CsRegisterForm()

#     return render(request, 'users/register_cs.html', {'register_form':register_form})

# def register_view(request):
#     if request.method == 'POST':
#         register_form = RegisterForm(request.POST)

#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.set_password(register_form.cleaned_data['password'])
#             user.level = '3'
#             user.save()
#             messages.success(request, "회원가입 성공.")
#             return redirect('users:login')
#     else:
#         register_form = RegisterForm()

#     return render(request, 'users/register.html', {'register_form':register_form})

#----------------------------------------------------------------------------------------------
# 회원가입 뷰 수정 TEST


class CsRegisterView(CreateView):
    model = User
    template_name = 'users/register_cs.html'
    form_class = CsRegisterForm

    def get(self, request, *args, **kwargs):
        url = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated:
            if url == request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        # messages.success(self.request, "회원가입 성공.")
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        # return settings.LOGIN_URL
        return reverse('users:register_success')

    def form_valid(self, form):
        self.object = form.save()

        # 회원가입 인증 메일 발송
        # ISSUE - https 통신오류 -> http 프로토콜 수정
        send_mail(
            '[인제대학교 컴퓨터공학부 RE:BORN] {}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('users/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())

class RegisterView(CsRegisterView):
    template_name = 'users/register.html'
    form_class = RegisterForm


# 이메일 인증 활성화 뷰
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('users:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('users:login')


 #------------------------------------------------------------------------------------------------       

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

    if result_pw:
        auth_num = email_auth_num()
        result_pw.auth = auth_num 
        result_pw.save()

        send_mail(
            '[인제대학교 컴퓨터공학부 RE:BORN] 비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('users/recovery_email.html', {
                'auth_num': auth_num,
            }),
        )
    print(auth_num)
    return HttpResponse(json.dumps({"result": result_pw.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")


def auth_confirm_view(request):
    # if request.method=='POST' and 'auth_confirm' in request.POST:
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    user = User.objects.get(user_id=user_id, auth=input_auth_num)
    # login(request, user)
    user.auth = ""
    user.save()
    request.session['auth'] = user.user_id  
    
    return HttpResponse(json.dumps({"result": user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

        # try:
        #     user = User.objects.get(auth=input_auth_num)
        #     return render(request, 'users/password_reset.html')
        # except ObjectDoesNotExist:
        #     error = "인증번호가 일치하지 않습니다."
        #     # messages.info(request, "인증번호가 일치하지 않습니다.")
        #     return HttpResponse(error)
        #     # return render(request, 'users/recovery.html')

        # password_change_form = PasswordChangeForm(request.user, request.POST)
        # return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})



# class AuthPwResetView(ForView):
#     success_url = 'users:login'
#     template_name = 'users/password_reset.html'
#     form_class = CustomSetPasswordForm

#     def form_valid(self, form):
#         messages.info(self.request, '비밀번호를 변경 하였습니다.')
#         return super().form_valid(form)

def auth_pw_reset_view(request):
    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(user_id=session_user)
        # del(request.session['auth'])
        login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)
        
        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('users:login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'users/password_reset.html', {'form':reset_password_form})

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
    #     if request.method=='POST' and 'auth_confirm' in request.POST:
    #         user_id = request.POST.get('user_id')
    #         name = request.POST.get('name')
    #         email = request.POST.get('email')
    #         print(user_id)
    #         print(name)
    #         print(email)
    #         # user = authenticate(self.request, username=user_id, password=password)
    #         # if user is not None:
    #         #     login(self.request, user)
    #         password_change_form = PasswordChangeForm(request.user, request.POST)
    #         return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})

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
            self.request.session['user_id'] = user_id
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