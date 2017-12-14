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
class CommercialAllyForm(forms.ModelForm):
    class Meta:
        model = CommercialAlly
        fields = '__all__'


# Form to include the fields of the Account Form.
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
