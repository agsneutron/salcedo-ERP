from django.conf.urls import url
from ERP import views, api
from ERP.lib import erp_api
from ERP.lib import erp_forms_api

# These urls are called after /erp/ in the url.
from ERP.views import CompaniesListView

urlpatterns = [



    url(r'^progress_estimate_log$', views.progress_estimate_log_view, name='progress_estimate_log_view'),
    #
    # Endpoints to retrieve information.
    url(r'^api/log_files_for_progress_estimate_log', erp_api.LogFilesForProgressEstimateLogEndpoint.as_view()),
    url(r'^api/concepts_inputs_by_line_item_and_type', erp_api
        .ConceptInputsForLineItemAndType.as_view()),
    url(r'^api/get_project_info', erp_api.GetProjectInfo.as_view()),
    #
    # Endpoints to be called after a form to be saved.
    url(r'^forms_api/save_pel_form', erp_forms_api.SaveProgressEstimateLogFormEndpoint.as_view()),
    url(r'^forms_api/save_pel_file_form', erp_forms_api.SaveProgressEstimateLogFileFormEndpoint.as_view()),
    url(r'^api/project_list', api.ProjectEndpoint.as_view()),
    url(r'^api/contractor_list', api.ContractorByProject.as_view()),

    url(r'^api/line_items_by_projects', api.LineItemsByProject.as_view()),
    url(r'^api/estimates_by_line_item', api.EstimatesByLineItems.as_view(), ),
    url(r'^api/sections_for_project_save', api.SectionsByProjectSave.as_view()),
    url(r'^api/sections_by_project', api.SectionsByProjectEndpoint.as_view()),
    url(r'^api/Saveamountofestimate', api.Saveamountofestimate.as_view()),

    url(r'^api/clean_project', api.CleanProject.as_view()),
    url(r'^api/clean_estimate', api.CleanEstimate.as_view()),


    # Endpoint to manage user assignment to a project.
    url(r'^api/get_access_to_project_by_user', api.AccessToProjectByUser.as_view()),


]

# handler404 = 'views.custom404'
# handler500 = 'views.custom500'
