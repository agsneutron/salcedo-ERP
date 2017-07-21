# coding=utf-8

from django.http import HttpResponse
from django.views.generic import ListView
#from oauth2_provider.models import AccessToken

from DataUpload.helper import DBObject, ErrorDataUpload
from DataUpload.models import UsuarioFolio
import datetime
import json


# Convierte a un string separado por comas en un arreglo o None
def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(str, the_string.split(','))


class DataUpload(ListView):
    def handle_uploaded_file(self, archivo):
        ruta = 'DataUpload/tmp/' + str(datetime.datetime.now()) + '.csv'
        with open(ruta, 'wb+') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)
        return ruta

    def get_usuario_for_token(token):
        if token:
            return AccessToken.objects.get(token=token).user
        else:
            return None

    def post(self, request, *args, **kwargs):
        # archivo = request.POST.get('archivo')
        archivo = request.FILES['archivo']
        ruta = self.handle_uploaded_file(archivo);
        parametros = ['fecha_venta',
                      'meta',
                      'ventas_totales',
                      'ventas_canceladas',
                      'ventas_netas',
                      'boletos',
                      'boletos_cancelados',
                      'apuestas',
                      'premios_pagados',
                      'presupuesto',
                      ['agencia', 'nombre_agencia'],  # Fk, [column name model, column name foreign entity]
                      ['producto', 'nombre_producto']]  # Fk, [column name model, column name foreign entity]

        #token = request.GET.get('access_token')
        #usuario = self.get_usuario_for_token(token)

        #nombre_usuario = usuario.first_name + ' ' + usuario.last_name

        nombre_usuario = 'Luis Gómez'
        objeto = DBObject(Venta, nombre_usuario,
                          parametros)

        try:
            folio = objeto.save_all(ruta)
            return HttpResponse(folio)
        except Exception, e:
            return HttpResponse("Error: " + str(e.message))
        return HttpResponse(ruta)


class BorrarRegistros(ListView):
    def get(self, request, *args, **kwargs):
        folio = request.GET.get('folio')
        try:
            Venta.objects.filter(folio=folio).delete()
            return HttpResponse("OK")
        except Exception, e:
            return HttpResponse("Error: " + str(e.message))


class ListaRegistros(ListView):
    def get(self, request, *args, **kwargs):
        registros = UsuarioFolio.objects.all()
        json_response = []
        for registro in registros:
            json_response.append(registro.to_serilizable_dic())

        return HttpResponse(json.dumps(json_response, indent=4, sort_keys=False, ensure_ascii=False),
                            'application/json; charset=utf-8')
