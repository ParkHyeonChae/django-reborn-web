from django import forms
from .models import Notice


class NoticeWriteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NoticeWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })
        self.fields['content'].label = '내용'
        self.fields['content'].widget.attrs.update({
            'placeholder': '내용을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_content',
            'rows': 15,
        })

    class Meta:
        model = Notice
        fields = ['title', 'content']

        