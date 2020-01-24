from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView
from .models import Notice
from users.decorators import login_message_required


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

@login_message_required
def notice_detail_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    # notice = Notice.objects.filter(id=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'notice_hits:{session_cookie}'
    context = {
        'notice': notice,
    }
    response = render(request, 'notice/notice_detail.html', context)
 
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            # notice.update(hits=F('hits') + 1)
            notice.hits += 1
            notice.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        # notice.update(hits=F('hits') + 1)
        notice.hits += 1
        notice.save()
        return response
    return render(request, 'notice/notice_detail.html', context)
