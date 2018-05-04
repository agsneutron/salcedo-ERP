# coding=utf-8
from __future__ import unicode_literals

import operator
import urllib
import locale
import decimal
from datetime import date

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms.models import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, loader
import datetime
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView

from ERP.forms import EstimateSearchForm, AddEstimateForm, ContractConceptsForm, EstimateDedutionsForm
from ERP.models import ProgressEstimateLog, LogFile, ProgressEstimate, Empresa, ContratoContratista, Contratista, \
    Propietario, Concept_Input, LineItem, Estimate, Project, UploadedInputExplotionsHistory, UploadedCatalogsHistory, \
    Contact, AccessToProject, \
    ProjectSections, ContractConcepts, ProgressEstimateAuthorization, EstimateAdvanceAuthorization
from django.db.models import Q
import json

from django.shortcuts import render, redirect
from ERP.lib.utilities import Utilities
from SalcedoERP.lib.constants import Constants

from django.forms import formset_factory

from users.models import ERPUser


def custom_404(request):
    return render_to_response('404.html', RequestContext(request))


def custom_500(request):
    return render_to_response('500.html', RequestContext(request))


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


def unlock_estimate(request, pk):
    if request.method == 'POST':
        estimate = Estimate.objects.get(pk=pk)
        amount = request.POST.get('liquidation_amount')

        if amount == "":
            messages.error(request, 'Tienes que definir un finiquito para desbloquear la estimación.')
            return HttpResponseRedirect('/admin/ERP/estimate/' + str(estimate.id) + '/')

        estimate.lock_status = 'U'

        estimate.save()

        advance = ProgressEstimate()

        advance.estimate = estimate
        advance.key = 'FINIQUITO'
        advance.amount = amount
        advance.type = ProgressEstimate.SETTLEMENT
        advance.payment_status = ProgressEstimate.NOT_PAID

        advance.save()

        return HttpResponseRedirect('/admin/ERP/estimate/' + str(estimate.id) + '/')
    else:

        to_delete = ProgressEstimate.objects.filter(type=ProgressEstimate.SETTLEMENT)
        for item in to_delete:
            item.delete()

        raise PermissionDenied


def approve_progress_estimate(request, pk):
    if request.method == 'POST':
        progress_estimate = ProgressEstimate.objects.get(pk=pk)

        user = request.user
        user_full_name = user.first_name + ' ' + user.last_name

        permissions = ['users.is_general_director',
                       'users.is_project_director',
                       'users.is_vicepresident',
                       'users.is_head_manager',
                       'users.is_president']

        permission_roles = {'users.is_general_director': 'Director General',
                            'users.is_project_director': 'Director de Obras',
                            'users.is_vicepresident': 'Vicepresidente Empresarial',
                            'users.is_head_manager': 'Jefe de Administración',
                            'users.is_president': 'Presidente'}

        for permission in permissions:
            if user.has_perm(permission):

                test_authorization = ProgressEstimateAuthorization.objects.filter(
                    Q(user_id=user.id) & Q(progress_estimate_id=progress_estimate.id))

                if len(test_authorization) == 0:
                    authorization = ProgressEstimateAuthorization()
                    authorization.full_name = permission_roles[permission] + ': ' + user_full_name
                    authorization.user = user
                    authorization.progress_estimate = progress_estimate

                    authorization.save()

        return HttpResponseRedirect('/admin/ERP/estimate/' + str(progress_estimate.estimate.id) + '/')
    else:

        to_delete = ProgressEstimate.objects.filter(type=ProgressEstimate.SETTLEMENT)
        for item in to_delete:
            item.delete()

        raise PermissionDenied


def approve_estimate_advance(request, pk):
    if request.method == 'POST':
        estimate = Estimate.objects.get(pk=pk)

        user = request.user
        user_full_name = user.first_name + ' ' + user.last_name

        permissions = ['users.is_general_director',
                       'users.is_project_director',
                       'users.is_vicepresident',
                       'users.is_head_manager',
                       'users.is_president']

        permission_roles = {'users.is_general_director': 'Director General',
                            'users.is_project_director': 'Director de Obras',
                            'users.is_vicepresident': 'Vicepresidente Empresarial',
                            'users.is_head_manager': 'Jefe de Administración',
                            'users.is_president': 'Presidente'}

        for permission in permissions:
            if user.has_perm(permission):

                test_authorization = EstimateAdvanceAuthorization.objects.filter(
                    Q(user_id=user.id) & Q(estimate_id=estimate.id))

                if len(test_authorization) == 0:
                    authorization = EstimateAdvanceAuthorization()
                    authorization.full_name = permission_roles[permission] + ': ' + user_full_name
                    authorization.user = user
                    authorization.estimate = estimate

                    authorization.save()

        return HttpResponseRedirect('/admin/ERP/estimate/' + str(estimate.id) + '/')
    else:

        to_delete = ProgressEstimate.objects.filter(type=ProgressEstimate.SETTLEMENT)
        for item in to_delete:
            item.delete()

        raise PermissionDenied


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
    title_list = 'Clientes'

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
        context['title_list'] = CompaniesListView.title_list
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q=' + CompaniesListView.query
        context['has_query'] = (CompaniesListView.query is not None) and (CompaniesListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_empresa'):
            raise PermissionDenied
        return super(CompaniesListView, self).dispatch(request, args, kwargs)


class CompanyDetailView(generic.DetailView):
    model = Empresa
    template_name = "ERP/company-detail.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        company_id = self.kwargs['pk']
        context['owners'] = Propietario.objects.filter(Q(empresa__id=company_id))
        context['projects'] = Project.objects.filter(Q(empresa__id=company_id))
        return context


class ContractorListView(ListView):
    model = Contratista
    template_name = "ERP/contractor-list.html"
    # search_fields = ("empresaNombre",)
    query = None
    title_list = 'Contratistas'
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
        context['title_list'] = ContractorListView.title_list
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q=' + CompaniesListView.query
        context['has_query'] = (CompaniesListView.query is not None) and (CompaniesListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_contratista'):
            raise PermissionDenied
        return super(ContractorListView, self).dispatch(request, args, kwargs)


class ContractorDetailView(generic.DetailView):
    model = Contratista
    template_name = "ERP/contractor-detail.html"

    def get_context_data(self, **kwargs):
        context = super(ContractorDetailView, self).get_context_data(**kwargs)
        contractor_id = self.kwargs['pk']
        context['contacts'] = Contact.objects.filter(Q(contractor__id=contractor_id))
        context['contracts'] = ContratoContratista.objects.filter(Q(contratista=contractor_id))
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_contratista'):
            raise PermissionDenied
        return super(ContractorDetailView, self).dispatch(request, args, kwargs)


# Views for the model ContratoContratista.
class ContractorContractListView(ListView):
    model = ContratoContratista
    template_name = "ERP/contractor-contract-list.html"
    query = None
    title_list = 'Contratos con Contratistas'
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
                       (Q(clave_contrato__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(project__nombreProyecto__icontains=q) for q in query_list))
            )
        else:
            ContractorContractListView.query = ''

        # Get the projects to which the user has access
        user = self.request.user

        project_ids = AccessToProject.get_projects_for_user(user.id)
        if len(project_ids) > 0:
            # Filter the result to only include the appropriate results
            result = result.filter(reduce(operator.or_, (Q(project_id=pid) for pid in project_ids)))

        return result

    def get_context_data(self, **kwargs):
        context = super(ContractorContractListView, self).get_context_data(**kwargs)
        context['title_list'] = ContractorContractListView.title_list
        context['query'] = CompaniesListView.query
        context['query_string'] = '&q=' + ContractorContractListView.query
        context['has_query'] = (ContractorContractListView.query is not None) and (
            ContractorContractListView.query != "")
        print context
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_contratocontratista'):
            raise PermissionDenied
        return super(ContractorContractListView, self).dispatch(request, args, kwargs)


class ContractorContractDetailView(generic.DetailView):
    model = ContratoContratista
    template_name = "ERP/contractor-contract-detail.html"

    def get_context_data(self, **kwargs):
        context = super(ContractorContractDetailView, self).get_context_data(**kwargs)
        contract_id = self.kwargs['pk']
        context['concepts'] = ContractConcepts.objects.filter(Q(contract__id=contract_id))
        # Getting, if exists, the advance payment for the contract
        try:
            estimate = Estimate.objects.get(contract__id=contract_id)
        except Estimate.DoesNotExist:
            estimate = None

        advance_payment = None
        advance_payment_status = ""

        if estimate:
            advance_payment = estimate.advance_payment_amount

        if advance_payment == None:
            advance_payment = "No se ha registrado un anticipo."
            advance_payment_status = "Estatus no disponible."
        else:
            advance_payment = Utilities.number_to_currency(advance_payment)
            advance_payment_status = estimate.get_advance_payment_status_display()

        context['advance_payment'] = advance_payment
        context['advance_payment_status'] = advance_payment_status

        return context

    def dispatch(self, request, *args, **kwargs):
        contract_id = kwargs['pk']
        project_id = ContratoContratista.objects.get(pk=contract_id).project_id
        user = request.user
        user_has_access = AccessToProject.user_has_access_to_project(user.id, project_id)
        if user_has_access and user.has_perm('ERP.view_list_contratocontratista'):
            return super(ContractorContractDetailView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


# Views for the model Propietaro.
class OwnerListView(ListView):
    model = Propietario
    template_name = "ERP/owner-list.html"
    query = None
    title_list = "Propietarios"
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
        context['title_list'] = OwnerListView.title_list
        context['query'] = OwnerListView.query
        context['query_string'] = '&q=' + OwnerListView.query
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
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,x
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
    title_list = 'Catálogo de '
    add_url = "/admin/ERP/"
    url_c = "uploadedcatalogshistory/add/?project="
    url_i = "uploadedinputexplotionshistory/add/?project="

    current_type = 'C'
    current_type_full = 'conceptos'

    types_dict = {
        'conceptos': 'C',
        'insumos': 'I'
    }

    """
       Display a Blog List page filtered by the search query.
    """

    def get_queryset(self):
        result = super(LineItemListView, self).get_queryset()

        # Reading the params from the url.
        LineItemListView.project_id = int(self.kwargs['project'])
        LineItemListView.parent_id = int(self.kwargs['parent'])
        LineItemListView.current_type = self.types_dict[self.kwargs['type']]
        LineItemListView.current_type_full = self.kwargs['type']

        print "The type is:"
        print LineItemListView.current_type

        # If the param for the parent is received as 0, then its value must be None.
        if LineItemListView.parent_id == 0:
            LineItemListView.parent_id = None

        print "The filters:"
        print "Project Id: " + str(LineItemListView.project_id)
        print "Parent Id: " + str(LineItemListView.parent_id)


        # Filtering the results.
        result = result.filter(
            Q(project__id=LineItemListView.project_id) & Q(parent_line_item__id=LineItemListView.parent_id))



        # Query to filter the list content.
        query = self.request.GET.get('q')

        if query:
            LineItemListView.query = query
            query_list = query.split()
            # result = result.filter(
            #     reduce(operator.and_,
            #            (Q(key__icontains=q) for q in query_list)) |
            #     reduce(operator.and_,
            #            (Q(description__icontains=q) for q in query_list))
            # )
        else:
            LineItemListView.query = ''

        for element in result:
            element.can_be_deleted = element.can_be_deleted()

        return result

    def dispatch(self, request, *args, **kwargs):
        user_has_access = AccessToProject.user_has_access_to_project(request.user.id, kwargs['project'])
        user = request.user
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(LineItemListView, self).dispatch(request, args, kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(LineItemListView, self).get_context_data(**kwargs)
        context['title_list'] = LineItemListView.title_list + LineItemListView.current_type_full
        context['project_id'] = LineItemListView.project_id
        context['query'] = LineItemListView.query
        context['query_string'] = '&q=' + LineItemListView.query
        context['has_query'] = (LineItemListView.query is not None) and (LineItemListView.query != "")
        context['current_type_full'] = LineItemListView.current_type_full

        # Getting the concept inputs for the selected Line Item parent.
        ciqs = Concept_Input.objects.filter(
            Q(line_item=LineItemListView.parent_id) & Q(type=LineItemListView.current_type))

        for item in ciqs:
            item.total = Utilities.number_to_currency(item.quantity * item.unit_price)

        context['concepts_inputs'] = ciqs

        if LineItemListView.parent_id is not None:
            context['parent_line_item'] = LineItem.objects.get(pk=LineItemListView.parent_id)

        if LineItemListView.current_type == 'C':
            context['add_url'] = LineItemListView.add_url + LineItemListView.url_c + str(LineItemListView.project_id)
        else:
            context['add_url'] = LineItemListView.add_url + LineItemListView.url_i + str(LineItemListView.project_id)

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
    title_list = "Proyectos"

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        user_id = self.request.user.id
        access_set = AccessToProject.objects.filter(user_id=user_id)

        projects_array = []
        for access in access_set:
            projects_array.append(access.project.id)

        result = super(ProjectListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            ProjectListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombreProyecto__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(ubicacion_calle__icontains=q) for q in query_list)))

        else:
            ProjectListView.query = ''

        if len(projects_array) > 0:
            result = result.filter(reduce(operator.or_, (Q(pk=q) for q in projects_array)))
        else:
            result = Project.objects.none()

        return result

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['title_list'] = ProjectListView.title_list
        context['query'] = ProjectListView.query
        context['query_string'] = '&q=' + ProjectListView.query
        context['has_query'] = (ProjectListView.query is not None) and (ProjectListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_project'):
            raise PermissionDenied
        return super(ProjectListView, self).dispatch(request, args, kwargs)


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "ERP/project-detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project_obj = context['project']

        # Getting the files name.
        context['documento_gravamen_nombre'] = str(project_obj.documento_gravamen.name).split("/")[-1]
        context['documento_propiedad_nombre'] = str(project_obj.documento_propiedad.name).split("/")[-1]
        context['documento_agua_nombre'] = str(project_obj.documento_agua.name).split("/")[-1]
        context['documento_predial_nombre'] = str(project_obj.documento_predial.name).split("/")[-1]
        context['documento_hidraulica_nombre'] = str(project_obj.hidraulica_documento.name).split("/")[-1]
        context['documento_sanitaria_nombre'] = str(project_obj.sanitaria_documento.name).split("/")[-1]
        context['documento_pluvial_nombre'] = str(project_obj.pluvial_documento.name).split("/")[-1]
        context['documento_vial_nombre'] = str(project_obj.vial_documento.name).split("/")[-1]
        context['documento_electricidad_nombre'] = str(project_obj.electricidad_documento.name).split("/")[-1]
        context['documento_alumbrado_nombre'] = str(project_obj.alumbradopublico_documento.name).split("/")[-1]
        context['documento_telefonia_nombre'] = str(project_obj.telefonia_documento.name).split("/")[-1]

        # Getting the info for the contractors relates to a project.
        context['contracts'] = ContratoContratista.objects.filter(Q(project__id=project_obj.id))

        # Getting the settings for the current project, to know which card details to show.
        project_sections = ProjectSections.objects.filter(
            Q(project_id=project_obj.id) & Q(section__parent_section=None))
        sections_result = []
        for section in project_sections:
            section_json = {
                "section_name": section.section.section_name,
                "section_id": section.section.id,
                "total_inner_sections": 0,
                "inner_sections": []
            }
            i = 0
            inner_sections = ProjectSections.objects.filter(
                Q(project_id=project_obj.id) & Q(section__parent_section=section.section) & Q(status=1))
            for inner_section in inner_sections:
                inner_json = {
                    "inner_section_name": inner_section.section.section_name,
                    "inner_section_id": inner_section.section.id,
                    "inner_section_status": inner_section.status,
                }
                i += 1
                section_json["inner_sections"].append(inner_json)
            section_json["total_inner_sections"] = i
            sections_result.append(section_json)
        print sections_result
        context['sections_result'] = sections_result

        print str(project_obj.documento_propiedad.name).split("/")[-1]

        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        user_has_access = AccessToProject.user_has_access_to_project(user.id, kwargs['pk'])
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(ProjectDetailView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


class ProgressEstimateLogListView(ListView):
    model = ProgressEstimateLog
    template_name = "ERP/progressestimatelog-list.html"
    # search_fields = ("empresaNombre",)
    query = None
    title_list = "Bitácoras"
    add_url = "/admin/ERP/progressestimatelog/add?project="

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ProgressEstimateLogListView, self).get_queryset()

        query = self.request.GET.get('q')
        project_id = self.request.GET.get('project')

        result = result.filter(Q(project_id=project_id))

        if query:
            ProgressEstimateLogListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(project__nombreProyecto__icontains=q) for q in query_list))
            )
        else:
            ProjectListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        project_id = self.request.GET.get('project')
        context = super(ProgressEstimateLogListView, self).get_context_data(**kwargs)
        context['query'] = ProgressEstimateLogListView.query
        context['title_list'] = ProgressEstimateLogListView.title_list
        if project_id is not None:
            context['add_url'] = ProgressEstimateLogListView.add_url + project_id

        if (ProgressEstimateLogListView.query is not None):
            context['query_string'] = '&q=' + ProgressEstimateLogListView.query
        else:
            context['query_string'] = ''

        context['has_query'] = (ProgressEstimateLogListView.query is not None) and (
            ProgressEstimateLogListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        project_id = request.GET.get('project')

        if project_id is None:
            raise PermissionDenied
        user = request.user
        user_has_access = AccessToProject.user_has_access_to_project(user.id, project_id)
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(ProgressEstimateLogListView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


'''class ProgressEstimateLogDetailView(generic.DetailView):
    model = ProgressEstimateLog
    template_name = "ERP/progressestimatelog-detail.html"'''


class ProgressEstimateLogDetailView(generic.DetailView):
    model = ProgressEstimateLog
    template_name = "ERP/progressestimatelog-detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProgressEstimateLogDetailView, self).get_context_data(**kwargs)
        progressestimatelog = context['progressestimatelog']
        print 'the id log id:' + str(progressestimatelog)
        log_files = LogFile.objects.filter(Q(progress_estimate_log_id=progressestimatelog.id))
        for record in log_files:
            file_name = record.file.name
            split_name = file_name.split('/')

            if len(split_name) <= 1:
                record.version = "Archivo sin nombre"
            else:
                record.version = split_name[len(split_name) - 1]

        context['logfiles'] = log_files

        return context

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = ProgressEstimateLog.objects.get(pk=pk).project

        if project is None:
            raise PermissionDenied

        user = request.user
        user_has_access = AccessToProject.user_has_access_to_project(user.id, project.id)
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(ProgressEstimateLogDetailView, self).dispatch(request, args, kwargs)

        raise PermissionDenied


# Views for the model Estimate.
class EstimateListView(ListView):
    model = Estimate
    template_name = "ERP/estimate-list.html"
    query = None
    project_id = None
    params = ""
    title_list = "Estimación"
    add_url = "/admin/ERP/estimate/add?project="

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):

        print "URL is:"

        result = super(EstimateListView, self).get_queryset()
        EstimateListView.project_id = int(self.kwargs['project'])

        # Filtering the results by the current project.


        # Query params for the estimates.
        query = Q()

        # Must filter by project id.
        query = query & Q(contract__project__id=EstimateListView.project_id)

        params_copy = self.request.GET.copy()
        params_copy.pop('page', None)

        EstimateListView.params = urllib.urlencode(params_copy)

        line_item = self.request.GET.get('line_item')
        if line_item is not None and line_item is not "":
            query = query & Q(contract__line_item__id=line_item)

        start_date = self.request.GET.get('start_date')
        if start_date is not None:
            query_date = datetime.datetime.strptime(start_date, Constants.DATE_FORMAT).date()
            query = query & Q(start_date__gte=query_date)

        end_date = self.request.GET.get('end_date')
        if end_date is not None:
            query_date = datetime.datetime.strptime(end_date, Constants.DATE_FORMAT).date()
            query = query & Q(start_date__lte=query_date)

        contractor = self.request.GET.get('contractor')
        if contractor is not None and contractor is not "":
            query = query & Q(contract__contratista__id=contractor)

        if query is not None:
            print "Query: "
            print query
            result = result.filter(query)

        return result

    def get_context_data(self, **kwargs):
        project_id = self.request.GET.get('project')
        context = super(EstimateListView, self).get_context_data(**kwargs)
        context['project'] = EstimateListView.project_id
        context['params'] = EstimateListView.params
        context['title_list'] = EstimateListView.title_list
        context['form'] = EstimateSearchForm(EstimateListView.project_id)
        context['add_url'] = EstimateListView.add_url + str(EstimateListView.project_id)

        context['add_form'] = AddEstimateForm(EstimateListView.project_id)

        AddEstimateFormSet = formset_factory(AddEstimateForm)

        context['formset'] = AddEstimateFormSet()

        return context

    def dispatch(self, request, *args, **kwargs):
        user_has_access = AccessToProject.user_has_access_to_project(request.user.id, kwargs['project'])
        user = request.user
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(EstimateListView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


class EstimateDelete(DeleteView):
    model = Estimate
    success_url = ""

    # template_name = "ERP/estimate_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm('ERP.delete_estimate'):
            return super(EstimateDelete, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        print "About to delete."
        obj = self.get_object()
        project_id = obj.contract.project.id
        EstimateDelete.success_url = "/admin/ERP/estimate/list/" + str(project_id)
        return super(EstimateDelete, self).delete(request, *args, **kwargs)


class EstimateDetailView(generic.DetailView):
    model = Estimate
    template_name = "ERP/estimate-detail.html"

    def get_context_data(self, **kwargs):
        context = super(EstimateDetailView, self).get_context_data(**kwargs)

        # Shallow copy for the main object.
        estimate = context['estimate']
        estimate.deduction_amount = Utilities.number_to_currency(estimate.deduction_amount)
        contract_amount = estimate.contract.monto_contrato
        estimate.contract.monto_contrato = Utilities.number_to_currency(estimate.contract.monto_contrato)
        estimate.contract_amount_override = Utilities.number_to_currency(estimate.contract_amount_override)

        progress_estimates = ProgressEstimate.objects.filter(Q(estimate_id=estimate.id))

        total = estimate.advance_payment_amount
        context['advance_percentage'] = "{0:.0f}%".format(total / contract_amount * 100)

        estimate.advance_payment_amount = locale.currency(estimate.advance_payment_amount, grouping=True)

        current_user_can_approve = estimate.user_can_approve(self.request.user.id)
        context['current_user_can_approve'] = current_user_can_approve
        estimate.show_approval_button = not estimate.has_been_approved_by(
            self.request.user.id) and current_user_can_approve

        for record in progress_estimates:
            total += record.amount
            record.amount = locale.currency(record.amount, grouping=True)
            percentage = total / contract_amount
            record.progress = "{0:.0f}%".format(percentage * 100)

            record.show_approval_button = not record.has_been_approved_by(
                self.request.user.id) and current_user_can_approve

        context['progress_estimates'] = progress_estimates

        # Get the concepts specified for the contract
        concepts = estimate.contract.contractconcepts_set.all()

        context['contract_concepts'] = concepts

        return context

    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            liquidation_amount = request.POST.get('liquidation_amount')
            print liquidation_amount

        return super(EstimateDetailView, self).get(request, args, kwargs)

    def dispatch(self, request, *args, **kwargs):
        estimate_id = kwargs['pk']
        project_id = Estimate.objects.get(pk=estimate_id).contract.project_id
        user_has_access = AccessToProject.user_has_access_to_project(request.user.id, project_id)
        user = request.user
        if user_has_access and user.has_perm('ERP.view_list_project'):
            return super(EstimateDetailView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


class DashBoardView(ListView):
    model = Project
    template_name = "ERP/dashboard_project.html"
    project_id = None

    def get_queryset(self):
        # Reading the params from the url.
        DashBoardView.project_id = int(self.kwargs['project'])
        print "The id:"
        print DashBoardView.project_id

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context['project_id'] = DashBoardView.project_id
        context['project'] = Project.objects.filter(Q(id=DashBoardView.project_id))
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        user_has_access_to_project = AccessToProject.user_has_access_to_project(user.id, kwargs['project'])
        print 'access:' + str(user_has_access_to_project)
        if user_has_access_to_project and user.has_perm('ERP.view_list_project'):
            return super(DashBoardView, self).dispatch(request, args, kwargs)
        raise PermissionDenied


# Views for the model UploadedInputExplotionsHistory.
class UploadedInputExplotionsHistoryListView(ListView):
    model = UploadedInputExplotionsHistory
    template_name = "ERP/uploadedinputexplotionshistory-list.html"
    query = None
    title_list = "Carga de Explosión de Insumos"
    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(UploadedInputExplotionsHistoryListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            UploadedInputExplotionsHistoryListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(file__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(upload_date__icontains=q) for q in query_list))
            )
        else:
            UploadedInputExplotionsHistoryListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(UploadedInputExplotionsHistoryListView, self).get_context_data(**kwargs)
        context['title_list'] = UploadedInputExplotionsHistoryListView.title_list
        context['query'] = UploadedInputExplotionsHistoryListView.query
        context['query_string'] = '&q=' + UploadedInputExplotionsHistoryListView.query
        context['has_query'] = (UploadedInputExplotionsHistoryListView.query is not None) and (
            UploadedInputExplotionsHistoryListView.query != "")
        return context


# Views for the model UploadedCatalogsHistory.
class UploadedCatalogsHistoryAdminListView(ListView):
    model = UploadedCatalogsHistory
    template_name = "ERP/uploadedcatalogshistoryadmin-list.html"
    query = None
    title_list = "Carga de Catálogo de Conceptos"
    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(UploadedCatalogsHistoryAdminListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            UploadedCatalogsHistoryAdminListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(concepts_file__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(line_items_file__icontains=q) for q in query_list))
            )
        else:
            UploadedCatalogsHistoryAdminListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(UploadedCatalogsHistoryAdminListView, self).get_context_data(**kwargs)
        context['title_list'] = UploadedCatalogsHistoryAdminListView.title_list
        context['query'] = UploadedCatalogsHistoryAdminListView.query
        context['query_string'] = '&q=' + UploadedCatalogsHistoryAdminListView.query
        context['has_query'] = (UploadedCatalogsHistoryAdminListView.query is not None) and (
            UploadedCatalogsHistoryAdminListView.query != "")
        return context


# Views for the model AccessToProjectAdmin.
class AccessToProjectAdminListView(ListView):
    model = AccessToProject
    template_name = "ERP/accesstoproject-list.html"
    query = None
    title_list = "Acceso a Proyectos"
    """
       Display a Project List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):

        result = super(AccessToProjectAdminListView, self).get_queryset()
        user = int(self.request.GET.get('user'))

        query = Q()
        query = query & Q(user_id=int(user))
        result = result.filter(query)

        query = self.request.GET.get('q')
        if query:
            AccessToProjectAdminListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(project__nombreProyecto__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(project__empresa__nombreEmpresa__icontains=q) for q in query_list))
            )
        else:
            AccessToProjectAdminListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(AccessToProjectAdminListView, self).get_context_data(**kwargs)
        context['title_list'] = AccessToProjectAdminListView.title_list
        context['query'] = AccessToProjectAdminListView.query
        context['query_string'] = '&q=' + AccessToProjectAdminListView.query
        context['has_query'] = (AccessToProjectAdminListView.query is not None) and (
            AccessToProjectAdminListView.query != "")

        context['user_id'] = self.request.GET.get('user')

        return context


# Views for the model Propietaro.
class ContactListView(ListView):
    model = Contact
    template_name = "ERP/contact-list.html"
    query = None
    title_list = "Contactos"
    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ContactListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            ContactListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__contains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(rfc__icontains=q) for q in query_list))
            )
        else:
            ContactListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        context['title_list'] = ContactListView.title_list
        context['query'] = ContactListView.query
        context['query_string'] = '&q=' + ContactListView.query
        context['has_query'] = (ContactListView.query is not None) and (ContactListView.query != "")
        return context


class ContactDetailView(generic.DetailView):
    model = Contact
    template_name = "ERP/contact-detail.html"


def apply_deductions_to_estimate(request):
    # Form
    if request.method == 'POST':
        # This post comes from another place, so we just have estimate_id
        estimate_id = request.POST.get('estimate_id')
        if estimate_id is None:
            raise PermissionDenied
        form = EstimateDedutionsForm()
        form.fields['estimate_id'].initial = estimate_id
    else:
        raise PermissionDenied
    return render(request, 'ERP/apply_deductions_to_estimate.html', {'form': form})


def save_deductions_to_estimate(request):
    # Save
    if request.method == 'POST':
        estimate_id = request.POST.get('estimate_id')
        if estimate_id is None:
            raise PermissionDenied

        # Save Estimate....
        estimate_qs = Estimate.objects.filter(id=estimate_id)
        if len(estimate_qs) == 0:
            raise PermissionDenied


        form = EstimateDedutionsForm(request.POST)

        if not form.is_valid():
            return render(request, 'ERP/apply_deductions_to_estimate.html', {'form': form})

        estimate = estimate_qs[0]
        estimate.lock_status = 'U'
        estimate.deduction_comments = request.POST.get('deduction_comments')
        estimate.deduction_amount = request.POST.get('deduction_amount')
        estimate.save()

        return HttpResponseRedirect('/admin/ERP/estimate/' + estimate_id + '/')
    else:
        raise PermissionDenied
