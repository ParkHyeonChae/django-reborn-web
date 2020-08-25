from django import forms
from .models import Notice

# from django.forms import FileInput, ClearableFileInput
# from django.utils.safestring import mark_safe

# class CustomFileWidget(forms.FileInput):
#     def __init__(self, attrs={}):
#         super(CustomFileWidget, self).__init__(attrs)

#     def render(self, name, value, attrs=None, renderer=None):
#         output = []
#         if value and hasattr(value, "url"):
#             output.append('%s <a target="_blank" href="%s">%s</a> <br />%s' %('첨부파일 :', value.url, value, '변경:'))
#         output.append(super(CustomFileWidget, self).render(name, value, attrs))
#         return mark_safe(u''.join(output))

class NoticeWriteForm(forms.ModelForm):
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={
    #     'multiple': True
    #     }))
    def __init__(self, *args, **kwargs):
        super(NoticeWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })

    class Meta:
        model = Notice
        fields = ['title', 'content', 'upload_files', 'top_fixed']
        # widgets = {
        #     'upload_files': CustomFileWidget
        # }