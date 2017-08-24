from django.conf.urls import url
from ERP import views
from ERP.lib import erp_api
from ERP.lib import erp_forms_api


# These urls are called after /erp/ in the url.
urlpatterns = [
    url(r'^progress_estimate_log$', views.progress_estimate_log_view, name='progress_estimate_log_view'),
    #
    # Endpoints to retrieve information.
    url(r'^api/log_files_for_progress_estimate_log', erp_api.LogFilesForProgressEstimateLogEndpoint.as_view()),
    #
    # Endpoints to be called after a form to be saved.
    url(r'^forms_api/save_pel_form', erp_forms_api.SaveProgressEstimateLogFormEndpoint.as_view()),
    url(r'^forms_api/save_pel_file_form', erp_forms_api.SaveProgressEstimateLogFileFormEndpoint.as_view()),
    url(r'^empresas', views.empresas, name='empresas'),




]
