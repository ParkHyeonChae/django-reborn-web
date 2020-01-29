from django import forms
from .models import Free, Comment


class FreeWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FreeWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })

    class Meta:
        model = Free
        fields = ['title', 'content', 'files']


# class FreeCommentForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(FreeCommentForm, self).__init__(*args, **kwargs)
#         self.fields['content'].widget.attrs.update({
#             'placeholder': '댓글을 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_content',
#         })
#     class Meta:
#         model = Comment
#         fields = ['content',]