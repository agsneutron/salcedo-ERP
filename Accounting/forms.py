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


    def save(self, commit=True):
        instance = super(AccountingPolicyForm, self).save(commit=False)

        if instance.folio is None:

            lista = AccountingPolicy.objects.filter(type_policy__id=instance.type_policy.id).values('folio').order_by('-folio')

            if lista.count() > 0:
                last_number = lista[0]
                numero = int(last_number.get('folio')) + 1
                print numero
                instance.folio = numero
            else:
                instance.folio = 1



        return super(AccountingPolicyForm, self).save(commit=commit)

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


class CommercialAllyContactForm(forms.ModelForm):
    class Meta:
        model = CommercialAllyContact
        fields = '__all__'

        widgets = {
            "commercialally": forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        self.commercialally_id = self.request.GET.get('commercialally_id', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the commercialally if it exists, otherwise, None.
        kwargs['initial'].update({'commercialally': self.commercialally_id})

        # Calling super class to have acces to the fields.
        super(CommercialAllyContactForm, self).__init__(*args, **kwargs)

        # Filtering the values for the commercialally if it , otherwise, None.
        if self.commercialally_id is not None:
            self.fields['commercialally'].queryset = CommercialAlly.objects.filter(id=self.commercialally_id)
