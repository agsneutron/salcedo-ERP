from django.conf.urls import url
from ERP import views
from ERP.lib import erp_api

urlpatterns = [
    url(r'^progress_estimate_log$', views.progress_estimate_log_view, name='progress_estimate_log_view'),
    #
    # Endpoints
    url(r'^api/log_files_for_progress_estimate_log', erp_api.LogFilesForProgressEstimateLogEndpoint.as_view()),

]
