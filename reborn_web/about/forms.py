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
