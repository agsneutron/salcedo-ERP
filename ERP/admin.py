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


class LogFileInline(admin.TabularInline):
    model = LogFile
    extra = 0


class ProgressEstimateLogAdmin(admin.ModelAdmin):
    fields = ('description', 'date')
    list_display = ('user', 'description', 'date')
    search_fields = ('user', 'description', 'date')
    list_display_links = ('user', 'description', 'date')
    list_per_page = 50

    inlines = [
        LogFileInline,
    ]


class ProgressEstimateInline(admin.TabularInline):
    model = ProgressEstimate
    extra = 0


class EstimateAdmin(admin.ModelAdmin):
    list_display = ('get_concept_and_line_item', 'start_date', 'end_date')
    search_fields = ('start_date', 'end_date')
    list_display_links = ('start_date', 'end_date')
    list_per_page = 50
    inlines = [
        ProgressEstimateInline
    ]
    form = EstimateForm
    fieldsets = (
        (
            'Concepto', {
                'fields': ('line_item_filter', 'concept_master',)
        }),
        (
            'Estimación', {
                'fields': ('start_date', 'end_date',)
        }),
    )

    def get_concept_and_line_item(self, obj):
        if obj.concept_master is not None:
            return obj.concept_master.line_item.description + " - " + obj.concept_master.description
        else:
            return "-"

    get_concept_and_line_item.short_description = "Concepto"


class ConceptMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'description')
    search_fields = ('key', 'description')
    list_display_links = ('key', 'description')
    list_per_page = 50


class ConceptDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'status', 'quantity', 'unit_price')
    search_fields = ('unit', 'status', 'quantity', 'unitPrice')
    list_display_links = ('unit', 'status', 'quantity', 'unit_price')
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
    list_display = ('id', 'nombreContratista', 'rfc')
    search_fields = ('nombreContratista', 'rfc')
    list_display_links = ('id', 'nombreContratista', 'rfc')
    list_per_page = 50


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreEmpresa', 'rfc')
    search_fields = ('nombreEmpresa', 'rfc')
    list_display_links = ('id', 'nombreEmpresa', 'rfc')
    list_per_page = 50


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_obra', 'objeto_contrato')
    search_fields = ('codigo_obra', 'objeto_contrato')
    list_display_links = ('id', 'codigo_obra', 'objeto_contrato')
    list_per_page = 50


class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePropietario', 'empresa')
    search_fields = ('nombrePropietario', 'empresa')
    list_display_links = ('id', 'nombrePropietario', 'empresa')
    list_per_page = 50


admin.site.register(Project, ProjectAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Estimate, EstimateAdmin)
admin.site.register(ConceptMaster, ConceptMasterAdmin)
admin.site.register(ConceptDetail, ConceptDetailAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(ProgressEstimateLog, ProgressEstimateLogAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Contratista, ContratistaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Propietario, PropietarioAdmin)
