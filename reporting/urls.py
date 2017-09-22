from django.conf.urls import url

from DataUpload.dataUpload import *
from . import views

app_name = 'Reporting'

urlpatterns = [
    #/DataUpload/
    url(r'^$', views.testView, name='test'),
]