# coding=utf-8

from django.conf.urls import url

from DataUpload.dataUpload import *
from . import views

app_name = 'DataUpload'

urlpatterns = [
    #/DataUpload/
    url(r'^$', views.testView, name='test'),
    url(r'^borrar_registros$', BorrarRegistros.as_view(), name='borrar_registros'),
    url(r'^cargar$', DataUpload.as_view(), name='cargar'),
    url(r'^listar_cargas$', ListaRegistros.as_view(), name='listar_cargas'),
]