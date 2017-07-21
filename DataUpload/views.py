# coding=utf-8
import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from helper import DBObject, ErrorDataUpload

from ERP.models import *


def testView(request):
    o = DBObject('Puebla')
    o.save_all('/Users/josecarranza/Documents/Trabajo/Salcedo-ERP/DataUpload/Orion.xlsx')
    return HttpResponse('Done')
    # return render(request, 'DataUpload/carga.html')
