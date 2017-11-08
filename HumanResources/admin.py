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
            'fields': ('employee_key', 'type', 'registry_date', 'status')
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

    def get_urls(self):
        urls = super(EmployeeAdmin, self).get_urls()

        my_urls = [
            # url(r'^$',
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


# Employee Position Description Admin.
@admin.register(EmployeePositionDescription)
class EmployeePositionDescriptionAdmin(admin.ModelAdmin):
    form = EmployeePositionDescriptionForm
    fieldsets = (
        ("Descripción de Puesto", {
            #contract
            'fields': ('start_date', 'end_date', 'direction', 'subdirection','area','department','job_profile','physical_location',
                       'payroll_classification','project','insurance_type','insurance_number','days_attendance','entry_time','departure_time',
                       'observations')
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

# Employee Financial Data Admin.
@admin.register(EmployeeFinancialData)
class EmployeeFinancialDataAdmin(admin.ModelAdmin):
    form = EmployeeFinancialDataForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeFinancialDataAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Infonavit Data Admin.
@admin.register(InfonavitData)
class InfonavitDataAdmin(admin.ModelAdmin):
    form = InfonavitDataForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(InfonavitDataAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Earnings Deductions Admin.
@admin.register(EarningsDeductions)
class EarningsDeductionsAdmin(admin.ModelAdmin):
    form = EarningsDeductionsForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EarningsDeductionsAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


# Employee Earnings Deductions Admin.
@admin.register(EmployeeEarningsDeductions)
class EmployeeEarningsDeductionsAdmin(admin.ModelAdmin):
    form = EmployeeEarningsDeductionsForm

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(EmployeeEarningsDeductionsAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


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



# Payroll Processed Admin.
@admin.register(PayrollProcessed)
class PayrollProcessedAdmin(admin.ModelAdmin):
    form = PayrollProcessedForm

# Payroll To Process Admin.
@admin.register(PayrollToProcess)
class PayrollToProcessAdmin(admin.ModelAdmin):
    form = PayrollToProcessForm

# Payroll Type Admin.
@admin.register(PayrollType)
class PayrollTypeAdmin(admin.ModelAdmin):
    form = PayrollTypeForm


# Payroll Period Admin.
@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    form = PayrollPeriodForm

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


# Assistance Admin.
@admin.register(EmployeeAssistance)
class EmployeeAssistanceAdmin(admin.ModelAdmin):
    form = EmployeeAssistanceForm


# Loan Admin.
@admin.register(EmployeeLoan)
class EmployeeLoanAdmin(admin.ModelAdmin):
    form = EmployeeLoanForm


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

    def get_urls(self):
        urls = super(JobInstanceAdmin, self).get_urls()
        my_urls = [
            url(r'^$', views.JobInstanceListView.as_view(), name='employee-detail'),
        ]
        return my_urls + urls
