from django.conf.urls import url, include
from reporting import views
from DataUpload.dataUpload import *
from . import views

app_name = 'Reporting'

urlpatterns = [
    # /DataUpload/
    url(r'^$', views.testView, name='test'),
    url(r'^', views.report, name='report'),
]
