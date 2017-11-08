from django.conf.urls import url, include
from HumanResources import views
from DataUpload.dataUpload import *
from . import views

app_name = 'HumanResources'

urlpatterns = [
    url(r'^', views.employeedetail, name='employeedetail'),
    url(r'^', views.employeehome, name='employeehome'),
]
