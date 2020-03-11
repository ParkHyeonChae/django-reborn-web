from django import forms
from .models import Anonymous


class AnonymousWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnonymousWriteForm, self).__init__(*args, **kwargs)
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
            'class': 'md-textarea form-control',
            'id': 'form_content',
            'style': 'padding:0',
        })
        self.fields['image_files'].label = '사진 첨부'
        self.fields['image_files'].widget.attrs.update({
            'id': 'id_image_files',
            # 'style': 'display:none;'
            'aria-describedby':'help'
        })

    class Meta:
        model = Anonymous
        fields = ['title', 'content', 'image_files']