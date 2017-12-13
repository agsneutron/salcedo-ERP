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
    context = RequestContext(request, {
        'account': Account.objects.all(),

    })
    return HttpResponse(template.render(context))