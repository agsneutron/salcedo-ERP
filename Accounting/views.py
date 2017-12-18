# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.template import RequestContext,loader
from Accounting.models import *
from django.http import HttpResponse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

import operator

from django.db.models import Q

# Create your views here.
def PolicieDetail(request):
    template = loader.get_template('Accounting/policie-detail.html')
    return HttpResponse(template.render(request))

# For Search Account filter objects view
def SearchAccount(request):
    template = loader.get_template('Accounting/search_account.html')
    context = {'account': Account.objects.all(),}

    return HttpResponse(template.render(context,request))


# For Search Comercial Allie filter objects view
def SearchProvider(request):
    title = "Proveedores"
    template = loader.get_template('Accounting/search_commercialally.html')
    context = {'commercialally': CommercialAlly.objects.filter(type=0),
               's_type': str(title),
               'type': str("PROVIDER"), }

    return HttpResponse(template.render(context,request))


def SearchCreditors(request):
    title = "Acreedores"
    template = loader.get_template('Accounting/search_commercialally.html')
    context = {'commercialally': CommercialAlly.objects.filter(type=1),
               's_type': str(title),
               'type': str("CREDITOR"), }

    return HttpResponse(template.render(context,request))


def SearchThird(request):
    title = "Terceros"
    template = loader.get_template('Accounting/search_commercialally.html')
    context = {'commercialally': CommercialAlly.objects.filter(type=2),
               's_type': str(title),
               'type': str("THIRD_PARTY"), }

    return HttpResponse(template.render(context,request))


def SearchPolicies(request):
    template = loader.get_template('Accounting/search_policy.html')
    context = {'typepolicy': TypePolicy.objects.all(),}

    return HttpResponse(template.render(context,request))


# For  Transactions by account filter objects view
def SearchTransactions(request):
    template = loader.get_template('Accounting/search_transactions.html')
    context = {'typepolicy': TypePolicy.objects.all(),}

    return HttpResponse(template.render(context, request))


# For  Policies by account list view
def PoliciesAccountList(request):
    template = loader.get_template('Accounting/policiesbyaccount_list.html')
    context = {'lower_fiscal_period_year': request.GET.get('lower_fiscal_period_year'),
               'uppper_fiscal_period_year': request.GET.get('uppper_fiscal_period_year'),
               'lower_fiscal_period_month': request.GET.get('lower_fiscal_period_month'),
               'upper_fiscal_period_month': request.GET.get('upper_fiscal_period_month'),
               'account': request.GET.get('account')}
    return HttpResponse(template.render(context, request))


# For Add Comercial Allie filter objects view
def AddhProvider(request):
    title = "Proveedores"
    template = loader.get_template('/admin/Accounting/')
    context = {'s_type': str(title),
               'type': str("PROVIDER"), }

    return HttpResponse(template.render(context,request))


'''class AccountingPolicyListView(ListView):
    model = AccountingPolicy
    template_name = "Accounting/accountingpolicy-list.html"
    # search_fields = ("empresaNombre",)
    query = None
    title_list = 'Pólizas'
    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(AccountingPolicyListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            AccountingPolicyListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(folio__icontains=q) for q in query_list))
            )
        else:
            AccountingPolicyListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(AccountingPolicyListView, self).get_context_data(**kwargs)
        context['title_list'] = AccountingPolicyListView.title_list
        context['query'] = AccountingPolicyListView.query
        context['query_string'] = '&q=' + AccountingPolicyListView.query
        context['has_query'] = (AccountingPolicyListView.query is not None) and (AccountingPolicyListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_contratista'):
            raise PermissionDenied
        return super(AccountingPolicyListView, self).dispatch(request, args, kwargs)'''


class AccountingPolicyDetailView(generic.DetailView):
    model = AccountingPolicy
    template_name = "ERP/AccountingPolicyDetail-detail.html"

    def get_context_data(self, **kwargs):
        context = super(AccountingPolicyDetailView, self).get_context_data(**kwargs)
        contractor_id = self.kwargs['pk']
        context['details'] = AccountingPolicyDetail.objects.filter(Q(contractor__id=contractor_id))
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_accountingpolicy'):
            raise PermissionDenied
        return super(AccountingPolicyDetailView, self).dispatch(request, args, kwargs)

class AccountDetailView(generic.DetailView):
    model = Account
    template_name = "SharedCatalogs /account-detail.html"

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        contractor_id = self.kwargs['pk']
        context['details'] = Account.objects.filter(Q(id=contractor_id))
        return context

    def dispatch(self, request, *args, **kwargs):
        #if not request.user.has_perm('ERP.view_list_accountingpolicy'):
        #    raise PermissionDenied
        return super(AccountDetailView, self).dispatch(request, args, kwargs)