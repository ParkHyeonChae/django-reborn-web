from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Notice

class NoticeList(ListView):
    model = Notice
    paginate_by = 10
    # template_name = 'notice/notice_list.html'  DEFAULT : <app_label>/<model_name>_list.html
    # context_object_name = 'notice_list'        DEFAULT : <app_label>_list

    def get_queryset(self):
        return Notice.objects.order_by('-id')

