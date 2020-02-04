from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from users.decorators import login_message_required, admin_required
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from .models import Anonymous, AnonymousComment
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from users.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .forms import AnonymousWriteForm
from django.views.decorators.http import require_GET, require_POST

class AnonymousListView(ListView):
    model = Anonymous
    paginate_by = 10
    template_name = 'anonymous/anonymous_list.html'
    context_object_name = 'anonymous_list'

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        anonymous_list = Anonymous.objects.order_by('-id') 

        if search_keyword :
            if search_type == 'all':
                anonymous_list = anonymous_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
            elif search_type == 'title_content':
                anonymous_list = anonymous_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
            elif search_type == 'title':
                anonymous_list = anonymous_list.filter(title__icontains=search_keyword)    
            elif search_type == 'content':
                anonymous_list = anonymous_list.filter(content__icontains=search_keyword)
        if anonymous_list :
            return anonymous_list
        else:
            messages.error(self.request, '일치하는 검색 결과가 없습니다.')
            # anonymous_list = Anonymous.objects.order_by('-id')
            return anonymous_list


@login_message_required
def anonymous_detail_view(request, pk):
    anonymous = get_object_or_404(Anonymous, pk=pk)
    comment = AnonymousComment.objects.filter(post=pk).order_by('created')
    comment_count = comment.exclude(deleted=True).count()
    reply = comment.exclude(reply='0')

    if anonymous.likes.filter(id=request.user.id):
        like_user_info = True
    else: like_user_info = False

    if request.user == anonymous.writer:
        anonymous_auth = True
    else: anonymous_auth = False

    context = {
        'anonymous': anonymous,
        'anonymous_auth': anonymous_auth,
        'comments': comment,
        'comment_count': comment_count,
        'replys': reply,
        'like_user_info': like_user_info,
    }
    return render(request, 'anonymous/anonymous_detail.html', context)


@login_message_required
def anonymous_write_view(request):
    if request.method == "POST":
        form = AnonymousWriteForm(request.POST, request.FILES)
        user_id = request.user

        if form.is_valid():
            anonymous = form.save(commit = False)
            anonymous.writer = user_id
            anonymous.save()
            return redirect('anonymous:anonymous_list')
    else:
        form = AnonymousWriteForm()
    return render(request, "anonymous/anonymous_write.html", {'form': form})


@login_message_required
def anonymous_edit_view(request, pk):
    anonymous = Anonymous.objects.get(id=pk)
    if request.method == "POST":
        if(anonymous.writer == request.user or request.user.level == '0'):
            form = AnonymousWriteForm(request.POST, request.FILES, instance=anonymous)
            if form.is_valid():
                form.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/anonymous/'+str(pk))
    else:
        anonymous = Anonymous.objects.get(id=pk)
        if anonymous.writer == request.user or request.user.level == '0':
            form = AnonymousWriteForm(instance=anonymous)
            return render(request, "anonymous/anonymous_write.html", {'form': form})
        else:
            messages.error(request, "본인 게시글이 아닙니다.")
            return redirect('/anonymous/'+str(pk))


@login_message_required
def anonymous_delete_view(request, pk):
    anonymous = Anonymous.objects.get(id=pk)
    if anonymous.writer == request.user or request.user.level == '1' or request.user.level == '0':
        anonymous.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('/anonymous/')
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('/anonymous/'+str(pk))


@login_message_required
def comment_write_view(request, pk):
    post = get_object_or_404(Anonymous, id=pk)
    content = request.POST.get('content')
    writer = request.POST.get('writer')
    reply = request.POST.get('reply')
    if content:
        comment = AnonymousComment.objects.create(post=post, content=content, writer=request.user, reply=reply)
        comment_count = AnonymousComment.objects.filter(post=pk).exclude(deleted=True).count()
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


@login_message_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Anonymous, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = AnonymousComment.objects.get(pk = comment_id)

    if request.user == target_comment.writer or request.user.level == '1' or request.user.level == '0':
        target_comment.deleted = True
        target_comment.save()
        comment_count = AnonymousComment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'comment_id': comment_id,
            'comment_count': comment_count,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


# 추천하기
@login_message_required
@require_POST
def post_like_view(request):
    post_id = request.POST.get('post')
    like_user = request.user
    post = get_object_or_404(Anonymous, id=post_id)
    
    if post.likes.filter(id=like_user.id):
        post.likes.remove(like_user)
        user_info = False
    else:
        post.likes.add(like_user)
        user_info = True

    data = {
        'like_count': post.like_count,
        'user_info': user_info
    }
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")