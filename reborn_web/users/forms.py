from django import forms
from django.contrib.auth.hashers import check_password
from .models import User

class RegisterForm(forms.Form):
    user_id = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=64, label='아이디'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            idCheck = User.objects.filter(user_id=user_id).exists()
            if idCheck == False:
                if password != re_password:
                    self.add_error('password', '비밀번호가 서로 다릅니다.')
                    self.add_error('re_password', '비밀번호가 서로 다릅니다.')
            else:
                self.add_error('user_id', '이미 존재하는 아아디입니다.')
                
class LoginForm(forms.Form):
    user_id = forms.CharField(
        error_messages={
            'required': '아이디을 입력해주세요.'
        },
        max_length=64, label='아이디'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
               user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 없습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')