from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model

# ModelForm Test

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': '비밀번호를 입력주세요.'}),  
    )
    confirm_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': '비밀번호를 다시 입력주세요.'}),  
    )

    class Meta:
        model = User
        fields = ['user_id', 'password', 'confirm_password', 'email', 'hp', 'name', 'student_id', 'grade']

        widgets = {
            'user_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '로그인과 사이트 활동에 사용할 아이디를 입력주세요.',}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': '비밀번호 분실 시 사용될 이메일을 입력해주세요.'}
            ),
            'hp': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '하이픈(-)을 제외한 번호를 입력해주세요.'}
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '각종 행사 참여를 위해 실명을 입력해주세요.'}
            ),
            'student_id': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '학번을 입력주세요.'}
            ),
            'grade': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
    
    def clean_confirm_password(self):
        pw_check = self.cleaned_data
        if pw_check['password'] != pw_check['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

        return pw_check['confirm_password']

    # def phonenumber_valid(self):
    #     number = self.cleaned_data
    #     if len(number['hp']) != 11:
    #         raise forms.ValidationError('핸드폰번호 11자리를 입력해주세요.')

    #     return number['hp']

    # def stdnumber_valid(self):
    #     std_number = self.cleaned_data['student_id']
    #     if len(str(std_number)) != 8:
    #         raise forms.ValidationError('학번 8자리를 입력해주세요.')

    #     return std_number

#--------------------------------------------------------#

# def phonenumber_valid(value):
#     if len(str(value)) != 11:
#         raise forms.ValidationError('핸드폰번호 11자리를 입력해주세요.')

# def stdnumber_valid(value):
#     if len(str(value)) != 8:
#         raise forms.ValidationError('학번 8자리를 입력해주세요.')

# class RegisterForm(forms.Form):
#     user_id = forms.CharField(
#         error_messages={
#             'required': '아이디를 입력해주세요.'
#         },
#         max_length=64, label='아이디', initial='로그인과 사이트 활동에 사용할 아이디를 입력주세요.'
#     )
#     password = forms.CharField(
#         error_messages={
#             'required': '비밀번호를 입력해주세요.'
#         },
#         widget=forms.PasswordInput, label='비밀번호', initial='비밀번호를 입력주세요.'
#     )
#     re_password = forms.CharField(
#         error_messages={
#             'required': '비밀번호를 입력해주세요.'
#         },
#         widget=forms.PasswordInput, label='비밀번호 확인', initial='비밀번호를 다시 입력해주세요.'
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput, max_length=128, label='이메일', initial='비밀번호 분실 시 사용될 이메일을 입력해주세요.'
#     )
#     hp = forms.IntegerField(
#         label='핸드폰번호', initial='하이픈(-)을 제외한 번호를 입력해주세요.', validators=[phonenumber_valid]
#     )
#     name = forms.CharField(
#         label='이름', initial='각종 행사 참여를 위해 실명을 입력해주세요.'
#     )
#     student_id = forms.IntegerField(
#         label='학번', initial='학번을 입력주세요.', validators=[stdnumber_valid]
#     )
#     GRADE_CHOICES = (("1", "1학년"),("2", "2학년"),("3", "3학년"),("4", "4학년"),("졸업", "졸업생"),)
#     grade = forms.ChoiceField(choices=GRADE_CHOICES, label='학년', initial='학년은 숫자만, 졸업생이시면 "졸업"을 입력하세요.')
    
#     # required=False 하면 빈칸 입력 가능

#     # 중복가입방지를 폰으로할까 이메일로할까


#     def clean(self):
#         cleaned_data = super().clean()
#         user_id = cleaned_data.get('user_id')
#         password = cleaned_data.get('password')
#         re_password = cleaned_data.get('re_password')
#         email = cleaned_data.get('email')
#         hp = cleaned_data.get('hp')
#         name = cleaned_data.get('name')
#         student_id = cleaned_data.get('student_id')
#         grade = cleaned_data.get('grade')

#         if password and re_password:
#             idCheck = User.objects.filter(user_id=user_id).exists()
#             if idCheck == False:
#                 if password != re_password:
#                     self.add_error('password', '비밀번호가 서로 다릅니다.')
#                     self.add_error('re_password', '비밀번호가 서로 다릅니다.')
#             else:
#                 self.add_error('user_id', '이미 존재하는 아아디입니다.')
                
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
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['email', 'hp', 'name', 'student_id', 'grade']

class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')