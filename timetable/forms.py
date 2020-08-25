from django import forms
from .models import TimeTable


class TimeTableEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TimeTableEditForm, self).__init__(*args, **kwargs)
        # self.fields['grade'].label = '학년'
        # self.fields['grade'].widget.attrs.update({
        #     'class': 'form-control',
        # })
        self.fields['subject'].label = '과목명'
        self.fields['subject'].widget.attrs.update({
            'placeholder': '과목명',
            'class': 'form-control',
        })
        self.fields['professor'].label = '담당교수'
        self.fields['professor'].widget.attrs.update({
            'placeholder': '담당교수',
            'class': 'form-control',
        })
        # self.fields['date'].label = '시험날짜'
        # self.fields['date'].widget.attrs.update({
        #     'placeholder': '시험날짜',
        #     'class': 'form-control',
        # })
        self.fields['day'].label = '시험요일'
        self.fields['day'].widget.attrs.update({
            'placeholder': '시험요일',
            'class': 'form-control',
        })
        self.fields['time'].label = '시험교시'
        self.fields['time'].widget.attrs.update({
            'placeholder': '시험교시',
            'class': 'form-control',
        })
        self.fields['time_length'].label = '시험시간'
        self.fields['time_length'].widget.attrs.update({
            'placeholder': '시험시간',
            'class': 'form-control',
        })
        self.fields['location'].label = '시험장소'
        self.fields['location'].widget.attrs.update({
            'placeholder': '시험장소',
            'class': 'form-control',
        })
    
    class Meta:
        model = TimeTable
        fields = ['grade', 'subject', 'professor', 'date', 'day', 'time', 'time_length', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'시험일자', 'type':'date'}),
        }


class TimeTableAddForm(TimeTableEditForm):
    class Meta:
        model = TimeTable
        fields = ['subject', 'professor', 'date', 'day', 'time', 'time_length', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'placeholder': '시험일자', 'type':'date'}),
        }
