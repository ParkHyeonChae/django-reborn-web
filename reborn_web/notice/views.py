from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Notice


class NoticeListView(ListView):
    model = Notice
    paginate_by = 10
    # template_name = 'notice/notice_list.html'  DEFAULT : <app_label>/<model_name>_list.html
    # context_object_name = 'notice_list'        DEFAULT : <app_label>_list

    def get_queryset(self):
        return Notice.objects.order_by('-id')
        
        # search_word = self.request.GET.get('search_word', '')
        # subject_type = self.request.GET.get('subject_type', '')
        # if search_word : # 검색 된 단어 있으면
        #     return Board.objects.filter(title__icontains=search_word) or Board.objects.filter(content__icontains=search_word)
        # if subject_type : # 클릭 된 키워드 있으면
        #     return Board.objects.filter(subject_type__icontains=subject_type)
        # return Board.objects.order_by('-id')


class NoticeDetailView(DetailView):
    model = Notice

    def get_object(self):
        notice = super().get_object()
        notice.hits += 1
        notice.save()
        return notice
