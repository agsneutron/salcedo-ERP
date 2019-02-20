# coding=utf-8
from __future__ import unicode_literals

import django
from django.conf.urls import url
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import redirect

from django import forms

from DataUpload.helper import DBObject, ErrorDataUpload
from ERP import views
from ERP.models import *
from ERP.forms import TipoProyectoDetalleAddForm, AddProyectoForm, DocumentoFuenteForm, EstimateForm, ContractForm, \
    ContactForm, ContractConceptsForm, ProgressEstimateForm
from ERP.forms import TipoProyectoDetalleAddForm, AddProyectoForm, DocumentoFuenteForm, EstimateForm, \
    ProgressEstimateLogForm, OwnerForm

from django.contrib import admin
from django.http import HttpResponseRedirect

# Register your models here.
# Modificacion del admin de Region para la parte de catalogos
from ERP.views import CompaniesListView, ContractorListView, ProjectListView, ProgressEstimateLogListView, \
    EstimateListView, UploadedInputExplotionsHistoryListView, UploadedCatalogsHistoryAdminListView, \
    AccessToProjectAdminListView
from SalcedoERP.lib.SystemLog import LoggingConstants


class DocumentoFuenteInline(admin.TabularInline):
    model = DocumentoFuente
    extra = 2
    form = DocumentoFuenteForm


class TipoProyectoDetalleInline(admin.TabularInline):
    form = TipoProyectoDetalleAddForm
    model = TipoProyectoDetalle
    extra = 0
    can_delete = True


# class ProjectAdmin(admin.ModelAdmin):
#    form = AddProyectoForm
#    inlines = (TipoProyectoDetalleInline,)
#    search_fields = ('nombreProyecto', 'key')


class LineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)
    search_fields = ('description',)
    list_display_links = ('description',)
    list_per_page = 50


class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'progress_estimate_log', 'file',)
    fields = ('id', 'progress_estimate_log', 'file', 'version',)
    model = LogFile


class LogFileInline(admin.TabularInline):
    list_display = ('id', 'progress_estimate_log', 'file',)
    fields = ('id', 'progress_estimate_log', 'file', 'version',)
    model = LogFile
    extra = 0


class ProgressEstimateLogAdmin(admin.ModelAdmin):
    form = ProgressEstimateLogForm
    fields = ('user', 'project', 'date', 'description', 'version', 'status')
    list_display = ('user', 'date', 'description')
    search_fields = ('user', 'date', 'description')
    list_display_links = ('user', 'date', 'description')
    list_per_page = 50
    inlines = [LogFileInline, ]

    def get_form(self, request, obj=None, **kwargs):
        ModelFormE = super(ProgressEstimateLogAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project')

        if project_id is None:
            raise PermissionDenied

        project_qs = Project.objects.filter(id=project_id)

        project = ModelFormE.base_fields['project']

        project.queryset = project_qs

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        project.widget.can_add_related = False
        project.widget.can_change_related = False

        class ModelFormEMetaClass(ModelFormE):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['project_id'] = request.GET.get('project')
                kwargs['user_id'] = request.user.id
                return ModelFormE(*args, **kwargs)

        return ModelFormEMetaClass

    def get_urls(self):
        urls = super(ProgressEstimateLogAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(ProgressEstimateLogListView.as_view()),
                name='progressestimatelog-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ProgressEstimateLogDetailView.as_view(), name='progressestimatelog-detail'),

        ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/progressestimatelog/?project=' + project_id)
        else:
            return super(ProgressEstimateLogAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/progressestimatelog/?project=' + project_id)
        else:
            return super(ProgressEstimateLogAdmin, self).response_add(request, obj, post_url_continue)

    # here
    def has_add_permission(self, request):
        project_id = request.GET.get('project')
        if project_id is None:
            return False
        else:
            user = request.user
            user_has_access = AccessToProject.user_has_access_to_project(user.id, project_id)
            if user_has_access and user.has_perm('ERP.view_list_project'):
                return True
            return False

    def has_change_permission(self, request, obj=None):
        user = request.user

        if user.has_perm('ERP.change_progressestimatelog') and user.has_perm('ERP.view_list_project'):
            if obj is not None:
                return AccessToProject.user_has_access_to_project(user.id, obj.project_id)
            else:
                return True
        else:
            return False


class ProgressEstimateInline(admin.TabularInline):
    model = ProgressEstimate
    extra = 1


'''
class EstimateAdmin(admin.ModelAdmin):
    form = EstimateForm
    list_display = ('line_item', 'concept_input', 'period', 'start_date', 'end_date')
    search_fields = ('line_item', 'concept_input', 'period', 'start_date', 'end_date')
    list_per_page = 50

    inlines = [
        ProgressEstimateInline
    ]
    fieldsets = (
        (
            'Partida', {
                'fields': ('line_item',)
            }),
        (
            'Estimación', {
                'fields': ('concept_input', 'period', 'start_date', 'end_date',)
            }),
    )

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EstimateAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        line_item = ModelForm.base_fields['line_item']
        concept_input = ModelForm.base_fields['concept_input']
        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        line_item.widget.can_add_related = False
        line_item.widget.can_change_related = False
        concept_input.widget.can_add_related = False
        concept_input.widget.can_change_related = False

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass
'''


class ConceptInputAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'unit', 'quantity', 'unit_price')
    search_fields = ('unit', 'quantity', 'unitPrice')
    list_display_links = ('unit', 'quantity', 'unit_price')
    exclude = ('end_date',)
    list_per_page = 50


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    list_display_links = ('name', 'abbreviation')
    list_per_page = 50


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreEmpleado', 'rfc')
    search_fields = ('nombreEmpleado', 'rfc')
    list_display_links = ('id', 'nombreEmpleado', 'rfc')
    list_per_page = 50


#
# class ContratistaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nombreContratista', 'rfc', 'email', 'estado', 'municipio')
#     search_fields = ('nombreContratista', 'rfc', 'estado__nombreEstado', 'email', 'municipio__nombreMunicipio')
#     list_display_links = ('id', 'nombreContratista', 'rfc')
#     list_per_page = 50
#
#     def get_fields(self, request, obj=None):
#         fields = (
#             'nombreContratista', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp',
#             'calle',
#             'numero', 'colonia')
#         return fields


# class EmpresaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nombreEmpresa', 'rfc', 'telefono')
#     search_fields = ('nombreEmpresa', 'rfc')
#     list_display_links = ('id', 'nombreEmpresa', 'rfc')
#     list_per_page = 50
#
#     def get_fields(self, request, obj=None):
#         fields = (
#             'nombreEmpresa', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp', 'calle',
#             'numero', 'colonia')
#         return fields


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'objeto_contrato')
    search_fields = ('objeto_contrato')
    list_display_links = ('id', 'objeto_contrato')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = (
            'no_licitacion', 'modalidad_contrato', 'dependencia', 'contratista', 'dias_pactados',
            'fecha_firma',
            'fecha_inicio', 'fecha_termino', 'monto_contrato', 'monto_contrato_iva', 'pago_inicial', 'pago_final',
            'objeto_contrato', 'lugar_ejecucion', 'observaciones', 'version', 'line_item')
        return fields


'''
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePropietario', 'email', 'empresa', 'telefono1')
    search_fields = ('nombrePropietario', 'empresa')
    list_display_links = ('id', 'nombrePropietario', 'empresa')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = (
            'nombrePropietario', 'rfc', 'email', 'telefono1', 'telefono2', 'pais', 'estado', 'municipio',
            'cp', 'calle', 'numero', 'colonia', 'version',)
        return fields

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(PropietarioAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['pais']
        estado = ModelForm.base_fields['estado']
        municipio = ModelForm.base_fields['municipio']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False

        return ModelForm
'''


class ProgressEstimateAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'key', 'amount', 'generator_file', 'payment_status')
    fields = ('estimate', 'key', 'amount', 'generator_file', 'payment_status', 'version',)
    model = ProgressEstimate

    form = ProgressEstimateForm

    def response_change(self, request, obj):
        """This makes the response after adding go to another apps changelist for some model"""
        return HttpResponseRedirect('/admin/ERP/estimate/' + str(obj.estimate.id))

    def response_add(self, request, obj, post_url_continue=None):
        """This makes the response after adding go to another apps changelist for some model"""
        return HttpResponseRedirect('/admin/ERP/estimate/' + str(obj.estimate.id))

    def get_form(self, request, obj=None, **kwargs):

        if obj is not None:
            estimate_id = obj.estimate.id
        else:
            estimate_id = request.GET.get('estimate')

        form = super(ProgressEstimateAdmin, self).get_form(request, obj, **kwargs)

        if estimate_id is not None:
            qs = Estimate.objects.filter(pk=estimate_id)
            if qs.exists():
                estimate = qs[0]
                form.contract_amount = estimate.contract.monto_contrato

                accumulated = estimate.get_accumulated_amount()

                form.contract_amount_accumulated = "{0:.2f}%".format(
                    accumulated / estimate.contract.monto_contrato * 100)

        amount_field = form.base_fields['amount']
        amount_field.widget = forms.NumberInput(attrs={'step': .1})

        if obj is None and estimate_id is not None:
            qs = Estimate.objects.filter(pk=estimate_id)
            if qs.exists():

                estimate_field = form.base_fields['estimate']
                estimate_field.queryset = Estimate.objects.filter(pk=estimate_id)

                estimate_field.widget.can_add_related = False
                estimate_field.widget.can_change_related = False


            else:
                raise Http404(
                    'No existe la estimación especificada.')
        elif obj is not None:
            estimate_field = form.base_fields['estimate']
            estimate_field.queryset = Estimate.objects.filter(pk=obj.estimate.id)

            estimate_field.widget.can_add_related = False
            estimate_field.widget.can_change_related = False

            if not request.user.has_perm('ERP.can_unlock_estimate') and obj.type == ProgressEstimate.SETTLEMENT:
                amount_field.widget.attrs['readonly'] = True

            if obj.type == ProgressEstimate.PROGRESS and obj.estimate.lock_status == Estimate.UNLOCKED:
                amount_field.widget.attrs['readonly'] = True

        else:
            raise Http404(
                'No existe esta página. Para editar una estimación, hazlo a través de las opciones del sistema.')

        return form

    def get_urls(self):
        urls = super(ProgressEstimateAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/approve', views.approve_progress_estimate, name='progress-estimate-approve'),
        ]
        return my_urls + urls

    def save_model(self, request, obj, form, change):

        return super(ProgressEstimateAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        estimate_id = request.GET.get('estimate')
        if estimate_id is None:
            return False
        else:
            estimate = Estimate.objects.get(pk=estimate_id)
            user = request.user
            user_has_access = AccessToProject.user_has_access_to_project(user.id, estimate.contract.project_id)
            if user_has_access and user.has_perm('ERP.view_list_project') and user.has_perm('ERP.add_progressestimate'):
                return True
            return False

    def has_change_permission(self, request, obj=None):
        user = request.user

        if user.has_perm('ERP.change_progressestimate'):
            if obj is not None:
                user_has_access = AccessToProject.user_has_access_to_project(user.id, obj.estimate.contract.project_id)
                if user_has_access and user.has_perm('ERP.view_list_project') and user.has_perm(
                        'ERP.change_progressestimate') and obj.payment_status == ProgressEstimate.NOT_PAID:
                    return True
                return False
            else:
                return False
        else:
            return False


class AccessToProjectAdmin(admin.ModelAdmin):
    model = AccessToProject

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(AccessToProjectAdmin, self).get_form(request, obj, **kwargs)

        # Field objects.
        user_field = ModelForm.base_fields['user']
        project_field = ModelForm.base_fields['project']

        user = request.GET.get('user')
        projects_set = AccessToProject.objects.filter(user__id=user).values('project__id')

        projects_array = []

        for project in projects_set:
            projects_array.append(project['project__id'])

        available_projects = Project.objects.exclude(Q(id__in=projects_array))

        if not available_projects.exists():
            custom_message = "No hay proyectos pendientes de asignación para el usuario actual."
            messages_list = messages.get_messages(request)

            if len(messages_list) <= 0:
                messages.error(request, custom_message)

        project_field.queryset = available_projects

        # Remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        user_field.widget.can_add_related = False
        user_field.widget.can_change_related = False

        return ModelForm

    def response_add(self, request, obj, post_url_continue=None):
        user_id = request.GET.get('user')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/accesstoproject/?user=' + user_id)
        else:
            return super(AccessToProjectAdmin, self).response_add(request, obj, post_url_continue)

    def get_urls(self):
        urls = super(AccessToProjectAdmin, self).get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(AccessToProjectAdminListView.as_view()),
                name='accesstoproject-list-view'),
        ]
        return my_urls + urls

    def response_delete(self, request, obj_display, obj_id):
        user_id = request.GET.get('user')

        return HttpResponseRedirect("/admin/ERP/accesstoproject/?user=" + str(user_id))


class UploadedCatalogsHistoryAdmin(admin.ModelAdmin):
    model = UploadedCatalogsHistory
    fields = ('project', 'line_items_file', 'concepts_file', 'version')
    list_display = ('project', 'line_items_file', 'concepts_file', 'upload_date')
    list_per_page = 50

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(UploadedCatalogsHistoryAdmin, self).get_form(request, obj, **kwargs)

        project_id = request.GET.get('project')

        # Fet the field for the project to restrict.
        project = ModelForm.base_fields['project']
        project.queryset = Project.objects.filter(pk=project_id)

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        project.widget.can_add_related = False
        project.widget.can_change_related = False

        return ModelForm

    def save_model(self, request, obj, form, change):
        user_id = request.user.id
        dbo = DBObject(user_id)

        try:
            with transaction.atomic():
                project_id = request.POST.get('project')

                dbo.save_all(request.FILES['line_items_file'],
                             dbo.LINE_ITEM_UPLOAD, project_id)
                dbo.save_all(request.FILES['concepts_file'],
                             dbo.CONCEPT_UPLOAD, project_id)
                super(UploadedCatalogsHistoryAdmin, self).save_model(request, obj, form, change)

        except ErrorDataUpload as e:
            e.save()
            messages.set_level(request, messages.ERROR)
            messages.error(request, e.get_error_message())
        except django.db.utils.IntegrityError as e:
            # Create exception without raising it.

            edu = ErrorDataUpload(str(e), LoggingConstants.ERROR, user_id)
            messages.set_level(request, messages.ERROR)
            messages.error(request, edu.get_error_message())

    def get_urls(self):
        urls = super(UploadedCatalogsHistoryAdmin, self).get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(UploadedCatalogsHistoryAdminListView.as_view()),
                name='uploadedcatalogshistoryadmin-list-view'),
        ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/uploadedcatalogshistory/?project=' + project_id)
        else:
            return super(UploadedCatalogsHistoryAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/uploadedcatalogshistory/?project=' + project_id)
        else:
            return super(UploadedCatalogsHistoryAdmin, self).response_add(request, obj, post_url_continue)

    def has_add_permission(self, request):
        project_id = request.GET.get('project')
        if project_id is None:
            return False
        else:
            user_has_access = AccessToProject.user_has_access_to_project(request.user.id, project_id)
            if user_has_access:
                return True
            return False


class UploadedInputExplotionHistoryAdmin(admin.ModelAdmin):
    model = UploadedInputExplotionsHistory

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(UploadedInputExplotionHistoryAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        project = ModelForm.base_fields['project']
        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        project.widget.can_add_related = False
        project.widget.can_change_related = False

        return ModelForm

    def get_fields(self, request, obj=None):
        fields = (
            'project', 'file', 'version',)
        return fields

    def save_model(self, request, obj, form, change):
        user_id = request.user.id
        dbo = DBObject(user_id)
        try:
            with transaction.atomic():
                project_id = request.POST.get('project')

                dbo.save_all(request.FILES['file'],
                             dbo.INPUT_UPLOAD, project_id)
                super(UploadedInputExplotionHistoryAdmin, self).save_model(request, obj, form, change)


        except django.db.utils.IntegrityError as e:
            # Create exception without raising it.
            edu = ErrorDataUpload(str(e.__cause__), LoggingConstants.ERROR, user_id)
            messages.set_level(request, messages.ERROR)
            messages.error(request, edu.get_error_message())
        except ErrorDataUpload as e:
            e.save()
            messages.set_level(request, messages.ERROR)
            messages.error(request, e.get_error_message())

    def get_urls(self):
        urls = super(UploadedInputExplotionHistoryAdmin, self).get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(UploadedInputExplotionsHistoryListView.as_view()),
                name='uploadedinputexplotionshistory-list-view'),

        ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/uploadedinputexplotionshistory/?project=' + project_id)
        else:
            return super(UploadedInputExplotionHistoryAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/uploadedinputexplotionshistory/?project=' + project_id)
        else:
            return super(UploadedInputExplotionHistoryAdmin, self).response_add(request, obj, post_url_continue)


# Overriding the admin views to provide a detail view as required.
class OwnerInline(admin.StackedInline):
    model = Propietario
    extra = 1
    can_delete = True

    def get_fields(self, request, obj=None):
        fields = (
            'nombrePropietario', 'rfc', 'email', 'telefono1', 'telefono2', 'pais', 'estado', 'municipio',
            'cp', 'calle', 'numero', 'colonia', 'version',)
        return fields

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(OwnerInline, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['pais']
        estado = ModelForm.base_fields['estado']
        municipio = ModelForm.base_fields['municipio']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False

        return ModelForm


# Overriding the admin views to provide a detail view as required.
class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    can_delete = True


@admin.register(Empresa)
class CompanyModelAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = (
            'nombreEmpresa', 'rfc', 'type', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp',
            'calle',
            'numero', 'colonia', 'version',)
        return fields

    def get_urls(self):
        urls = super(CompanyModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(CompaniesListView.as_view()), name='company-list-view'),
            url(r'^(?P<pk>\d+)/$', views.CompanyDetailView.as_view(), name='company-detail'),

        ]
        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CompanyModelAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['pais']
        estado = ModelForm.base_fields['estado']
        municipio = ModelForm.base_fields['municipio']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False

        return ModelForm


class ContactInline(admin.StackedInline):
    model = Contact
    extra = 1

    def get_fields(self, request, obj=None):
        fields = (
            'name', 'rfc', 'email', 'phone_number_1', 'phone_number_2', 'country', 'state', 'town', 'post_code',
            'street', 'number', 'colony', 'version', 'contractor')
        return fields

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(ContactInline, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        country = ModelForm.base_fields['country']
        state = ModelForm.base_fields['state']
        town = ModelForm.base_fields['town']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        country.widget.can_add_related = False
        country.widget.can_change_related = False
        state.widget.can_add_related = False
        state.widget.can_change_related = False
        town.widget.can_add_related = False
        town.widget.can_change_related = False

        return ModelForm


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    form = ContactForm

    def get_fields(self, request, obj=None):
        fields = (
            'name', 'rfc', 'contractor', 'email', 'phone_number_1', 'phone_number_2', 'country', 'state', 'town',
            'post_code',
            'street', 'number', 'colony', 'is_legal_representantive', 'version',)
        return fields

    def get_urls(self):
        urls = super(ContactModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.ContactListView.as_view()),
                name='contact-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ContactDetailView.as_view(), name='contact-detail'),

        ]
        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):

        ModelForm = super(ContactModelAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['country']
        estado = ModelForm.base_fields['state']
        municipio = ModelForm.base_fields['town']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['contratista_id'] = request.GET.get('contratista_id')
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect("/admin/ERP/contratista/" + str(obj.contractor.id))
        else:
            return super(ContactModelAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        return HttpResponseRedirect("/admin/ERP/contratista/" + str(obj.contractor.id))


@admin.register(Contratista)
class ContractorModelAdmin(admin.ModelAdmin):
    # inlines = (ContactInline, )

    def get_fields(self, request, obj=None):
        fields = (
            'nombreContratista', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp',
            'calle',
            'numero', 'colonia', 'employer_registration_number', 'infonavit', 'tax_person_type', 'services', 'version',
            'bank', 'bank_account_name', 'bank_account') #'CLABE'
        return fields

    def get_urls(self):
        urls = super(ContractorModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(ContractorListView.as_view()), name='contractor-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ContractorDetailView.as_view(), name='contractor-detail'),
        ]

        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(ContractorModelAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['pais']
        estado = ModelForm.base_fields['estado']
        municipio = ModelForm.base_fields['municipio']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False

        return ModelForm


@admin.register(ContratoContratista)
class ContractorContractModelAdmin(admin.ModelAdmin):
    form = ContractForm

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(ContractorContractModelAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        project = ModelForm.base_fields['project']
        contratista = ModelForm.base_fields['contratista']
        modalidad_contrato = ModelForm.base_fields['modalidad_contrato']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        project.widget.can_add_related = False
        project.widget.can_change_related = False
        contratista.widget.can_add_related = False
        contratista.widget.can_change_related = False
        modalidad_contrato.widget.can_add_related = False
        modalidad_contrato.widget.can_change_related = False

        project_ids = AccessToProject.get_projects_for_user(request.user.id)
        ModelForm.base_fields['project'].queryset = Project.objects.filter(pk__in=project_ids)

        return ModelForm

    def get_fields(self, request, obj=None):
        fields = (
            'clave_contrato', 'project', 'contratista', 'no_licitacion',
            'modalidad_contrato', 'dependencia', 'porcentaje_iva', 'assigment_number',
            'fecha_firma', 'fecha_inicio','fecha_termino_propuesta', 'fecha_termino_real',
            'objeto_contrato', 'lugar_ejecucion', 'observaciones', 'version')
        return fields

    def get_urls(self):
        urls = super(ContractorContractModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.ContractorContractListView.as_view()),
                name='contractor-contract-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ContractorContractDetailView.as_view(), name='contractor-contract-detail'),

        ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue="../%s/"):
        return HttpResponseRedirect("/admin/ERP/contratocontratista/" + str(obj.id) + "/change/?contrato=" + str(obj.id))

    def has_add_permission(self, request):
        if request.user.has_perm('ERP.add_contratocontratista'):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        user = request.user

        if user.has_perm('ERP.change_contratocontratista'):
            if obj is not None:
                return AccessToProject.user_has_access_to_project(user.id, obj.project_id)
            else:
                return True
        else:
            return False


class ConceptForContractsInlines(admin.TabularInline):
    model = Concept_Input


@admin.register(ContractConcepts)
class ContractConceptsAdmin(admin.ModelAdmin):
    form = ContractConceptsForm

    def get_amounts_per_contract(self, contract_id):
        line_item_id = PartidasContratoContratista.objects.get(pk=contract_id).line_item.id

        concepts = Concept_Input.objects.filter(line_item_id=line_item_id)
        response = []

        for c in concepts:
            contract_concept = ContractConcepts.objects.filter(Q(concept_id=c.id))

            if len(contract_concept) == 0:
                response.append({'key': str(c.id), 'amount': str(c.quantity) + ' ' + c.unit.abbreviation,
                                 'resting': str(c.quantity) + ' ' + c.unit.abbreviation})
            else:
                contracted_amount = contract_concept[0].amount
                response.append(
                    {'key': str(c.id), 'amount': str(c.quantity), 'resting': str(c.quantity - contracted_amount)})
        return response

    def get_form(self, request, obj=None, **kwargs):

        ModelForm = super(ContractConceptsAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['contract_id'] = request.GET.get('contract_id')
                self.form.amounts_per_concept = self.get_amounts_per_contract(kwargs['contract_id'])
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect("/admin/ERP/contratocontratista/" + str(obj.contract.id))
        else:
            return HttpResponseRedirect(
                "/admin/ERP/contractconcepts/" + str(obj.id) + "/change/?contract_id=" + str(obj.contract.id))

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if '_continue' not in request.POST:
            return HttpResponseRedirect("/admin/ERP/contratocontratista/" + str(obj.contract.id))
        else:
            return HttpResponseRedirect(
                "/admin/ERP/contractconcepts/" + str(obj.id) + "/change/?contract_id=" + str(obj.contract.id))

    def response_delete(self, request, obj_display, obj_id):
        contract_id = request.contract_id

        return HttpResponseRedirect("/admin/ERP/contratocontratista/" + str(contract_id))

    def delete_model(self, request, obj):
        request.contract_id = obj.contract_id
        return super(ContractConceptsAdmin, self).delete_model(request,obj)

@admin.register(Propietario)
class OwnerModelAdmin(admin.ModelAdmin):
    form = OwnerForm

    def get_urls(self):
        urls = super(OwnerModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.OwnerListView.as_view()),
                name='owner-list-view'),
            url(r'^(?P<pk>\d+)/$', views.OwnerDetailView.as_view(), name='propietario-detail'),

        ]
        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):

        ModelForm = super(OwnerModelAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        pais = ModelForm.base_fields['pais']
        estado = ModelForm.base_fields['estado']
        municipio = ModelForm.base_fields['municipio']
        empresa = ModelForm.base_fields['empresa']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        pais.widget.can_add_related = False
        pais.widget.can_change_related = False
        estado.widget.can_add_related = False
        estado.widget.can_change_related = False
        municipio.widget.can_add_related = False
        municipio.widget.can_change_related = False
        empresa.widget.can_add_related = False
        empresa.widget.can_change_related = False

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['company_id'] = request.GET.get('empresa_id')
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect("/admin/ERP/empresa/" + str(obj.empresa.id))
        else:
            return super(OwnerModelAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if '_continue' not in request.POST:
            return HttpResponseRedirect("/admin/ERP/empresa/" + str(obj.empresa.id))
        else:
            return super(OwnerModelAdmin, self).response_add(request, obj, post_url_continue)

    def response_delete(self, request, obj_display, obj_id):
        empresa_id = request.GET.get('empresa_id')
        return HttpResponseRedirect("/admin/ERP/empresa/" + str(empresa_id))


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(LineItemAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<type>conceptos|insumos)/(?P<project>[0-9]+)/(?P<parent>[0-9]+)/$',
                self.admin_site.admin_view(views.LineItemListView.as_view()),
                name='concept-input-view'),
            url(r'^(?P<pk>\d+)/$', views.LineItemDetailView.as_view(), name='concept-input-detail'),

        ]
        return my_urls + urls


@admin.register(Concept_Input)
class ConceptInputAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ConceptInputAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.ConceptInputListView.as_view()),
                name='concept-input-view'),
            url(r'^(?P<pk>\d+)/$', views.ConceptInputDetailView.as_view(), name='concept-input-detail'),

        ]
        return my_urls + urls


class PaymentScheduleInline(admin.TabularInline):
    model = PaymentSchedule
    extra = 0
    ordering = ("year", "month")
    fields = ('project', 'year', 'month', 'amount')


class BlueprintInline(admin.TabularInline):
    model = Blueprint
    extra = 1
    fields = ('file','description')


@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    inlines = (TipoProyectoDetalleInline, PaymentScheduleInline, BlueprintInline)
    exclude = None

    @staticmethod
    def get_project_settings(project_id):
        # Getting the settings for the current project, to know which card details to show.

        project_obj = Project.objects.get(pk=project_id)

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
                Q(project_id=project_obj.id) & Q(section__parent_section=section.section))
            for inner_section in inner_sections:
                inner_json = {
                    "inner_section_name": inner_section.section.section_name,
                    "inner_section_id": inner_section.section.id,
                    "inner_section_status": inner_section.status,
                    "inner_section_short_name": inner_section.section.short_section_name
                }
                if inner_section.status == 1:
                    i += 1
                section_json["inner_sections"].append(inner_json)
            section_json["total_inner_sections"] = i
            sections_result.append(section_json)

        return sections_result

    def get_urls(self):
        urls = super(ProjectModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(ProjectListView.as_view()), name='project-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project-detail'),
            url(r'^dashboard/(?P<project>[0-9]+)/$', views.DashBoardView.as_view(), name='project-dashboard'),
        ]

        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):

        self.exclude = None

        if obj:
            sections_dictionary = {
                'legal': [
                    'estadolegal_documento_propiedad',
                    'estadolegal_gravamen',
                    'estadolegal_predial',
                    'estadolegal_agua',
                    'documento_propiedad',
                    'documento_gravamen',
                    'documento_agua',
                    'documento_predial',
                    'documento_agua'
                ],
                'afectacion': [
                    'programayarea_afectacion',
                    'programayarea_documento'
                ],
                'programas_y_areas': [
                    'programayarea_areaprivativa',
                    'programayarea_caseta',
                    'programayarea_jardin',
                    'programayarea_vialidad',
                    'programayarea_areaverde',
                    'programayarea_estacionamientovisita'
                ],
                'definicion_de_proyecto': [
                    'definicionproyecto_alternativa',
                    'definicionproyecto_tamano',
                    'definicionproyecto_programa'
                ],
                'estudio_mercado': [
                    'estudiomercado_demanda',
                    'estudiomercado_oferta',
                    'estudiomercado_conclusiones',
                    'estudiomercado_recomendaciones'
                ],
                'costo': [
                    'costo_predio',
                    'costo_m2',
                    'costo_escrituras',
                    'costo_levantamiento'
                ],
                'telefonia': [
                    'telefonia_distancia',
                    'telefonia_observaciones',
                    'telefonia_documento'
                ],
                'tv_y_cable': [
                    'tvcable_distancia',
                    'tvcable_observaciones'
                ],
                'equipamiento': [
                    'equipamiento_a100',
                    'equipamiento_a200',
                    'equipamiento_a500',
                    'equipamiento_regional'
                ],
                'alambrado_publico': [
                    'alumbradopublico_tipo',
                    'alumbradopublico_distancia',
                    'alumbradopublico_observaciones',
                    'alumbradopublico_documento'
                ],
                'electricidad': [
                    'electricidad_tipo',
                    'electricidad_distancia',
                    'electricidad_observaciones',
                    'electricidad_documento'
                ],
                'vial': [
                    'vial_viaacceso',
                    'vial_distancia',
                    'vial_carriles',
                    'vial_seccion',
                    'vial_tipopavimento',
                    'vial_estadoconstruccion',
                    'vial_observaciones',
                    'vial_documento'
                ],
                'pluvial': [
                    'pluvial_tipo',
                    'pluvial_responsable',
                    'pluvial_observaciones',
                    'pluvial_documento'
                ],
                'sanitaria': [
                    'sanitaria_tipo',
                    'sanitaria_responsable',
                    'sanitaria_observaciones',
                    'sanitaria_documento'
                ],
                'hidraulica': [
                    'hidraulica_fuente',
                    'hidraulica_distancia',
                    'hidraulica_observaciones',
                    'hidraulica_documento'
                ],
                'uso_de_suelo': [
                    'usosuelo_pmdu',
                    'usosuelo_densidad',
                    'usosuelo_loteminimo',
                    'usosuelo_m2construccion',
                    'usosuelo_arealibre',
                    'usosuelo_altura',
                    'usosuelo_densidadrequerida'
                ],
                'restricciones_detalle': [
                    'restriccion_vial',
                    'restriccion_cna',
                    'restriccion_cfe',
                    'restriccion_pemex',
                    'restriccion_inha',
                    'restriccion_otros',
                    'restriccion_observaciones'
                ]
            }
            fields_to_exclude = []

            # This means we are not trying to add a new project, but to edit an existing one.
            sections = ProjectModelAdmin.get_project_settings(obj.id)

            for top_section in sections:
                for inner_section in top_section['inner_sections']:
                    if inner_section['inner_section_status'] == 0 and inner_section['inner_section_short_name'] in sections_dictionary:
                        fields_to_exclude += sections_dictionary[inner_section['inner_section_short_name']]

            if len(fields_to_exclude) > 0:
                self.exclude = fields_to_exclude
        else:
            self.exclude = None

        return super(ProjectModelAdmin, self).get_form(request, obj, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        project_id = object_id
        sections_result = ProjectModelAdmin.get_project_settings(project_id)
        extra['sections_result'] = sections_result

        return super(ProjectModelAdmin, self).change_view(request, object_id,
                                                          form_url, extra_context=extra)

    def has_change_permission(self, request, obj=None):
        user = request.user

        print 'User id: ' + str(user.id)
        print 'User has perm:' + str(user.has_perm('ERP.change_project'))

        if user.has_perm('ERP.change_project'):
            if obj is not None:
                return AccessToProject.user_has_access_to_project(user.id, obj.id)
            else:
                return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        user = request.user
        print obj
        if user.has_perm('ERP.delete_project'):
            if obj is not None:
                return AccessToProject.user_has_access_to_project(user.id, obj.id)
            else:
                return True
        else:
            return False


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    form = EstimateForm
    list_per_page = 50

    fieldsets = (
        (
            'Contrato', {
                'fields': ('contract',)
            }),
        (
            'Estimación', {
                'fields': (
                    'period', 'start_date', 'end_date', 'advance_payment_amount', 'Total_paid',
                    'advance_payment_date',
                    'advance_payment_status', 'version')
            }),
    )

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EstimateAdmin, self).get_form(request, obj, **kwargs)
        # get the foreign key field I want to restrict
        contract = ModelForm.base_fields['contract']

        # remove the green + and change icons by setting can_change_related and can_add_related to False on the widget
        contract.widget.can_add_related = False
        contract.widget.can_change_related = False

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def get_urls(self):
        urls = super(EstimateAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            url(r'^list/(?P<project>[0-9]+)/$',
                self.admin_site.admin_view(views.EstimateListView.as_view()),
                name='estimate-view'),
            url(r'^(?P<pk>\d+)/unlock$', views.unlock_estimate, name='estimate-detail'),
            url(r'^(?P<pk>\d+)/$', views.EstimateDetailView.as_view(), name='estimate-detail'),
            url(r'^(?P<pk>\d+)/delete/$', views.EstimateDelete.as_view(), name='estimate-delete'),
            url(r'^(?P<pk>\d+)/approve', views.approve_estimate_advance, name='estimate-advance-approve'),
            url(r'^apply_deductions_to_estimate', views.apply_deductions_to_estimate),
            url(r'^save_deductions_to_estimate', views.save_deductions_to_estimate),

        ]

        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST:
            project_id = request.GET.get('project')
            return HttpResponseRedirect('/admin/ERP/estimate/' + str(obj.id) + '/')
        else:
            return super(EstimateAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj, post_url_continue=None):
        project_id = request.GET.get('project')
        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/ERP/estimate/' + str(obj.id) + '/')
        else:
            return super(EstimateAdmin, self).response_add(request, obj, post_url_continue)

    def has_add_permission(self, request):
        project_id = request.GET.get('project')
        if project_id is None:
            return False
        else:
            user = request.user
            user_has_access = AccessToProject.user_has_access_to_project(user.id, project_id)
            if user_has_access and user.has_perm('ERP.view_list_project') and user.has_perm('ERP.add_estimate'):
                return True
            return False

    def has_change_permission(self, request, obj=None):
        user = request.user

        if user.has_perm('ERP.change_estimate'):
            if obj is not None:
                return AccessToProject.user_has_access_to_project(user.id, obj.contract.project_id)
            else:
                return True
        else:
            return False


# Simple admin views.
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(TipoConstruccion)
admin.site.register(ModalidadContrato)
admin.site.register(UploadedCatalogsHistory, UploadedCatalogsHistoryAdmin)
admin.site.register(UploadedInputExplotionsHistory, UploadedInputExplotionHistoryAdmin)

# admin.site.register(Project, ProjectAdmin)

# admin.site.register(LineItem, LineItemAdmin)
# admin.site.register(Estimate, EstimateAdmin)
# admin.site.register(Concept_Input, ConceptInputAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(ProgressEstimateLog, ProgressEstimateLogAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
# admin.site.register(Contratista, ContratistaAdmin)
# admin.site.register(Empresa, EmpresaAdmin)
# admin.site.register(ContratoContratista, ContratoAdmin)
# admin.site.register(Propietario, PropietarioAdmin)
admin.site.register(ProgressEstimate, ProgressEstimateAdmin)
admin.site.register(LogFile, LogFileAdmin)
# admin.site.register(Contact, ContactModelAdmin)
admin.site.register(AccessToProject, AccessToProjectAdmin)
admin.site.register(Section)
admin.site.register(ProjectSections)
admin.site.register(Bank)
admin.site.register(DistribucionPago)
admin.site.register(DocumentacionContrato)
admin.site.register(PartidasContratoContratista)
