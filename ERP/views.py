# coding=utf-8
from __future__ import unicode_literals

import operator
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView

from ERP.models import ProgressEstimateLog, LogFile, ProgressEstimate, Empresa, ContratoContratista, Contratista,Project, Propietario, Concept_Input, LineItem
from django.db.models import Q
import json

from django.shortcuts import render
from ERP.lib.utilities import Utilities
from django.utils import timezone


# Create your views here.
def progress_estimate_log_view(request):
    project = request.GET.get('project')
    concept = request.GET.get('concept')
    estimate = request.GET.get('estimate')
    progress_estimate = request.GET.get('progress_estimate')

    # Retrieving data from the model to be rendered.
    if progress_estimate is None:
        logs_queryset = ProgressEstimateLog.objects.all()
    else:
        logs_queryset = ProgressEstimateLog.objects.first(Q(progress_estimate=progress_estimate))

    if logs_queryset:
        # As both cases where treated as querysets, we can retrieve the first id.
        progress_estimate_id = logs_queryset.first().progress_estimate.id
        logs = []
        for log in logs_queryset:
            user_fullname = log.user.user.first_name + " " + log.user.user.last_name
            log = log.to_serializable_dict()
            log['user_fullname'] = user_fullname
            logs.append(log)

        log_files = []
        if logs:
            log_files = LogFile.objects.filter(Q(progress_estimate_log__id=logs[0]['id']))

        params = {
            'logs': Utilities.json_to_safe_string(logs),
            'log_files': Utilities.query_set_to_json_string(log_files),
            'progress_estimate_id': progress_estimate_id
        }

    else:
        params = {
            'logs': [],
            'log_files': [],
            'progress_estimate_id': ProgressEstimate.objects.all().first().id
        }

    return render(request, 'ProgressEstimateLog/progress_estimate_log_form.html', params)


# def upload_file(request):
#     if request.method == 'POST':
#         form = LineItemUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             #handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = LineItemUploadForm()
#     return render(request, 'upload.html', {'form': form})


class CompaniesListView(ListView):
    model = Empresa
    template_name = "ERP/company-list.html"
    # search_fields = ("empresaNombre",)
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(CompaniesListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            CompaniesListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombreEmpresa__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(calle__icontains=q) for q in query_list))
            )
        else:
            CompaniesListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(CompaniesListView, self).get_context_data(**kwargs)
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q=' + CompaniesListView.query
        context['has_query'] = (CompaniesListView.query is not None) and (CompaniesListView.query != "")
        return context


class CompanyDetailView(generic.DetailView):
    model = Empresa
    template_name = "ERP/company-detail.html"


class ContractorListView(ListView):
    model = Contratista
    template_name = "ERP/contractor-list.html"
    # search_fields = ("empresaNombre",)
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ContractorListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            CompaniesListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombreContratista__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(calle__icontains=q) for q in query_list))
            )
        else:
            CompaniesListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(ContractorListView, self).get_context_data(**kwargs)
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q=' + CompaniesListView.query
        context['has_query'] = (CompaniesListView.query is not None) and (CompaniesListView.query != "")
        return context


class ContractorDetailView(generic.DetailView):
    model = Contratista
    template_name = "ERP/contractor-detail.html"




# Views for the model ContratoContratista.
class ContractorContractListView(ListView):
    model = ContratoContratista
    template_name = "ERP/contractor-contract-list.html"
    query = None

    """
       Display a Blog List page filtered by the search query.
       """
    paginate_by = 10

    def get_queryset(self):
        result = super(ContractorContractListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            ContractorContractListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(dependencia__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(project__nombreProyecto__icontains=q) for q in query_list))
            )
        else:
            ContractorContractListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(ContractorContractListView, self).get_context_data(**kwargs)
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q='+ContractorContractListView.query
        context['has_query'] = (ContractorContractListView.query is not None) and (ContractorContractListView.query != "")
        print context
        return context


class ContractorContractDetailView(generic.DetailView):
    model = ContratoContratista
    template_name = "ERP/contractor-contract-detail.html"



# Views for the model Propietaro.
class OwnerListView(ListView):
    model = Propietario
    template_name = "ERP/owner-list.html"
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(OwnerListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            OwnerListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombrePropietario__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(rfc__icontains=q) for q in query_list))
            )
        else:
            OwnerListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(OwnerListView, self).get_context_data(**kwargs)
        context['query'] = OwnerListView.query
        context['query_string'] = '&q='+OwnerListView.query
        context['has_query'] = (OwnerListView.query is not None) and (OwnerListView.query != "")
        return context


class OwnerDetailView(generic.DetailView):
    model = Propietario
    template_name = "ERP/owner-detail.html"



# Views for the model Concept Input.
class ConceptInputListView(ListView):
    model = Concept_Input
    template_name = "ERP/concept-input-list.html"
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ConceptInputListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            ConceptInputListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(key__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))|
                reduce(operator.and_,
                       (Q(status__icontains=q) for q in query_list))
            )
        else:
            ConceptInputListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(ConceptInputListView, self).get_context_data(**kwargs)
        context['query'] = ConceptInputListView.query
        context['query_string'] = '&q=' + ConceptInputListView.query
        context['has_query'] = (ConceptInputListView.query is not None) and (ConceptInputListView.query != "")
        return context

class ConceptInputDetailView(generic.DetailView):
    model = Concept_Input
    template_name = "ERP/concept-input-detail.html"


# Views for the model Concept Input.
class LineItemListView(ListView):
    model = LineItem
    template_name = "ERP/line-item-list.html"
    query = None
    project_id = None
    parent_id = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(LineItemListView, self).get_queryset()

        # Reading the params from the url.
        LineItemListView.project_id = self.kwargs['project']
        LineItemListView.parent_id = self.kwargs['parent']

        # If the param for the parent is received as 0, then its value must be None.
        if LineItemListView.parent_id == '0':
            LineItemListView.parent_id = None

        print "The filters:"
        print "Project Id: " + str(LineItemListView.project_id)
        print "Parent Id: " + str(LineItemListView.parent_id)

        # Filtering the results.
        result = result.filter(Q(project__id = LineItemListView.project_id) & Q(parent_line_item__id = LineItemListView.parent_id))


        # Query to filter the list content.
        query = self.request.GET.get('q')

        if query:
            LineItemListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(key__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )
        else:
            LineItemListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(LineItemListView, self).get_context_data(**kwargs)
        context['project_id'] = LineItemListView.project_id
        context['query'] = LineItemListView.query
        context['query_string'] = '&q=' + LineItemListView.query
        context['has_query'] = (LineItemListView.query is not None) and (LineItemListView.query != "")

        # Getting the concept inputs for the selected Line Item parent.
        context['concepts_inputs'] = Concept_Input.objects.filter(Q(line_item=LineItemListView.parent_id))

        print "Concept / Inputs"
        print context['concepts_inputs']
        return context

class LineItemDetailView(generic.DetailView):
    model = LineItem
    template_name = "ERP/line-item-detail.html"

class ProjectListView(ListView):
    model = Project
    template_name = "ERP/project-list.html"
    # search_fields = ("empresaNombre",)
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ProjectListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            ProjectListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombreProyecto__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(ubicacion_calle__icontains=q) for q in query_list))
            )
        else:
            ProjectListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['query'] = ProjectListView.query
        context['query_string'] = '&q=' + ProjectListView.query
        context['has_query'] = (ProjectListView.query is not None) and (ProjectListView.query != "")
        return context


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "ERP/project-detail.html"
