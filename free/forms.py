from django import forms
from .models import Free


class FreeWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FreeWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
            'style': "width: 91%;"
        })
        self.fields['category'].label = '분류'
        self.fields['category'].widget.attrs.update({
            'class': 'custom-select custom-select-md',
            'style': "width: 8%; float:left; margin-right:1%"
        })

    class Meta:
        model = Free
        fields = ['category', 'title', 'content', 'upload_files']