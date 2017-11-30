from django import forms

# Importing the model.
from HumanResources.models import *
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.utils.timezone import now

# Form to include the fields of the Employee Form.
class EmployeeForm(forms.ModelForm):
    contractor_id = None

    class Meta:
        model = Employee
        fields = '__all__'


# Form to include the fields of the Education Form.
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EducationForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Education Form.
class CurrentEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(CurrentEducationForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Emergency Contact Form.
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmergencyContactForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Family Member Form.
class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(FamilyMemberForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the FWork Reference Form.
class WorkReferenceForm(forms.ModelForm):
    class Meta:
        model = WorkReference
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(WorkReferenceForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Work Reference Form.
class TestApplicationForm(forms.ModelForm):
    class Meta:
        model = TestApplication
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(TestApplicationForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Employee Document Form.
class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeeDocumentForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Checker Data Form.
class CheckerDataForm(forms.ModelForm):
    class Meta:
        model = CheckerData
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(CheckerDataForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Employee Has Tag Form.
class EmployeeHasTagForm(forms.ModelForm):
    class Meta:
        model = EmployeeHasTag
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeeHasTagForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Employee Position Description Form.
class EmployeePositionDescriptionForm(forms.ModelForm):
    class Meta:
        model = EmployeePositionDescription
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeePositionDescriptionForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Employee Financial Data Form.
class EmployeeFinancialDataForm(forms.ModelForm):
    class Meta:
        model = EmployeeFinancialData
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeeFinancialDataForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of the Infonavit Data Form.
class InfonavitDataForm(forms.ModelForm):
    class Meta:
        model = InfonavitData
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(InfonavitDataForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)



# Form to include the fields of Earnings Deductions Form.
class EarningsDeductionsForm(forms.ModelForm):
    class Meta:
        model = EarningsDeductions
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EarningsDeductionsForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)


# Form to include the fields of Employee Earnings Deductions Form.
class EmployeeEarningsDeductionsForm(forms.ModelForm):
    class Meta:
        model = EmployeeEarningsDeductions
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeeEarningsDeductionsForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)

# Form to include the fields of Employee Earnings Deductions Form.
class EmployeeEarningsDeductionsbyPeriodForm(forms.ModelForm):
    class Meta:
        model = EmployeeEarningsDeductionsbyPeriod
        fields = '__all__'
        widgets = {
            "employee": forms.HiddenInput,
            "payroll_period": forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)
        self.payroll_period_id = self.request.GET.get('payrollperiod', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})
        kwargs['initial'].update({'payroll_period': self.payroll_period_id})

        # Calling super class to have acces to the fields.
        super(EmployeeEarningsDeductionsbyPeriodForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)

        if self.payroll_period_id is not None:
            self.fields['payroll_period'].queryset = PayrollPeriod.objects.filter(pk=self.payroll_period_id)

# Form to include the fields of Employee Earnings Deductions Form.
class PayrollTeForm(forms.ModelForm):
    class Meta:
        model = PayrollType
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(EmployeeEarningsDeductionsForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)



# Form to include the fields of Payroll Receipt Processed Form.
class PayrollReceiptProcessedForm(forms.ModelForm):
    class Meta:
        model = PayrollReceiptProcessed
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.employee_id = self.request.GET.get('employee', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'employee': self.employee_id})

        # Calling super class to have acces to the fields.
        super(PayrollReceiptProcessedForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.employee_id is not None:
            self.fields['employee'].queryset = Employee.objects.filter(pk=self.employee_id)



# Form to include the fields of Payroll Processed Detail Form.
class PayrollProcessedDetailForm(forms.ModelForm):
    class Meta:
        model = PayrollProcessedDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.payroll_receip_processed_id = self.request.GET.get('payroll_receip_processed', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'payroll_receip_processed': self.payroll_receip_processed_id})

        # Calling super class to have acces to the fields.
        super(PayrollProcessedDetailForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.payroll_receip_processed_id is not None:
            self.fields['payroll_receip_processed'].queryset = PayrollReceiptProcessed.objects.filter(pk=self.payroll_receip_processed_id)
'''
class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data

class EmployeeFinantialForm(CombinedFormBase):
    form_classes = [EmployeeFinancialDataForm, InfonavitDataForm]

class RegisterView(FormView):
    template_name = "register.html"
    form_class = EmployeeFinantialForm

    def form_valid(self, form):
        # some actions...
        return redirect(self.get_success_url())

'''


# Form to include the fields of the Payroll Group Form.
class EmployeeLoanDetailForm(forms.ModelForm):
    class Meta:
        model = EmployeeLoanDetail
        fields = '__all__'


# Form to include the fields of the Payroll Group Form.
class PayrollGroupForm(forms.ModelForm):
    class Meta:
        model = PayrollGroup
        fields = '__all__'


# Form to include the fields of the Earning Deduction Period Form.
class EarningDeductionPeriodForm(forms.ModelForm):
    class Meta:
        model = EarningDeductionPeriod
        fields = '__all__'


# Form to include the fields of the Payroll To Process Form.
class PayrollToProcessForm(forms.ModelForm):
    class Meta:
        model = PayrollToProcess
        fields = '__all__'


# Form to include the fields of the Payroll Type Form.
class PayrollTypeForm(forms.ModelForm):
    class Meta:
        model = PayrollType
        fields = '__all__'


# Form to include the fields of the Payroll Period Form.
class PayrollPeriodForm(forms.ModelForm):
    class Meta:
        model = PayrollPeriod
        fields = '__all__'


# Form to include the fields of the Tax Regime Form.
class TaxRegimeForm(forms.ModelForm):
    class Meta:
        model = TaxRegime
        fields = '__all__'


# Form to include the fields of the Tax Regime Form.
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'


# Form to include the fields of the Document Type Form.
class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = '__all__'


# Form to include the fields of Tag Form.
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


# Form to include the fields of Tag Form.
class EmployeeAssistanceForm(forms.ModelForm):
    class Meta:
        model = EmployeeAssistance
        fields = ('employee', 'payroll_period', 'record_date', 'entry_time', 'exit_time','absence')


# Form to include the fields of Tag Form.
class EmployeeAssistanceForm(forms.ModelForm):
    class Meta:
        model = EmployeeAssistance
        fields = ('employee', 'payroll_period', 'record_date', 'entry_time', 'exit_time', 'justified','absence')


# Form to include the fields of Tag Form.
class AbsenceProofForm(forms.ModelForm):
    class Meta:
        model = AbsenceProof
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        # Getting the request object.
        self.request = kwargs.pop('request', None)
        payroll_period_id = self.request.GET.get('payroll_period')
        employee_id = self.request.GET.get('employee')



        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Updating the initial value of the dropdown.
        kwargs['initial'].update({'employee': employee_id})
        kwargs['initial'].update({'payroll_period': payroll_period_id})

        # After this point, we can filter the querysets for the intended fields.
        super(AbsenceProofForm, self).__init__(*args, **kwargs)

        self.fields['employee'].queryset = Employee.objects.filter(pk=employee_id)
        self.fields['payroll_period'].queryset = PayrollPeriod.objects.filter(pk=payroll_period_id)



# Form to include the fields of Tag Form.
class UploadedEmployeeAssistanceHistoryForm(forms.ModelForm):
    class Meta:
        model = UploadedEmployeeAssistanceHistory
        fields = '__all__'


# Form to include the fields of Tag Form.
class EmployeeLoanForm(forms.ModelForm):
    class Meta:
        model = EmployeeLoan
        fields = '__all__'


# Form to include the fields of Tag Form.
class JobProfileForm(forms.ModelForm):
    class Meta:
        model = JobProfile
        fields = '__all__'


# Form to include the fields of Tag Form.
class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'


# Form to include the fields of Tag Form.
class SubdirectionForm(forms.ModelForm):
    class Meta:
        model = Subdirection
        fields = '__all__'


# Form to include the fields of Tag Form.
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

# Form to include the fields of Tag Form.
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'


# Form to include the fields of Tag Form.
class JobInstanceForm(forms.ModelForm):
    class Meta:
        model = JobInstance
        fields = '__all__'


# Form to include the fields of Tag Form.
class EmployeeDropOutForm(forms.ModelForm):
    class Meta:
        model = EmployeeDropOut
        fields = '__all__'




