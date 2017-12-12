from django import forms

# Importing the model.
from Accounting.models import *
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.utils.timezone import now


# Form to include the fields of the Employee Form.
class AccountingPolicyForm(forms.ModelForm):
    class Meta:
        model = AccountingPolicy
        fields = '__all__'