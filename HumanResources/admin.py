# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Libraries.
from django.conf.urls import url
from django.contrib import admin

# Importing the views.
from django.contrib.admin.views.main import ChangeList

from HumanResources import views

# Importing the forms.
from HumanResources.forms import *

# Importing the models.
from HumanResources.models import *


class HumanResourcesAdminUtilities():
    @staticmethod
    def get_detail_link(obj):
        model_name =  obj.__class__.__name__.lower()
        link = "http://localhost:8000/admin/HumanResources/"+model_name+"/"+str(obj.id)+"/"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-eye color-default eliminar' > </i>"

        return '<a href="'+link+'" class="'+css+'" >'+button+'</a>'

    @staticmethod
    def get_delete_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "http://localhost:8000/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/delete"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-trash-o color-danger eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'


    @staticmethod
    def get_change_link_with_employee(obj, employee_id):
        model_name = obj.__class__.__name__.lower()
        link = "http://localhost:8000/admin/HumanResources/" + model_name + "/" + str(obj.id) + "/change?employee="+str(employee_id)
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

    list_display = ('get_full_name','get_detail_column','get_change_column', 'get_delete_column','get_payroll_column')
    list_display_links = None

    def get_full_name(self, obj):
        return obj.name + " " + obj.first_last_name + " " + obj.second_last_name

    def get_detail_column(self, obj):
        return HumanResourcesAdminUtilities.get_detail_link(obj)

    def get_change_column(self, obj):
        return HumanResourcesAdminUtilities.get_change_link_with_employee(obj, obj.id)

    def get_delete_column(self, obj):
        return HumanResourcesAdminUtilities.get_delete_link(obj)

    def get_payroll_column(self, obj):
        return HumanResourcesAdminUtilities.get_nomina_link_with_employee(obj,obj.id)

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


    # Overriding the Change View for the employee
    #def change_view(self, request, object_id, form_url='', extra_context=None):

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

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        education_set = Education.objects.filter(employee_id=employee_id)

        extra['template'] = "education"
        extra['education'] = education_set

        return super(EducationAdmin, self).add_view(request, form_url, extra_context=extra)


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
        # Adding extra context to the change view.

    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        employee_id = request.GET.get('employee')
        emergencycontact_set = EmergencyContact.objects.filter(employee_id=employee_id)

        extra['template'] = "emergencycontact"
        extra['emergencycontact'] = emergencycontact_set

        return super(EmergencyContactAdmin, self).add_view(request, form_url, extra_context=extra)


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
            'fields': ('employee','start_date', 'end_date', 'direction', 'subdirection','area','department','job_profile', 'physical_location',
                       'payroll_classification','project','insurance_type','insurance_number','monday','tuesday', 'wednesday', 'thursday','friday','saturday','sunday','entry_time','departure_time',
                       'observations','payroll_group')
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

    # Infonavit Data Admin.
#@admin.register(InfonavitData)
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


@admin.register(EmployeeEarningsDeductions)
class EmployeeEarningsDeductionsAdmin(admin.ModelAdmin):
    form = EmployeeEarningsDeductionsForm

    fieldsets = (
        ("Percepciones y Deducciones", {
            'fields': ('employee','concept','ammount','date')
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
        deductions_set = EmployeeEarningsDeductions.objects.filter(employee_id=employee_id).filter(concept__type='D')

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
            'fields': ('employee', 'payment_method', 'account_number', 'CLABE', 'bank', 'monthly_salary', 'daily_salary',
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

        #employee_id = request.GET.get('employee')
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



# Payroll Processed Admin.
@admin.register(PayrollProcessed)
class PayrollProcessedAdmin(admin.ModelAdmin):
    form = PayrollProcessedForm

    fieldsets = (
        ("Nómina a Generar", {
            'fields': ('payroll_period','payroll_to_process','payroll_classification')
        }),
    )


    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        #employee_id = request.GET.get('employee')
        payroll_set = PayrollProcessed.objects.all()

        extra['template'] = "payrollprocessed"
        extra['payroll'] = payroll_set


        return super(PayrollProcessedAdmin, self).add_view(request, form_url, extra_context=extra)

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
            'fields': ('name',)
        }),
    )


    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        #employee_id = request.GET.get('employee')
        period_set = PayrollGroup.objects.all()

        extra['template'] = "payrollgroup"
        extra['period'] = period_set


        return super(PayrollGroupAdmin, self).add_view(request, form_url, extra_context=extra)

# Payroll Period Admin.
@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    form = PayrollPeriodForm


    fieldsets = (
        ("Periodos de Nómina", {
            'fields': ('name','start_period','end_period', 'week', 'month', 'year', 'payroll_group')
        }),
    )


    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        #employee_id = request.GET.get('employee')
        period_set = PayrollPeriod.objects.all()

        extra['template'] = "payrollperiod"
        extra['period'] = period_set


        return super(PayrollPeriodAdmin, self).add_view(request, form_url, extra_context=extra)


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
