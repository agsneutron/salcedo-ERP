# coding=utf-8
from __future__ import unicode_literals
from ERP.models import *

from django.contrib import admin

# Register your models here.
# Modificacion del admin de Region para la parte de catalogos
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'key','name',)
    search_fields = ('key','name',)
    list_display_links = ('id', 'key', 'name',)
    list_per_page = 50

class LineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)
    search_fields = ('description',)
    list_display_links = ('description',)
    list_per_page = 50


class EstimateAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date','end_date')
    search_fields = ('start_date','end_date')
    list_display_links = ('start_date','end_date')
    list_per_page = 50


class ConceptMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'description')
    search_fields = ('key', 'description')
    list_display_links = ('key', 'description')
    list_per_page = 50


class ConceptDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'status','quantity','unitPrice')
    search_fields = ('unit', 'status','quantity','unitPrice')
    list_display_links = ('unit', 'status','quantity','unitPrice')
    exclude = ('end_date',)
    list_per_page = 50



class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    list_display_links = ('name', 'abbreviation')
    list_per_page = 50


admin.site.register(Project, ProjectAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Estimate, EstimateAdmin)
admin.site.register(ConceptMaster, ConceptMasterAdmin)
admin.site.register(ConceptDetail, ConceptDetailAdmin)
admin.site.register(Unit, UnitAdmin)
