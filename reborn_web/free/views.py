from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from .models import Free, Comment
from users.decorators import login_message_required, admin_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from .forms import FreeWriteForm
from users.models import User
import mimetypes
from mimetypes import guess_type
import os
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote
import urllib
from django.conf import settings
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


# 자유게시판 권한
# level 2,3 = CREATE. READ + 본인글 UPDATE, DELETE
# level 1 관리자 = CREATE, READ, DELETE + 본인글 UPDATE
# level 0 개발자 = CREATE, READ, UPDATE, DELETE


class FreeListView(ListView):
    model = Free
    paginate_by = 10
    template_name = 'free/free_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'free_list'        #DEFAULT : <app_label>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.order_by('-id') 

        if search_keyword :
            if search_type == 'all':
                free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
            elif search_type == 'title_content':
                free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
            elif search_type == 'title':
                free_list = free_list.filter(title__icontains=search_keyword)    
            elif search_type == 'content':
                free_list = free_list.filter(content__icontains=search_keyword)    
            elif search_type == 'writer':
                free_list = free_list.filter(writer__user_id__icontains=search_keyword)
        if free_list :
            return free_list
        else:
            messages.error(self.request, '일치하는 검색 결과가 없습니다.')
            free_list = Free.objects.order_by('-id')
            return free_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        context['q'] = search_keyword
        context['type'] = search_type

        return context


@login_message_required
def free_detail_view(request, pk):
    free = get_object_or_404(Free, pk=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'free_hits:{session_cookie}'
    comment = Comment.objects.filter(post=pk).order_by('created')

    if request.user == free.writer:
        free_auth = True
    else:
        free_auth = False

    context = {
        'free': free,
        'free_auth': free_auth,
        'comments': comment,
    }
    response = render(request, 'free/free_detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            free.hits += 1
            free.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        free.hits += 1
        free.save()
        return response
    return render(request, 'free/free_detail.html', context)


@login_message_required
def free_write_view(request):
    if request.method == "POST":
        form = FreeWriteForm(request.POST, request.FILES)
        user = request.session['user_id']
        user_id = User.objects.get(user_id = user)

        if form.is_valid():
            free = form.save(commit = False)
            free.writer = user_id
            free.save()
            return redirect('free:free_list')
    else:
        form = FreeWriteForm()
    return render(request, "free/free_write.html", {'form': form})


@login_message_required
def free_edit_view(request, pk):
    free = Free.objects.get(id=pk)

    if request.method == "POST":
        if(free.writer == request.user or request.user.level == '0'):
            form = FreeWriteForm(request.POST, request.FILES, instance=free)
            if form.is_valid():
                form.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/free/'+str(pk))
    else:
        free = Free.objects.get(id=pk)
        if free.writer == request.user or request.user.level == '0':
            form = FreeWriteForm(instance=free)
            return render(request, "free/free_write.html", {'form': form})
        else:
            messages.error(request, "본인 게시글이 아닙니다.")
            return redirect('/free/'+str(pk))


@login_message_required
def free_delete_view(request, pk):
    free = Free.objects.get(id=pk)
    if free.writer == request.user or request.user.level == '1' or request.user.level == '0':
        free.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('/free/')
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('/free/'+str(pk))


@login_message_required
def free_download_view(request, pk):
    free = get_object_or_404(Free, pk=pk)
    url = free.files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(file_url.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url[29:]
            return response
        raise Http404


# 댓글
@login_message_required
def comment_write_view(request, pk):
    post = get_object_or_404(Free, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user)
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전 작성',
        }
        if request.user == post.writer:
            data['self_comment'] = '(글쓴이)'
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")