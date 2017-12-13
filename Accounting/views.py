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
    accounts = Account.objects.all()

    context = {'object_list': accounts}
    return HttpResponse(template.render(context, request))