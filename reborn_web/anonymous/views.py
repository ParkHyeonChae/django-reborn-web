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
def anonymous_detail_view(request, pk):
    anonymous = get_object_or_404(Anonymous, pk=pk)
    
    if request.user == anonymous.writer:
        anonymous_auth = True
    else:
        anonymous_auth = False

    context = {
        'anonymous': anonymous,
        'anonymous_auth': anonymous_auth,
    }

    return render(request, 'anonymous/anonymous_detail.html', context)


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