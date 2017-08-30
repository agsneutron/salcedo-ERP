# coding=utf-8
from __future__ import unicode_literals

import django
from django.conf.urls import url
from django.contrib import messages
from django.db import transaction

from DataUpload.helper import DBObject, ErrorDataUpload
from ERP import views
from ERP.models import *
from ERP.forms import TipoProyectoDetalleAddForm, AddProyectoForm, DocumentoFuenteForm, EstimateForm

from django.contrib import admin

# Register your models here.
# Modificacion del admin de Region para la parte de catalogos
from ERP.views import CompaniesListView, ContractorListView
from SalcedoERP.lib.SystemLog import LoggingConstants


class DocumentoFuenteInline(admin.TabularInline):
    model = DocumentoFuente
    extra = 2
    form = DocumentoFuenteForm


class TipoProyectoDetalleInline(admin.TabularInline):
    form = TipoProyectoDetalleAddForm
    model = TipoProyectoDetalle
    extra = 1
    can_delete = False


class ProjectAdmin(admin.ModelAdmin):
    form = AddProyectoForm
    inlines = (TipoProyectoDetalleInline,)
    search_fields = ('nombreProyecto', 'key')


class LineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)
    search_fields = ('description',)
    list_display_links = ('description',)
    list_per_page = 50


class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'progress_estimate_log', 'file', 'mime',)
    fields = ('id', 'progress_estimate_log', 'file', 'mime',)
    model = LogFile


class LogFileInline(admin.TabularInline):
    list_display = ('id', 'progress_estimate_log', 'file', 'mime',)
    fields = ('id', 'progress_estimate_log', 'file', 'mime',)
    model = LogFile
    extra = 1


class ProgressEstimateLogAdmin(admin.ModelAdmin):
    fields = ('user', 'project', 'description', 'date')
    list_display = ('user', 'description', 'date')
    search_fields = ('user', 'description', 'date')
    list_display_links = ('user', 'description', 'date')
    list_per_page = 50
    inlines = [LogFileInline, ]


class ProgressEstimateInline(admin.TabularInline):
    model = ProgressEstimate
    extra = 0


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
    list_display = ('id', 'codigo_obra', 'objeto_contrato')
    search_fields = ('codigo_obra', 'objeto_contrato')
    list_display_links = ('id', 'codigo_obra', 'objeto_contrato')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = (
            'no_licitacion', 'modalidad_contrato', 'dependencia', 'codigo_obra', 'contratista', 'dias_pactados',
            'fecha_firma',
            'fecha_inicio', 'fecha_termino', 'monto_contrato', 'monto_contrato_iva', 'pago_inicial', 'pago_final',
            'objeto_contrato', 'lugar_ejecucion', 'observaciones')
        return fields


class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePropietario', 'email', 'empresa', 'telefono1')
    search_fields = ('nombrePropietario', 'empresa')
    list_display_links = ('id', 'nombrePropietario', 'empresa')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = (
            'nombrePropietario', 'rfc', 'empresa', 'email', 'telefono1', 'telefono2', 'pais', 'estado', 'municipio',
            'cp',
            'calle', 'numero', 'colonia')
        return fields


class ProgressEstimateAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'key', 'progress', 'amount', 'type', 'generator_file')
    fields = ('estimate', 'key', 'progress', 'amount', 'type', 'generator_file')
    model = ProgressEstimate


class UploadedCatalogsHistoryAdmin(admin.ModelAdmin):
    model = UploadedCatalogsHistory
    fields = ('project', 'line_items_file', 'concepts_file')
    list_display = ('project', 'line_items_file', 'concepts_file', 'upload_date')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        user_id = request.user.id
        print "se intentó 1"
        dbo = DBObject(user_id)

        try:
            with transaction.atomic():
                project_id = request.POST.get('project')

                print 'about to save line_items'
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
            print 'Hubo un error de integridad'
            edu = ErrorDataUpload(str(e), LoggingConstants.ERROR, user_id)
            messages.set_level(request, messages.ERROR)
            messages.error(request, edu.get_error_message())


class UploadedInputExplotionHistoryAdmin(admin.ModelAdmin):
    model = UploadedInputExplotionsHistory

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


# Overriding the admin views to provide a detail view as required.

@admin.register(Empresa)
class CompanyModelAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = (
            'nombreEmpresa', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp', 'calle',
            'numero', 'colonia')
        return fields

    def get_urls(self):
        urls = super(CompanyModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(CompaniesListView.as_view()), name='company-list-view'),
            url(r'^(?P<pk>\d+)/$', views.CompanyDetailView.as_view(), name='company-detail'),

        ]
        return my_urls + urls


@admin.register(Contratista)
class ContractorModelAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = (
            'nombreContratista', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp',
            'calle',
            'numero', 'colonia')
        return fields

    def get_urls(self):
        urls = super(ContractorModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(ContractorListView.as_view()), name='contractor-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ContractorDetailView.as_view(), name='contractor-detail'),
        ]

        return my_urls + urls


@admin.register(ContratoContratista)
class ContractorContractModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ContractorContractModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.ContractorContractListView.as_view()),
                name='contractor-contract-list-view'),
            url(r'^(?P<pk>\d+)/$', views.ContractorContractDetailView.as_view(), name='contractor-contract-detail'),

        ]
        return my_urls + urls


@admin.register(Propietario)
class OwnerModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(OwnerModelAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(views.OwnerListView.as_view()),
                name='owner-list-view'),
            url(r'^(?P<pk>\d+)/$', views.OwnerDetailView.as_view(), name='propietario-detail'),

        ]
        return my_urls + urls


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(LineItemAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<project>[0-9]+)/(?P<parent>[0-9]+)/$',
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


# Simple admin views.
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(TipoConstruccion)
admin.site.register(ModalidadContrato)
admin.site.register(UploadedCatalogsHistory, UploadedCatalogsHistoryAdmin)
admin.site.register(UploadedInputExplotionsHistory, UploadedInputExplotionHistoryAdmin)

admin.site.register(Project, ProjectAdmin)

# admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Estimate, EstimateAdmin)
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
