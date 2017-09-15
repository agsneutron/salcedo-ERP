# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import DeleteView

from users.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from ERP.lib.utilities import Utilities
from SalcedoERP.lib.constants import Constants

from django.forms import formset_factory

def empresas(request):
    return render(request, 'empresas.html')


def contratos(request):
    return render(request, 'contratos.html')


#Views for the model Users.
class UsersListView(ListView):
    model = User
    template_name = "users/users-list.html"
    query = None
    title_list = "Usuarios"
    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(UsersListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            UsersListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(username__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(first_name__icontains=q) for q in query_list))
            )
        else:
            UsersListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title_list'] = UsersListView.title_list
        context['query'] = UsersListView.query
        context['query_string'] = '&q=' + UsersListView.query
        context['has_query'] = (UsersListView.query is not None) and (UsersListView.query != "")
        return context


class UsersDetailView(generic.DetailView):
    model = User
    template_name = "users/users-detail.html"

