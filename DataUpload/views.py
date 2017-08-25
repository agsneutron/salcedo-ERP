# coding=utf-8
import uuid

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from helper import DBObject, ErrorDataUpload

from ERP.models import *

@transaction.atomic
def testView(request):
    o = DBObject('Puebla')
    # o.save_all('/Users/josecarranza/Documents/Trabajo/Salcedo-ERP/DataUpload/ResultadoExportacion_2.xlsx',
    #            o.INPUT_UPLOAD)
    o.save_all('/Users/josecarranza/Documents/Trabajo/Salcedo-ERP/DataUpload/ResultadoExportacion_Partidas.xlsx',
               9)
    return HttpResponse('Done')
    # return render(request, 'DataUpload/carga.html')
