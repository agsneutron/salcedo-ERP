# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Libraries.
from django.conf.urls import url
from django.contrib import admin

# Importing the views.
from HumanResources import views

# Importing the forms.
from HumanResources.forms import *


# Employee Admin.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    fieldsets = (
        ("Datos de Empleado", {
            'fields': ('employee_key','type','registry_date', 'status')
        }),
        ("Datos Personales", {
            'fields': ('name', 'first_last_name', 'second_last_name', 'birthdate', 'birthplace', 'gender', 'marital_status',
                       'curp', 'rfc', 'tax_regime', 'blood_type', 'street', 'outdoor_number', 'indoor_number', 'colony',
                       'country', 'state', 'town', 'zip_code', 'phone_number', 'cellphone_number','office_number',
                       'extension_number','personal_email', 'work_email', 'driving_license_number','driving_license_expiry_date')
        }),
    )
    list_display = ('name', 'first_last_name', 'personal_email', )
    # list_editable = ('first_last_name', 'personal_email', )

    def get_urls(self):
        urls = super(EmployeeAdmin, self).get_urls()
        my_urls = [
            #url(r'^$',
            #    self.admin_site.admin_view(ProgressEstimateLogListView.as_view()),
            #    name='progressestimatelog-list-view'),
            url(r'^(?P<pk>\d+)/$', views.EmployeeDetailView.as_view(), name='employee-detail'),

        ]
        return my_urls + urls


# Education Admin.
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    form = EducationForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EducationAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass



# Admin for the inline documents of the current education of an employee.
class CurrentEducationDocumentInline(admin.TabularInline):
    model = CurrentEducationDocument
    extra = 1


# Current Education Admin.
@admin.register(CurrentEducation)
class CurrentEducationAdmin(admin.ModelAdmin):
    form = CurrentEducationForm
    inlines = (CurrentEducationDocumentInline, )

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

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmergencyContactAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass



# Family Member Admin.
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    form = FamilyMemberForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(FamilyMemberAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Work Reference Admin.
@admin.register(WorkReference)
class WorkReferenceAdmin(admin.ModelAdmin):
    form = WorkReferenceForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(WorkReferenceAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

# Test Application Admin.
@admin.register(TestApplication)
class TestApplicationAdmin(admin.ModelAdmin):
    form = TestApplicationForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(TestApplicationAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Employee Document Admin.
@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    form = EmployeeDocumentForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeDocumentAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Checker Data Admin.
@admin.register(CheckerData)
class CheckerDataAdmin(admin.ModelAdmin):
    form = CheckerDataForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CheckerDataAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Employee Has Tag Admin.
@admin.register(EmployeeHasTag)
class EmployeeHasTagAdmin(admin.ModelAdmin):
    form = EmployeeHasTagForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeHasTagAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


''' ----------------------------------
Administrators to fill the database.
----------------------------------  '''

# Tax Regime Admin.
@admin.register(TaxRegime)
class TaxRegimeAdmin(admin.ModelAdmin):
    form = TaxRegimeForm


# Test (Exam) Admin.
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestForm


# DocumentType Admin.
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    form = DocumentTypeForm


# Tag Admin.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm