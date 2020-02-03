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
        form = AnonymousWriteForm(request.POST)
        user_id = request.user

        if form.is_valid():
            free = form.save(commit = False)
            free.writer = user_id
            free.save()
            return redirect('anonymous:anonymous_list')
    else:
        form = AnonymousWriteForm()
    return render(request, "anonymous/anonymous_write.html", {'form': form})