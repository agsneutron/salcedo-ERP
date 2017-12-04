from django.conf.urls import url

from Assistance import api
from DataUpload.dataUpload import *
import views

app_name = 'DataUpload'

urlpatterns = [

    url(r'^upload_file$', views.assistance_upload_view, name='assistance_upload'),
    url(r'^generate_automatic_absences', api.AutomaticAbsences.as_view(), name='assistance_automatic'),

]