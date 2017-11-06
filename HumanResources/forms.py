from django import forms

# Importing the model.
from HumanResources.models import *


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
        model = Tag
        fields = '__all__'


# Form to include the fields of Tag Form.
class EmployeeLoanForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
