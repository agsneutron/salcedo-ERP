from django.conf.urls import url

from DataUpload.dataUpload import *
import views

app_name = 'DataUpload'

urlpatterns = [

    url(r'^upload_file$', views.assistance_upload_test_view, name='assistance_test'),

]