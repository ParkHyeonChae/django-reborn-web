from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, SetPasswordForm, UserCreationForm
from django.contrib.auth import get_user_model
from .choice import *

# ModelForm Test

# class CsRegisterForm(forms.ModelForm):
#     password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
#       attrs={'class': 'form-control', 'placeholder': '비밀번호를 입력주세요.'}),
#     )
#     confirm_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
#       attrs={'class': 'form-control', 'placeholder': '비밀번호를 다시 입력주세요.'}),  
#     )

#     class Meta:
#         model = User
#         fields = ['user_id', 'password', 'confirm_password', 'email', 'hp', 'name', 'student_id', 'grade', 'circles']

#         widgets = {
#             'user_id': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': '로그인과 사이트 활동에 사용할 아이디를 입력주세요.',}
#             ),
#             'email': forms.EmailInput(
#                 attrs={'class': 'form-control', 'placeholder': '비밀번호 분실 시 사용될 이메일을 입력해주세요.'}
#             ),
#             'hp': forms.NumberInput(
#                 attrs={'class': 'form-control', 'placeholder': '하이픈(-)을 제외한 번호를 입력해주세요.'}
#             ),
#             'name': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': '각종 행사 참여를 위해 실명을 입력해주세요.'}
#             ),
#             'student_id': forms.NumberInput(
#                 attrs={'class': 'form-control', 'placeholder': '학번을 입력해주세요.'}
#             ),
#             'grade': forms.Select(
#                 attrs={'class': 'form-control'}
#             ),
#             'circles': forms.Select(
#                 attrs={'class': 'form-control'}
#             ),
#         }
    
#     def clean_confirm_password(self):
#         pw_check = self.cleaned_data
#         if pw_check['password'] != pw_check['confirm_password']:
#             raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

#         return pw_check['confirm_password']

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

# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': '비밀번호를 입력주세요.'}),  
#     )
#     confirm_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': '비밀번호를 다시 입력주세요.'}),  
#     )
#     student_id = forms.IntegerField(required=False, label='학번 (선택사항)', widget=forms.NumberInput(
#         attrs={'class': 'form-control', 'placeholder': '학번을 입력해주세요.'}), 
#     )
#     grade = forms.ChoiceField(choices=GRADE_CHOICES, label='학년 (선택사항)', widget=forms.Select(
#         attrs={'class': 'form-control'}),
#     )
#     department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label='학과 (선택사항)', widget=forms.Select(
#         attrs={'class': 'form-control'}),
#     )

#     class Meta:
#         model = User
#         fields = ['user_id', 'password', 'confirm_password', 'email', 'hp', 'name', 'student_id', 'grade', 'department']

#         widgets = {
#             'user_id': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': '로그인과 사이트 활동에 사용할 아이디를 입력주세요.',}
#             ),
#             'email': forms.EmailInput(
#                 attrs={'class': 'form-control', 'placeholder': '비밀번호 분실 시 사용될 이메일을 입력해주세요.'}
#             ),
#             'name': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': '각종 행사 참여를 위해 실명을 입력해주세요.'}
#             ),
#             'hp': forms.NumberInput(
#                 attrs={'class': 'form-control', 'placeholder': '하이픈(-)을 제외한 번호를 입력해주세요.'}
#             ),
#             # 'grade': forms.Select(
#             #     attrs={'class': 'form-control'}
#             # ),
#             # 'department': forms.Select(
#             #     attrs={'class': 'form-control'}
#             # ),
#         }
    
#     def clean_confirm_password(self):
#         pw_check = self.cleaned_data
#         if pw_check['password'] != pw_check['confirm_password']:
#             raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

#         return pw_check['confirm_password']

                
class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={
            'required': '아이디을 입력해주세요.'
        },
        max_length=32,
        label='아이디'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        label='비밀번호'
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
    name = forms.CharField(required=False, label='이름', widget=forms.TextInput)        
    student_id = forms.IntegerField(required=False, label='학번', widget=forms.NumberInput)
    grade = forms.ChoiceField(choices=GRADE_CHOICES, label='학년', widget=forms.Select)
       
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

class RecoveryIdForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
    )

    class Meta:
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'placeholder': '이름을 입력해주세요',
            'class': 'form-control',
            'id': 'form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'placeholder': '이메일을 입력해주세요',
            'class': 'form-control',
            'id': 'form_email' 
        })


class RecoveryPwForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput,
    )
    name = forms.CharField(
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
    )
    class Meta:
        fields = ['user_id', 'name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'placeholder': '아이디을 입력해주세요',
            'class': 'form-control',
            'id': 'pw_form_id',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'placeholder': '이름을 입력해주세요',
            'class': 'form-control',
            'id': 'pw_form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'placeholder': '이메일을 입력해주세요',
            'class': 'form-control',
            'id': 'pw_form_email',
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '새 비밀번호',
        })
        self.fields['new_password2'].label = '비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '새 비밀번호 확인',
        })

#--------------------------------------------------------------------------------------------
# 회원가입 test

class CsRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CsRegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            # 'class': 'form-control col-sm-10',
            'class': 'form-control',
            # 'placeholder': '아이디를 입력해주세요.',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '비밀번호를 입력해주세요.',
        })
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '비밀번호를 다시 입력해주세요.',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '회원가입 후 입력하신 메일로 본인인증 메일이 전송됩니다.',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': "아이디, 비밀번호 찾기에 이용됩니다.",
        })
        self.fields['hp'].label = '핸드폰번호'
        self.fields['hp'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': "'-'를 제외한 숫자로 입력해주세요",
        })
        self.fields['grade'].label = '학년'
        self.fields['grade'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['student_id'].label = '학번'
        self.fields['student_id'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': "학번을 입력해주세요.",
        })
        self.fields['circles'].label = '학술동아리'
        self.fields['circles'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'email', 'name', 'hp', 'grade', 'student_id', 'circles']

    def save(self, commit=True):
        user = super(CsRegisterForm, self).save(commit=False)
        user.level = '2'
        user.department = '컴퓨터공학부'
        user.is_active = False
        user.save()

        return user


class RegisterForm(UserCreationForm):
    student_id = forms.IntegerField(required=False, label='학번', widget=forms.NumberInput(
        attrs={'class': 'form-control',}), 
    )
    grade = forms.ChoiceField(choices=GRADE_CHOICES, label='학년', widget=forms.Select(
        attrs={'class': 'form-control'}),
    )
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label='학과', widget=forms.Select(
        attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            # 'class': 'form-control col-sm-10',
            'class': 'form-control',
            'autofocus': False,
            # 'placeholder': '아이디를 입력해주세요.',
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '비밀번호를 입력해주세요.',
        })
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '비밀번호를 다시 입력해주세요.',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': '회원가입 후 입력하신 메일로 본인인증 메일이 전송됩니다.',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': "아이디, 비밀번호 찾기에 이용됩니다.",
        })
        self.fields['hp'].label = '핸드폰번호'
        self.fields['hp'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': "'-'를 제외한 숫자로 입력해주세요",
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'email', 'name', 'hp', 'department', 'grade', 'student_id']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.level = '3'
        user.is_active = False
        user.save()

        return user
