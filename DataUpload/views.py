# coding=utf-8

from django.db import transaction
from django.http import HttpResponse
from helper import DBObject, ErrorDataUpload


def testView(request):
    o = DBObject(request.user.id)

    try:
        #with transaction.atomic():
        o.save_all('/Users/josecarranza/Documents/Trabajo/Salcedo-ERP/DataUpload/ResultadoExportacion_2.xlsx',
                   o.INPUT_UPLOAD)
            # o.save_all('/Users/josecarranza/Documents/Trabajo/Salcedo-ERP/DataUpload/ResultadoExportacion_Partidas.xlsx',
            #            o.LINE_ITEM_UPLOAD)
    except ErrorDataUpload as e:
        e.save()
        raise e

    return HttpResponse('Done')
    # return render(request, 'DataUpload/carga.html')
