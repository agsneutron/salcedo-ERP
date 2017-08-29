# coding=utf-8
from __future__ import unicode_literals

import operator
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView

from ERP.models import ProgressEstimateLog, LogFile, ProgressEstimate, Empresa, ContratoContratista
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
#


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
        context['query_string'] = '&q='+CompaniesListView.query
        context['has_query'] = (CompaniesListView.query is not None) and (CompaniesListView.query != "")
        print context
        return context


class CompanyDetailView(generic.DetailView):
    model = Empresa
    template_name = "ERP/company-detail.html"




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