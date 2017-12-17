# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext,loader
from Accounting.models import *
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

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