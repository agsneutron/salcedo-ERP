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
class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

# Form to include the fields of the Creditors Form.
class CreditorsForm(forms.ModelForm):
    class Meta:
        model = Creditors
        fields = '__all__'

