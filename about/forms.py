from django import forms
from .models import Organization, Circles, Labs


class OrganizationAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'placeholder': '이름',
            'class': 'form-control',
        })
        self.fields['part'].label = '부서'
        self.fields['part'].widget.attrs.update({
            'placeholder': '부서',
            'class': 'form-control',
        })
        self.fields['rank'].label = '직위'
        self.fields['rank'].widget.attrs.update({
            'placeholder': '직위',
            'class': 'form-control',
        })

    class Meta:
        model = Organization
        fields = ['name', 'part', 'rank']


class CirclesEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CirclesEditForm, self).__init__(*args, **kwargs)
        # self.fields['circles_name'].label = '동아리이름'
        # self.fields['circles_name'].widget.attrs.update({
        #     'placeholder': '동아리이름',
        #     'class': 'form-control',
        # })
        self.fields['introduce'].label = '동아리소개'
        self.fields['introduce'].widget.attrs.update({
            'placeholder': '동아리소개를 작성해주세요',
            'class': 'md-textarea form-control circlesIntroduce',
            'autofocus': 'autofocus',
        })

    class Meta:
        model = Circles
        fields = ['introduce',]


class LabsEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LabsEditForm, self).__init__(*args, **kwargs)
        self.fields['location'].label = '연구실위치'
        self.fields['location'].widget.attrs.update({
            'placeholder': '연구실위치',
            'class': 'form-control',
        })
        self.fields['introduce'].label = '연구실소개'
        self.fields['introduce'].widget.attrs.update({
            'placeholder': '연구실소개를 작성해주세요',
            'class': 'md-textarea form-control circlesIntroduce',
            'autofocus': 'autofocus',
        })

    class Meta:
        model = Labs
        fields = ['location', 'introduce',]
