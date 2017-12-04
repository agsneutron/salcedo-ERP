# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from _mysql import IntegrityError

import django

import datetime
from datetime import date

# Django Libraries.
from django.conf.urls import url
from django.contrib import admin, messages

from Assistance.helper import AssistanceFileInterface, AssistanceDBObject, ErrorDataUpload

# Constants.
from SalcedoERP.lib.SystemLog import LoggingConstants

# DBObject assistant.
from Assistance.helper import AssistanceDBObject

# Atomic Transactions.
from django.db import transaction

# Importing the views.
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect

from HumanResources import views

# Importing the forms.
from HumanResources.forms import *

# Importing the models.
from HumanResources.models import *


class HumanResourcesAdminUtilities():
    @staticmethod
    def get_detail_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-eye color-default eliminar' > </i>"
        if model_name == "payrollgroup":
            button = "<i class ='fa fa-calendar-check-o color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_delete_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/delete"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-trash-o color-danger eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_change_link_with_employee(obj, employee_id):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/change?employee=" + str(employee_id)
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-pencil color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_nomina_link_with_employee(obj, employee_id):
        model_name = "employeeearningsdeductions"
        link = "/admin/HumanResources/" + model_name + "/add/?employee=" + str(employee_id)
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-address-card-o color-default' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_change_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/change"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-pencil color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_listpayroll_link(obj, payrollperiod_id, payrollgroup_id):
        model_name = obj.__class__.__name__.lower()
        link = "/humanresources/employeebyperiod/?payrollperiod=" + str(payrollperiod_id) + "&payrollgroup=" + str(
            payrollgroup_id)
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-list color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_EmployeeModelDetail_link(model_name,employee_id,anchor):
        link = "/admin/HumanResources/" + str(model_name) + "/" + str(employee_id) + "/"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-eye color-default eliminar' > </i>"

        return '<a href="' + link + anchor + '" class="' + css + '" >' + button + '</a>'


# Employee Admin.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm

    search_fields = ('^employee_key', '^name', '^type', '^registry_date', '^work_email', '^status', '^tags__name')

    list_display = ('employee_key', 'type', 'registry_date', 'status')

    fieldsets = (
        ("Datos de Empleado", {
            'fields': ('employee_key', 'type', 'registry_date', 'status', 'photo')
        }),
        ("Datos Personales", {
            'fields': (
                'name', 'first_last_name', 'second_last_name', 'birthdate', 'birthplace', 'gender', 'marital_status',
                'curp', 'rfc', 'tax_regime', 'blood_type', 'street', 'outdoor_number', 'indoor_number', 'colony',
                'country', 'state', 'town', 'zip_code', 'phone_number', 'cellphone_number', 'office_number',
                'extension_number', 'personal_email', 'work_email', 'driving_license_number',
                'driving_license_expiry_date')
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        keywords = search_term.split(" ")

        r = Employee.objects.none()

        for k in keywords:
            q, ud = super(EmployeeAdmin, self).get_search_results(request, queryset, k)
            r |= q

        return r, True

    def get_urls(self):
        urls = super(EmployeeAdmin, self).get_urls()

        my_urls = [
            # url(r'^$',
            #    self.admin_site.admin_view(ProgressEstimateLogListView.as_view()),
            #    name='progressestimatelog-list-view'),
            url(r'^(?P<pk>\d+)/$', views.EmployeeDetailView.as_view(), name='employee-detail'),

        ]
        return my_urls + urls

    list_display = (
        'employee_key', 'get_full_name', 'work_email', 'get_detail_column', 'get_change_column', 'get_delete_column',
        'get_payroll_column')
    list_display_links = None

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_detail_column(self, obj):
        return HumanResourcesAdminUtilities.get_detail_link(obj)

    def get_change_column(self, obj):
        return HumanResourcesAdminUtilities.get_change_link_with_employee(obj, obj.id)

    def get_delete_column(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    def get_payroll_column(self, obj):
        return HumanResourcesAdminUtilities.get_nomina_link_with_employee(obj, obj.id)

    # Added columns meta data.
    get_full_name.short_description = "Nombre"

    get_detail_column.allow_tags = True
    get_detail_column.short_description = 'Detalle'

    get_change_column.allow_tags = True
    get_change_column.short_description = 'Editar'

    get_delete_column.allow_tags = True
    get_delete_column.short_description = 'Eliminar'

    get_payroll_column.allow_tags = True
    get_payroll_column.short_description = 'Nómina'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        if employee_id != object_id:
            raise PermissionDenied

        employee = Employee.objects.get(pk=employee_id)
        extra['employee'] = employee
        return super(EmployeeAdmin, self).change_view(request, object_id, form_url, extra)

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = "/admin/HumanResources/employee/" + str(obj.id) + "/change/?employee=" + str(obj.id)
        return HttpResponseRedirect(redirect_url)

    def response_change(self, request, obj):
        redirect_url = "/admin/HumanResources/employee/" + str(obj.id) + "/change/?employee=" + str(obj.id)
        return HttpResponseRedirect(redirect_url)


# Education Admin.
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    form = EducationForm
    fieldsets = (
        ("Formación Académica", {
            'fields': ('type', 'name', 'institution', 'license_code', 'evidence', 'employee')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EducationAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        education_set = Education.objects.filter(employee_id=employee_id)

        extra['template'] = "education"
        extra['employee'] = employee
        extra['education'] = education_set

        return super(EducationAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/education/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/education/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/education/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Admin for the inline documents of the current education of an employee.
class CurrentEducationDocumentInline(admin.TabularInline):
    model = CurrentEducationDocument
    extra = 1


# Current Education Admin.
@admin.register(CurrentEducation)
class CurrentEducationAdmin(admin.ModelAdmin):
    form = CurrentEducationForm
    inlines = (CurrentEducationDocumentInline,)

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CurrentEducationAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Emergency Contact Admin.
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    form = EmergencyContactForm

    fieldsets = (
        ("Contactos de Emergencia", {
            'fields': (
                'name', 'first_last_name', 'second_last_name', 'phone_number', 'cellphone_number', 'email', 'employee')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmergencyContactAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass
        # Adding extra context to the change view.

    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        emergencycontact_set = EmergencyContact.objects.filter(employee_id=employee_id)

        extra['template'] = "emergencycontact"
        extra['employee'] = employee
        extra['emergencycontact'] = emergencycontact_set

        return super(EmergencyContactAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/emergencycontact/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/emergencycontact/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/emergencycontact/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Family Member Admin.
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    form = FamilyMemberForm

    fieldsets = (
        ("Familiares", {
            'fields': (
                'name', 'first_last_name', 'second_last_name', 'relationship', 'employee')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(FamilyMemberAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        family_member_set = FamilyMember.objects.filter(employee_id=employee_id)

        extra['template'] = "family_members"
        extra['employee'] = employee
        extra['family_member'] = family_member_set

        return super(FamilyMemberAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/familymember/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/familymember/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/familymember/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Work Reference Admin.
@admin.register(WorkReference)
class WorkReferenceAdmin(admin.ModelAdmin):
    form = WorkReferenceForm

    fieldsets = (
        ("Referencias", {
            'fields': (
                'name', 'first_last_name', 'second_last_name', 'company_name', 'first_phone_number',
                'second_phone_number', 'email', 'notes', 'employee')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(WorkReferenceAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the work reference admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        work_reference_set = WorkReference.objects.filter(employee_id=employee_id)

        extra['template'] = "work_reference"
        extra['employee'] = employee
        extra['work_reference'] = work_reference_set

        return super(WorkReferenceAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/workreference/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/workreference/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/workreference/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Test Application Admin.
@admin.register(TestApplication)
class TestApplicationAdmin(admin.ModelAdmin):
    form = TestApplicationForm

    fieldsets = (
        ("Pruebas Aplicadas", {
            'fields': (
                'application_date', 'result', 'test', 'comments', 'employee',)
        }),
    )

    list_display = ('test', 'employee', 'application_date','result','get_EmployeeModelDetail_link')
    list_display_links = None
    search_fields = (
        'employee__name', '^test__name', 'result')

    def get_EmployeeModelDetail_link(self, obj):
        return HumanResourcesAdminUtilities.get_EmployeeModelDetail_link("testapplication", obj.employee.id, "#pruebas")

    get_EmployeeModelDetail_link.short_description = 'Ver'
    get_EmployeeModelDetail_link.allow_tags = True

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(TestApplicationAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the tests admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        applications_set = TestApplication.objects.filter(employee_id=employee_id)

        extra['template'] = "applications"
        extra['employee'] = employee
        extra['applications'] = applications_set

        return super(TestApplicationAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/testapplication/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/testapplication/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/testapplication/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    def get_urls(self):
        urls = super(TestApplicationAdmin, self).get_urls()
        my_urls = [
            #url(r'^$', views.Tests, name='tests'),
            url(r'^(?P<pk>\d+)/$', views.TestApplicationDetail, name='test_application_detail'),
        ]
        return my_urls + urls


# Employee Document Admin.
@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    form = EmployeeDocumentForm

    fieldsets = (
        ("Documentación", {
            'fields': ('file', 'document_type', 'comments', 'employee',)
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeDocumentAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the employee document admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)
        documents_set = EmployeeDocument.objects.filter(employee_id=employee_id)

        extra['template'] = "documentation"
        extra['employee'] = employee
        extra['documentation'] = documents_set

        return super(EmployeeDocumentAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeedocument/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeedocument/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeedocument/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Checker Data Admin.
@admin.register(CheckerData)
class CheckerDataAdmin(admin.ModelAdmin):
    form = CheckerDataForm

    fieldsets = (
        ("Documentación", {
            'fields': ('checks_entry', 'checks_exit', 'employee',)
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CheckerDataAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the employee document admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        found_checker = request.GET.get('checker')

        extra['employee'] = Employee.objects.get(pk=employee_id)

        checker_data = CheckerData.objects.filter(employee_id=employee_id)

        if len(checker_data) > 0 and found_checker is None:
            # There's checker info for the current employee and found_checker control variable was not sent.
            return HttpResponseRedirect(
                "/admin/HumanResources/checkerdata/" + str(checker_data.first().id) + "/change?employee=" + str(
                    employee_id) + "&checker=1")

        return super(CheckerDataAdmin, self).add_view(request, form_url, extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/checkerdata/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/checkerdata/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/checkerdata/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        employee_id = request.GET.get('employee')
        checker_data = CheckerData.objects.filter(employee_id=employee_id)

        if len(checker_data) <= 0 or (int(object_id) != int(checker_data.first().id)):
            raise PermissionDenied

        extra['employee'] = Employee.objects.get(pk=employee_id)

        return super(CheckerDataAdmin, self).change_view(request, object_id, form_url, extra)


# Employee Has Tag Admin.
@admin.register(EmployeeHasTag)
class EmployeeHasTagAdmin(admin.ModelAdmin):
    form = EmployeeHasTagForm

    fieldsets = (
        ("Etiquetas", {
            'fields': ('employee', 'tag',)
        }),
    )

    list_display = ('tag','employee','get_EmployeeModelDetail_link')

    search_fields = (
        '^employee__name', 'tag__name',)

    model_name = str(object.__class__.__name__.lower())

    def get_EmployeeModelDetail_link(self,obj):
        return HumanResourcesAdminUtilities.get_EmployeeModelDetail_link("employee", obj.employee.id,"")


    get_EmployeeModelDetail_link.short_description = 'Ver'
    get_EmployeeModelDetail_link.allow_tags = True

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeHasTagAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

        # Overriding the add_wiew method for the employee document admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        employeehastag_set = EmployeeHasTag.objects.filter(employee_id=employee_id)

        extra['template'] = "employeehastag"
        extra['employee'] = Employee.objects.get(pk=employee_id)
        extra['employee_hastag'] = employeehastag_set

        return super(EmployeeHasTagAdmin, self).add_view(request, form_url, extra_context=extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeehastag/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeehastag/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeehastag/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# Employee Position Description Admin.
@admin.register(EmployeePositionDescription)
class EmployeePositionDescriptionAdmin(admin.ModelAdmin):
    form = EmployeePositionDescriptionForm
    fieldsets = (
        ("Descripción de Puesto", {
            # contract
            'fields': (
                'employee', 'start_date', 'end_date', 'direction', 'subdirection', 'area', 'department', 'job_profile',
                'physical_location', 'insurance_type', 'insurance_number', 'entry_time', 'departure_time', 'monday',
                'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'payroll_group', 'contract', 'observations',)
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeePositionDescriptionAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the employee position description admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        found_position = request.GET.get('position')

        extra['employee'] = Employee.objects.get(pk=employee_id)

        position_description_data = EmployeePositionDescription.objects.filter(employee_id=employee_id)

        if len(position_description_data) > 0 and found_position is None:
            return HttpResponseRedirect(
                "/admin/HumanResources/employeepositiondescription/" + str(
                    position_description_data.first().id) + "/change?employee=" + str(
                    employee_id) + "&position=1")

        return super(EmployeePositionDescriptionAdmin, self).add_view(request, form_url, extra_context=extra)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        position_description_data = EmployeePositionDescription.objects.filter(employee_id=employee_id)

        if len(position_description_data) <= 0 or (int(object_id) != int(position_description_data.first().id)):
            raise PermissionDenied

        extra['employee'] = Employee.objects.get(pk=employee_id)

        return super(EmployeePositionDescriptionAdmin, self).change_view(request, object_id, form_url, extra)

    # To redirect after object delete.
    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeepositiondescription/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeepositiondescription/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)

    # To redirect after object change
    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        redirect_url = "/admin/HumanResources/employeepositiondescription/add/?employee=" + str(employee_id)
        return HttpResponseRedirect(redirect_url)


# @admin.register(InfonavitData)
class InfonavitDataAdmin(admin.StackedInline):
    model = InfonavitData

    fieldsets = (
        ("Datos de Crédito Infonavit", {
            'fields': ('infonavit_credit_number', 'discount_type', 'discount_amount', 'start_date', 'credit_term',
                       'comments',)
        }),
    )
    # form = InfonavitDataForm
    #
    #
    # # Method to override some characteristics of the form.
    # def get_form(self, request, obj=None, **kwargs):
    #      ModelForm = super(InfonavitDataAdmin, self).get_form(request, obj, **kwargs)
    #
    #
    #      # Class to pass the request to the form.
    #      class ModelFormMetaClass(ModelForm):
    #          def __new__(cls, *args, **kwargs):
    #              kwargs['request'] = request
    #
    #              return ModelForm(*args, **kwargs)
    #
    #      return ModelFormMetaClass


@admin.register(EmployeeEarningsDeductionsbyPeriod)
class EmployeeEarningsDeductionsbyPeriodAdmin(admin.ModelAdmin):
    form = EmployeeEarningsDeductionsbyPeriodForm

    fieldsets = (
        ("Percepciones y Deducciones", {
            'fields': ('employee', 'concept', 'ammount', 'date', 'payroll_period',)
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeEarningsDeductionsbyPeriodAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        payrollperiod_id = request.GET.get('payrollperiod')
        employee_position = EmployeePositionDescription.objects.filter(employee_id=employee_id)
        employee_data = Employee.objects.filter(id=employee_id)
        earnings_set = EmployeeEarningsDeductions.objects.filter(employee_id=employee_id).filter(concept__type='P')
        deductions_set = EmployeeEarningsDeductions.objects.filter(employee_id=employee_id).filter(concept__type='D')
        earnings_by_period_set = EmployeeEarningsDeductionsbyPeriod.objects.filter(employee_id=employee_id).filter(
            concept__type='P').filter(payroll_period=payrollperiod_id)
        deductions_by_period_set = EmployeeEarningsDeductionsbyPeriod.objects.filter(employee_id=employee_id).filter(
            concept__type='D').filter(payroll_period=payrollperiod_id)
        payroll_set = PayrollPeriod.objects.filter(id=payrollperiod_id)

        extra['template'] = "employee_earnings_deductions"
        extra['payrolldata'] = payroll_set
        extra['employeedata'] = employee_data
        extra['employeeposition'] = employee_position
        extra['earnings'] = earnings_set
        extra['deductions'] = deductions_set
        extra['periodearnings'] = earnings_by_period_set
        extra['perioddeductions'] = deductions_by_period_set

        return super(EmployeeEarningsDeductionsbyPeriodAdmin, self).add_view(request, form_url, extra_context=extra)


    def response_delete(self, request, obj_display, obj_id):
        employee_id = request.GET.get('employee')
        payroll_period_id = request.GET.get('payrollperiod')
        django.contrib.messages.success(request, "Deducción borrada exitosamente.")

        return HttpResponseRedirect("http://localhost:8000/admin/HumanResources/employeeearningsdeductionsbyperiod/add/?employee="+employee_id+"&payrollperiod="+payroll_period_id)


    def response_change(self, request, obj):
        employee_id = request.GET.get('employee')
        payroll_period_id = request.GET.get('payrollperiod')
        django.contrib.messages.success(request, "La deducción se modificó exitosamente.")

        return HttpResponseRedirect(
            "http://localhost:8000/admin/HumanResources/employeeearningsdeductionsbyperiod/add/?employee=" + employee_id + "&payrollperiod=" + payroll_period_id)


@admin.register(EmployeeEarningsDeductions)
class EmployeeEarningsDeductionsAdmin(admin.ModelAdmin):
    form = EmployeeEarningsDeductionsForm

    fieldsets = (
        ("Percepciones y Deducciones", {
            'fields': ('employee', 'concept', 'ammount', 'date')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeEarningsDeductionsAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        earnings_set = EmployeeEarningsDeductions.objects.filter(employee_id=employee_id).filter(concept__type='P')
        deductions_set = EmployeeEarningsDeductions.objects.filter(employee_id=employee_id).filter(
            concept__type='D')

        extra['template'] = "employee_earnings_deductions"
        extra['earnings'] = earnings_set
        extra['deductions'] = deductions_set

        return super(EmployeeEarningsDeductionsAdmin, self).add_view(request, form_url, extra_context=extra)


# Employee Financial Data Admin.
@admin.register(EmployeeFinancialData)
class EmployeeFinancialDataAdmin(admin.ModelAdmin):
    form = EmployeeFinancialDataForm

    fieldsets = (
        ("Datos Financieros", {
            'fields': (
                'employee', 'payment_method', 'account_number', 'CLABE', 'bank', 'monthly_salary', 'daily_salary',
                'aggregate_daily_salary',)
        }),
    )

    inlines = (InfonavitDataAdmin,)

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeFinancialDataAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Overriding the add_wiew method for the employee pfinancial data admin.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        found_financial_data = request.GET.get('position')

        extra['employee'] = Employee.objects.get(pk=employee_id)

        financial_data = EmployeeFinancialData.objects.filter(employee_id=employee_id)

        if len(financial_data) > 0 and found_financial_data is None:
            return HttpResponseRedirect(
                "/admin/HumanResources/employeefinancialdata/" + str(
                    financial_data.first().id) + "/change?employee=" + str(employee_id) + "&position=1")

        return super(EmployeeFinancialDataAdmin, self).add_view(request, form_url, extra_context=extra)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        financial_data = EmployeeFinancialData.objects.filter(employee_id=employee_id)

        if len(financial_data) <= 0 or (int(object_id) != int(financial_data.first().id)):
            raise PermissionDenied

        extra['employee'] = Employee.objects.get(pk=employee_id)

        return super(EmployeeFinancialDataAdmin, self).change_view(request, object_id, form_url,
                                                                   extra)


# Earnings Deductions Admin.
@admin.register(EarningsDeductions)
class EarningsDeductionsAdmin(admin.ModelAdmin):
    form = EarningsDeductionsForm

    fieldsets = (
        ("Catálogo de Percepciones y Deducciones", {
            'fields': (
                'name', 'type', 'category', 'taxable', 'percent_taxable', 'accounting_account', 'sat_key',
                'law_type', 'status', 'comments',)
        }),
    )

    list_display = ('name', 'type', 'category', 'taxable', 'percent_taxable', 'get_change_link', 'get_delete_link')
    list_display_links = None

    def get_change_link(self, obj):
        return HumanResourcesAdminUtilities.get_change_link(obj)

    def get_delete_link(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    get_change_link.short_description = 'Editar'
    get_change_link.allow_tags = True

    get_delete_link.short_description = 'Eliminar'
    get_delete_link.allow_tags = True

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EarningsDeductionsAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        # employee_id = request.GET.get('employee')
        earnings_set = EarningsDeductions.objects.filter(type='P')
        deductions_set = EarningsDeductions.objects.filter(type='D')

        extra['template'] = "earnings_deductions"
        extra['earnings'] = earnings_set
        extra['deductions'] = deductions_set

        return super(EarningsDeductionsAdmin, self).add_view(request, form_url, extra_context=extra)


# Payroll Receipt Processed Admin.
@admin.register(PayrollReceiptProcessed)
class PayrollReceiptProcessedAdmin(admin.ModelAdmin):
    form = PayrollReceiptProcessedForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(PayrollReceiptProcessedAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def get_urls(self):
        urls = super(PayrollReceiptProcessedAdmin, self).get_urls()
        my_urls = [
            url(r'^receipts_by_period/(?P<payroll_period_id>\d+)/$',
                self.admin_site.admin_view(views.PayrollReceiptProcessedListView.as_view()),
                name='payroll-receipt-processed-list-view')

        ]

        return my_urls + urls


# Earning Deduction Period Project Admin.
@admin.register(EarningDeductionPeriod)
class EarningDeductionPeriodAdmin(admin.ModelAdmin):
    form = EarningDeductionPeriodForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EarningDeductionPeriodAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Payroll Processed Detail Admin.
@admin.register(PayrollProcessedDetail)
class PayrollProcessedDetailAdmin(admin.ModelAdmin):
    form = PayrollProcessedDetailForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(PayrollProcessedDetailAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


''' ----------------------------------
Administrators to fill the database.
----------------------------------  '''


# Payroll To Process Admin.
@admin.register(PayrollToProcess)
class PayrollToProcessAdmin(admin.ModelAdmin):
    form = PayrollToProcessForm


# Payroll Type Admin.
@admin.register(PayrollType)
class PayrollTypeAdmin(admin.ModelAdmin):
    form = PayrollTypeForm


# Payroll Type Admin.
@admin.register(PayrollGroup)
class PayrollGroupAdmin(admin.ModelAdmin):
    form = PayrollGroupForm

    fieldsets = (
        ("Grupos de Nómina", {
            'fields': ('name', 'payroll_classification', 'project', 'checker_type')
        }),
    )

    list_display = (
        'name', 'payroll_classification', 'project', 'get_detail_button', 'get_change_link', 'get_delete_link')

    def get_detail_button(self, obj):
        return HumanResourcesAdminUtilities.get_detail_link(obj)

    def get_change_link(self, obj):
        return HumanResourcesAdminUtilities.get_change_link(obj)

    def get_delete_link(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    get_detail_button.short_description = 'Periodos'
    get_detail_button.allow_tags = True

    get_change_link.short_description = 'Editar'
    get_change_link.allow_tags = True

    get_delete_link.short_description = 'Eliminar'
    get_delete_link.allow_tags = True

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        # employee_id = request.GET.get('employee')
        period_set = PayrollGroup.objects.all()

        extra['template'] = "payrollgroup"
        extra['period'] = period_set

        return super(PayrollGroupAdmin, self).add_view(request, form_url, extra_context=extra)

    def get_urls(self):
        urls = super(PayrollGroupAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/$', views.PayrollPeriodListView.as_view(), name='payroll-detail'),
        ]
        return my_urls + urls


# Payroll Period Admin.
@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    form = PayrollPeriodForm
    fieldsets = (
        ("Periodos de Nómina", {
            'fields': ('name', 'start_period', 'end_period', 'payroll_group', 'payroll_to_process')
        }),
    )

    search_fields = (
        'name', 'payroll_group__name', 'payroll_to_process__name')
    list_display = (
        'name', 'payroll_group', 'payroll_to_process', 'get_listpayroll_link', 'get_change_link', 'get_delete_link')

    def get_listpayroll_link(self, obj):
        return HumanResourcesAdminUtilities.get_listpayroll_link(obj, obj.id, obj.payroll_group.id)

    def get_change_link(self, obj):
        return HumanResourcesAdminUtilities.get_change_link(obj)

    def get_delete_link(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    get_listpayroll_link.short_description = 'Listado'
    get_listpayroll_link.allow_tags = True

    get_change_link.short_description = 'Editar'
    get_change_link.allow_tags = True

    get_delete_link.short_description = 'Eliminar'
    get_delete_link.allow_tags = True

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('/admin/HumanResources/payrollgroup/' + str(obj.payroll_group.id) + '/')

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        payroll_group_id = request.GET.get('payroll_group')

        print 'the id id ' + str(payroll_group_id)

        period_set = PayrollPeriod.objects.all()

        if payroll_group_id is not None:
            period_set = period_set.filter(payroll_group_id=payroll_group_id)

        extra['template'] = "payrollperiod"
        extra['period'] = period_set

        return super(PayrollPeriodAdmin, self).add_view(request, form_url, extra_context=extra)

    def get_urls(self):
        urls = super(PayrollPeriodAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/$', views.PayrollPeriodDetail.as_view(), name='payroll-period-detail'),
            url(r'^employee/(?P<pk>\d+)/$', views.PayrollPeriodEmployeeDetail.as_view(), name='payroll-period-detail'),
        ]
        return my_urls + urls


# Tax Regime Admin.
@admin.register(TaxRegime)
class TaxRegimeAdmin(admin.ModelAdmin):
    form = TaxRegimeForm


# Test (Exam) Admin.
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestForm


    fieldsets = (
        ("Pruebas", {
            'fields': ('name', )
        }),
    )

    list_display = ('name', 'get_change_link', 'get_delete_link')
    list_display_links = None

    search_fields = ('name',)

    def get_change_link(self, obj):
        return HumanResourcesAdminUtilities.get_change_link(obj)

    def get_delete_link(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    get_change_link.short_description = 'Editar'
    get_change_link.allow_tags = True

    get_delete_link.short_description = 'Eliminar'
    get_delete_link.allow_tags = True


# DocumentType Admin.
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    form = DocumentTypeForm


# Tag Admin.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm


    fieldsets = (
        ("Etiquetas", {
            'fields': ('name',)
        }),
    )

    search_fields = ('name',)

    list_display = ('name', 'get_change_link', 'get_delete_link')
    list_display_links = None

    def get_change_link(self, obj):
        return HumanResourcesAdminUtilities.get_change_link(obj)

    def get_delete_link(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    get_change_link.short_description = 'Editar'
    get_change_link.allow_tags = True

    get_delete_link.short_description = 'Eliminar'
    get_delete_link.allow_tags = True

# Assistance Admin.
@admin.register(EmployeeAssistance)
class EmployeeAssistanceAdmin(admin.ModelAdmin):
    form = EmployeeAssistanceForm

    fieldsets = (
        ("Registro de Asistencia por Empleado", {
            'fields': ('employee', 'payroll_period', 'record_date', 'entry_time', 'exit_time', 'absence')
        }),
    )

    readonly_fields = ('absence',)

    def save_model(self, request, obj, form, change):

        if obj.entry_time is None or obj.exit_time is None:
            return True

        employee_position = EmployeePositionDescription.objects.get(employee_id=obj.employee.id)

        position_entry_time = employee_position.entry_time
        position_exit_time = employee_position.departure_time

        entry_diff = datetime.datetime.combine(date.today(), obj.entry_time) - datetime.datetime.combine(date.today(),
                                                                                                         position_entry_time)
        exit_diff = datetime.datetime.combine(date.today(), position_exit_time) - datetime.datetime.combine(
            date.today(), obj.exit_time)

        arrived_minutes_late = entry_diff.total_seconds() / 60
        left_minutes_early = exit_diff.total_seconds() / 60

        absent = False
        allowed_minutes = 15

        if arrived_minutes_late > allowed_minutes or left_minutes_early > allowed_minutes:
            absent = True

        obj.absence = absent

        super(EmployeeAssistanceAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        urls = super(EmployeeAssistanceAdmin, self).get_urls()
        my_urls = [
            url(r'^incidences_by_period/(?P<payroll_period_id>\d+)/$',
                self.admin_site.admin_view(views.IncidencesByPayrollPeriod.as_view()),
                name='incidences-list-view',
                ),
            url(r'^incidences_by_employee/(?P<payroll_period_id>\d+)/(?P<employee_key>[\w-]+)/$',
                self.admin_site.admin_view(views.IncidencesByEmployee.as_view()),
                name='incidences-list-view',
                ),
        ]
        return my_urls + urls


# Assistance Admin.
@admin.register(AbsenceProof)
class AbsenceProofAdmin(admin.ModelAdmin):
    form = AbsenceProofForm

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(AbsenceProofAdmin, self).get_form(request, obj, **kwargs)

        # To pass the request object to the model form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if '_continue' not in request.POST:
            url = "/admin/HumanResources/employeeassistance/incidences_by_employee/" + str(
                obj.payroll_period.id) + "/" + obj.employee.employee_key + "/"
            return HttpResponseRedirect(url)
        else:
            return super(AbsenceProofAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            url = "/admin/HumanResources/employeeassistance/incidences_by_employee/" + str(
                obj.payroll_period.id) + "/" + obj.employee.employee_key + "/"
            return HttpResponseRedirect(url)
        else:
            return super(AbsenceProofAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        payroll_period_id = request.GET.get('payroll_period')
        employee_id = request.GET.get('employee')

        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)
        employee = Employee.objects.get(pk=employee_id)

        url = "/admin/HumanResources/employeeassistance/incidences_by_employee/" + str(
            payroll_period.id) + "/" + employee.employee_key + "/"
        return redirect(url)


# Uploaded Assistances Admin.
@admin.register(UploadedEmployeeAssistanceHistory)
class UploadedEmployeeAssistanceHistoryAdmin(admin.ModelAdmin):
    form = UploadedEmployeeAssistanceHistoryForm

    fieldsets = (
        ("Carga de Archivo de Asistencias", {
            'fields': ('payroll_period', 'assistance_file',)
        }),
    )

    def save_model(self, request, obj, form, change):
        current_user = request.user
        #payroll_group_id = int(request.POST.get('payroll_group'))
        payroll_period_id = int(request.POST.get('payroll_period'))

        try:
            with transaction.atomic():
                assistance_file = request.FILES['assistance_file']
                file_interface_obj = AssistanceFileInterface(assistance_file)

                # Getting the elements from the file.
                elements = file_interface_obj.get_element_list()

                # Processing the results.
                assitance_db_object = AssistanceDBObject(current_user, elements[1:], payroll_period_id)
                assitance_db_object.process_records()

                super(UploadedEmployeeAssistanceHistoryAdmin, self).save_model(request, obj, form, change)


        except ErrorDataUpload as e:
            e.save()
            # messages.set_level(request, messages.ERROR)
            django.contrib.messages.error(request, e.get_error_message())

        except django.db.utils.IntegrityError as e:
            django.contrib.messages.error(request, "Error de integridad de datos.")


class EmployeeLoanDetailInLine(admin.TabularInline):
    model = EmployeeLoanDetail
    form = EmployeeLoanDetailForm
    extra = 1


# Loan Admin.
@admin.register(EmployeeLoan)
class EmployeeLoanAdmin(admin.ModelAdmin):
    form = EmployeeLoanForm
    inlines = (EmployeeLoanDetailInLine,)

    fieldsets = (
        ("Prestamos a Empleados", {
            'fields': ('employee', 'amount', 'payment_plan', 'request_date')
        }),
    )


# JobProfile Admin.
@admin.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
    form = JobProfileForm


# Loan Admin.
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    form = DirectionForm


# Loan Admin.
@admin.register(Subdirection)
class SubdirectionAdmin(admin.ModelAdmin):
    form = SubdirectionForm


# Loan Admin.
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    form = AreaForm


# Loan Admin.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm


# Loan Admin.
@admin.register(JobInstance)
class JobInstanceAdmin(admin.ModelAdmin):
    form = JobInstanceForm

    fieldsets = (
        ("Puesto", {
            'fields': (
                'job_profile', 'employee',)
        }),
    )

    def get_urls(self):
        urls = super(JobInstanceAdmin, self).get_urls()
        my_urls = [
            url(r'^$', views.JobInstanceListView.as_view(), name='employee-detail'),
        ]
        return my_urls + urls

        # To redirect after object delete.

    def response_delete(self, request, obj_display, obj_id):
        if obj_id == 1:
            django.contrib.messages.set_level(request, messages.ERROR)
            django.contrib.messages.error(request, 'No se puede eliminar la raíz del organigrama.')

        return super(JobInstanceAdmin, self).response_delete(request, obj_display, obj_id)


# EmployeeDropOut
@admin.register(EmployeeDropOut)
class EmployeeDropOutAdmin(admin.ModelAdmin):
    form = EmployeeDropOutForm

    fieldsets = (
        ("Baja de Empleados", {
            'fields': ('employee', 'type', 'severance_pay', 'reason', 'date', 'observations')
        }),
    )

    # To redirect after add
    def response_add(self, request, obj, post_url_continue=None):
        employee = obj.employee
        employee.status = Employee.STATUS_INNACTIVE
        employee.save()

        return super(EmployeeDropOutAdmin, self).response_add(request, obj, post_url_continue)


# Employee Document Admin.
@admin.register(ISRTable)
class ISRTableAdmin(admin.ModelAdmin):
    pass


admin.site.register(PayrollClassification)
