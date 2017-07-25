from django.conf.urls import url
from ERP import views

urlpatterns = [
    url(r'^progress_estimate_log$', views.progress_estimate_log_view, name='progress_estimate_log_view'),
]
