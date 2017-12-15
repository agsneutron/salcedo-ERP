from django import forms

# Importing the model.
from Accounting.models import *
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.utils.timezone import now


# Form to include the fields of the AccountingPolicy Form.
class AccountingPolicyForm(forms.ModelForm):
    class Meta:
        model = AccountingPolicy
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


# Form to include the fields of the FiscalPeriod Form.
class FiscalPeriodForm(forms.ModelForm):
    class Meta:
        model = FiscalPeriod
        fields = '__all__'


# Form to include the fields of the TypePolicy Form.
class TypePolicyForm(forms.ModelForm):
    class Meta:
        model = TypePolicy
        fields = '__all__'


# Form to include the fields of the Provider Form.
class CommercialAllyForm(forms.ModelForm):
    class Meta:
        model = CommercialAlly
        fields = '__all__'

        widgets = {
            "type": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.type = self.request.GET.get('type', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the commercialally if it exists, otherwise, None.
        kwargs['initial'].update({'type': self.type})

        # Calling super class to have acces to the fields.
        super(CommercialAllyForm, self).__init__(*args, **kwargs)

        # Filtering the values for the commercialally if it , otherwise, None.
        if self.type is not None:
            self.fields['type'].queryset = CommercialAlly.objects.filter(type=self.type)


# Form to include the fields of the Account Form.
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
