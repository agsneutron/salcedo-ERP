# coding=utf-8
from __future__ import unicode_literals
from ERP.models import *
from ERP.forms import TipoProyectoDetalleAddForm, AddProyectoForm, DocumentoFuenteForm, EstimateForm

from django.contrib import admin


# Register your models here.
# Modificacion del admin de Region para la parte de catalogos
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


class LineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)
    search_fields = ('description',)
    list_display_links = ('description',)
    list_per_page = 50


class ProgressEstimateLogAdmin(admin.ModelAdmin):
    fields = ('user','progress_estimate','description', 'date')
    list_display = ('user', 'description', 'date')
    search_fields = ('user', 'description', 'date')
    list_display_links = ('user', 'description', 'date')
    list_per_page = 50


class ProgressEstimateInline(admin.TabularInline):
    model = ProgressEstimate
    extra = 0


class EstimateAdmin(admin.ModelAdmin):
    list_display = ('period','start_date', 'end_date')
    search_fields = ('period','start_date', 'end_date')
    list_per_page = 50
    inlines = [
        ProgressEstimateInline
    ]
    form = EstimateForm
    fieldsets = (
        (
            'Concepto', {
                'fields': ('line_item_filter', )
        }),
        (
            'Estimación', {
                'fields': ('period','start_date', 'end_date',)
        }),
    )



class ConceptDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'quantity', 'unit_price')
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


class ContratistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreContratista', 'rfc', 'estado')
    search_fields = ('nombreContratista', 'rfc')
    list_display_links = ('id', 'nombreContratista', 'rfc')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = ('nombreContratista', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp', 'calle', 'numero', 'colonia')
        return fields


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreEmpresa', 'rfc', 'telefono')
    search_fields = ('nombreEmpresa', 'rfc')
    list_display_links = ('id', 'nombreEmpresa', 'rfc')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = ('nombreEmpresa', 'rfc', 'email', 'telefono', 'telefono_dos', 'pais', 'estado', 'municipio', 'cp', 'calle', 'numero', 'colonia')
        return fields


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_obra', 'objeto_contrato')
    search_fields = ('codigo_obra', 'objeto_contrato')
    list_display_links = ('id', 'codigo_obra', 'objeto_contrato')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = (
        'no_licitacion', 'modalidad_contrato', 'dependencia', 'codigo_obra', 'contratista', 'dias_pactados', 'fecha_firma',
        'fecha_inicio', 'fecha_termino', 'monto_contrato', 'monto_contrato_iva', 'pago_inicial', 'pago_final', 'objeto_contrato', 'lugar_ejecucion', 'observaciones')
        return fields


class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePropietario', 'email', 'empresa', 'telefono1')
    search_fields = ('nombrePropietario', 'empresa')
    list_display_links = ('id', 'nombrePropietario', 'empresa')
    list_per_page = 50

    def get_fields(self, request, obj=None):
        fields = ('nombrePropietario', 'rfc', 'empresa', 'email','telefono1', 'telefono2', 'pais', 'estado', 'municipio', 'cp', 'calle', 'numero', 'colonia')
        return fields


class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'progress_estimate_log', 'file', 'mime',)
    fields = ('id', 'progress_estimate_log', 'file', 'mime',)
    model = LogFile


class ProgressEstimateAdmin(admin.ModelAdmin):
    list_display = ('id', 'estimate', 'key', 'progress','amount', 'type', )
    fields = ('id', 'estimate', 'key', 'progress','amount', 'type', )
    model = ProgressEstimate


# Simple admin views.
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(TipoConstruccion)
admin.site.register(ModalidadContrato)

admin.site.register(Project, ProjectAdmin)

admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Estimate, EstimateAdmin)
admin.site.register(Concept_Input, ConceptDetailAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(ProgressEstimateLog, ProgressEstimateLogAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Contratista, ContratistaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Propietario, PropietarioAdmin)
admin.site.register(ProgressEstimate, ProgressEstimateAdmin )
admin.site.register(LogFile, LogFileAdmin)
