from django import forms

from SharedCatalogs.models import *


class InternalCompanyForm(forms.ModelForm):
    class Meta:
        mode = InternalCompany
        fields = '__all__'