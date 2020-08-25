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


# 게시글 세부 권한 (free.detail.html)
# level 0 개발자 : 글의 수정, 삭제, 모든 댓글의 입력, 삭제, 모든 답글의 입력, 삭제 
# level 1 관리자 : 글의 삭제, 모든 댓글의 입력, 삭제, 모든 답글의 입력, 삭제
# level 2 사용자 : 글의 보기, 댓글의 입력, 답글의 입력 (본인일시 글의 수정, 삭제, 댓글의 입력, 삭제, 답글의 입력, 삭제)

# 1. 본인의 글일시 댓글과 답글에 (글쓴이) 표시를 한다.
# 2. 답글작성은 댓글에서만 가능하다. (답글에 답글불가)
# 3. 댓글과 답글 작성, 삭제시 그 갯수를 동적으로 표시한다.
# 4. 본 게시글이 삭제될시 댓글과 답글은 DB상에서 삭제된다.
# 5. 댓글과 답글 삭제시 DB상에서 내용은 보존한다.
# 6. 댓글과 답글 삭제시 삭제된 댓글이라는 표시를 한다.
# 7. 답글이 있는 댓글을 삭제해도 그 답글은 보존한다.
# 8. 답글의 입력창은 답글이 입력되는 위치에 동적으로 생성한다. (다른곳을 Click시 입력창 삭제)
# 9. 댓글과 답글 입력, 삭제는 비동기로 구현한다.


# 자유게시판 모두보기
class AllListView(ListView):
    model = Free
    paginate_by = 15
    template_name = 'free/free_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'free_list'        #DEFAULT : <app_label>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.order_by('-id') 

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_free_list = free_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_free_list = free_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_free_list = free_list.filter(writer__user_id__icontains=search_keyword)
                
                return search_free_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
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
         
        if len(search_keyword) > 1 :
            context['q'] = search_keyword
        context['type'] = search_type

        return context


# 카테고리 자유만 보기
class FreeListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.filter(category='자유').order_by('-id')
        
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_free_list = free_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_free_list = free_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_free_list = free_list.filter(writer__user_id__icontains=search_keyword)

                return search_free_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return free_list


# 카테고리 질문만 보기
class QuestionListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.filter(category='질문').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_free_list = free_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_free_list = free_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_free_list = free_list.filter(writer__user_id__icontains=search_keyword)
        
                return search_free_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return free_list


# 카테고리 정보만 보기
class InformationListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        free_list = Free.objects.filter(category='정보').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_free_list = free_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_free_list = free_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_free_list = free_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_free_list = free_list.filter(writer__user_id__icontains=search_keyword)
                    
                return search_free_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return free_list


# 자유게시판 글 상세보기
@login_message_required
def free_detail_view(request, pk):
    free = get_object_or_404(Free, pk=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'free_hits:{session_cookie}'
    comment = Comment.objects.filter(post=pk).order_by('created')
    # comment_count = comment.count()
    comment_count = comment.exclude(deleted=True).count()
    reply = comment.exclude(reply='0')

    if request.user == free.writer:
        free_auth = True
    else:
        free_auth = False

    context = {
        'free': free,
        'free_auth': free_auth,
        'comments': comment,
        'comment_count': comment_count,
        'replys': reply,
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


# 자유게시판 글 쓰기
@login_message_required
def free_write_view(request):
    if request.method == "POST":
        form = FreeWriteForm(request.POST, request.FILES)
        user = request.session['user_id']
        user_id = User.objects.get(user_id = user)
        
        if form.is_valid():
            free = form.save(commit = False)
            free.writer = user_id

            if request.FILES:
                if 'upload_files' in request.FILES.keys():
                    free.filename = request.FILES['upload_files'].name
                    
            free.save()
            return redirect('free:all_list')
    else:
        form = FreeWriteForm()
    return render(request, "free/free_write.html", {'form': form})


# 자유게시판 글 수정
@login_message_required
def free_edit_view(request, pk):
    free = Free.objects.get(id=pk)
    if request.method == "POST":
        if(free.writer == request.user or request.user.level == '0'):

            file_change_check = request.POST.get('fileChange', False)
            file_check = request.POST.get('upload_files-clear', False)

            if file_check or file_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, free.upload_files.path))

            form = FreeWriteForm(request.POST, request.FILES, instance=free)
            if form.is_valid():
                free = form.save(commit = False)

                if request.FILES:
                    if 'upload_files' in request.FILES.keys():
                        free.filename = request.FILES['upload_files'].name

                free.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/free/'+str(pk))
    else:
        free = Free.objects.get(id=pk)
        if free.writer == request.user or request.user.level == '0':
            form = FreeWriteForm(instance=free)
            context = {
                'form': form,
                'edit': '수정하기',
            }
            if free.filename and free.upload_files:
                context['filename'] = free.filename
                context['file_url'] = free.upload_files.url
            return render(request, "free/free_write.html", context)
            # return render(request, "free/free_write.html", {'form': form, 'edit': '수정하기'})
        else:
            messages.error(request, "본인 게시글이 아닙니다.")
            return redirect('/free/'+str(pk))


# 자유게시판 글 삭제
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


# 자유게시판 게시글 첨부파일 다운로드
@login_message_required
def free_download_view(request, pk):
    free = get_object_or_404(Free, pk=pk)
    url = free.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(free.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404


# 게시글 댓글달기
@login_message_required
def comment_write_view(request, pk):
    post = get_object_or_404(Free, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    reply = request.POST.get('reply')
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user, reply=reply)
        # comment_count = Comment.objects.filter(post=pk).count()
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전',
            'comment_count': comment_count,
            'comment_id': comment.id
        }
        if request.user == post.writer:
            data['self_comment'] = '(글쓴이)'
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


# 게시글 댓글 삭제
@login_message_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Free, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.writer or request.user.level == '1' or request.user.level == '0':
        # target_comment.delete()
        # target_comment.content = ('삭제된 댓글입니다.')
        target_comment.deleted = True
        target_comment.save()
        # comment_count = Comment.objects.filter(post=pk).count()
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'comment_id': comment_id,
            'comment_count': comment_count,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")