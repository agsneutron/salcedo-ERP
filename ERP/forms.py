# coding=utf-8
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.contrib import messages
from django.forms import SelectDateWidget
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from tinymce.widgets import TinyMCE

from users.models import ERPUser
from django.utils.translation import ugettext as _

import datetime

from ERP.models import Project, TipoProyectoDetalle, DocumentoFuente, Estimate, ProgressEstimateLog, LogFile, LineItem, \
    ContratoContratista, Propietario, Empresa, Contact, Contratista, ContractConcepts, Concept_Input, AccessToProject, \
    ProgressEstimate
from django.utils.safestring import mark_safe
from Logs.controller import Logs
import os
from django.conf import settings
from django.contrib.admin import widgets

from django.contrib.admin.widgets import RelatedFieldWidgetWrapper


class TipoProyectoDetalleAddForm(forms.ModelForm):
    class Meta:
        model = TipoProyectoDetalle
        fields = '__all__'

    def save(self, commit=True):
        instance = super(TipoProyectoDetalleAddForm, self).save(commit=False)
        if instance.id is not None:  # Revisa si existe ese objeto
            a = TipoProyectoDetalle.objects.filter(id=instance.id).first()
            Logs.log(a.documento.name, "Mensaje")
            if a.documento.name != "":  # revisa si tiene una foto asignada

                if instance.documento.name != a.documento.name:  # revisa si cambio la foto asignada

                    route = settings.MEDIA_ROOT + "/" + a.documento.name  # borra la anterior y pon la nueva
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e
        return super(TipoProyectoDetalleAddForm, self).save(commit)


class AddProyectoForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def save(self, commit=True):
        instance = super(AddProyectoForm, self).save(commit=False)

        return super(AddProyectoForm, self).save(commit=commit)


class DocumentoFuenteForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuente
        fields = "__all__"

    def save(self, commit=True):
        print "OVERAID"
        instance = super(DocumentoFuenteForm, self).save(commit=False)

        if instance.id is not None:  # Revisa si existe ese objeto
            a = DocumentoFuente.objects.filter(id=instance.id).first()

            if a.documento.name != "":  # revisa si tiene una foto asignada

                if instance.documento.name != a.documento.name:  # revisa si cambio la foto asignada
                    route = settings.MEDIA_ROOT + "/" + a.documento.name  # borra la anterior y pon la nueva
                    print route
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e

        return super(DocumentoFuenteForm, self).save(commit)


'''
    Forms for the Estimate View: 
    This forms allows the user to register a new estimate for an specific project.
    
'''


class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        super(EstimateForm, self).__init__(*args, **kwargs)
        project_id = self.request.GET.get('project')

        if kwargs.get('instance'):
            contract_id = kwargs['instance'].contract.id
            self.fields['contract'].queryset = ContratoContratista.objects.filter(id=contract_id)
        else:
            estimated_contracts = Estimate.objects.filter(contract__project_id=project_id).values('contract_id')

            print "Contracts by Project: " + str(project_id)
            print estimated_contracts

            contract_id_array = []
            for estimated_contract in estimated_contracts:
                contract_id_array.append(estimated_contract['contract_id'])

            all_contracts_by_project = ContratoContratista.objects.filter(Q(project_id=project_id))
            no_estimated_contracts = ContratoContratista.objects.filter(Q(project_id=project_id)).exclude(
                Q(id__in=contract_id_array))

            no_concepts_contract_key_array = []
            no_concepts_contract_id_array = []

            for contract in all_contracts_by_project:
                concepts_by_contract = contract.concepts.all()
                if len(concepts_by_contract) <= 0:
                    no_concepts_contract_key_array.append(contract.clave_contrato)
                    no_concepts_contract_id_array.append(contract.id)

            self.fields['contract'].queryset = no_estimated_contracts.exclude(Q(id__in=no_concepts_contract_id_array))

            if not all_contracts_by_project.exists():
                messages.error(self.request, "No se han generado contratos con contratistas para el proyecto actual.")
            elif not no_estimated_contracts.exists():
                messages.error(self.request, "No hay contratos pendientes de estimar para este proyecto.")
            if len(no_concepts_contract_key_array) >= 1:
                messages.error(self.request, "Los siguientes contratos no cuentan con conceptos asignados: "
                               + ", ".join(no_concepts_contract_key_array))

    def clean(self):
        cleaned_data = super(EstimateForm, self).clean()
        status = cleaned_data.get("advance_payment_status")
        amount = cleaned_data.get("advance_payment_amount")

        print 'cleaning'

        if status == Estimate.PAID and amount <= 0:
            self._errors["advance_payment_status"] = self.error_class(
                ['El estatus del pago no puede ser "Pagado" si la cantidad es 0.0.'])
            # self.fields['advance_payment_amount'].
            raise forms.ValidationError("Error")


'''
    Forms for the progress estimate log.
'''


class ProgressEstimateLogForm(forms.ModelForm):
    class Meta:
        model = ProgressEstimateLog
        fields = '__all__'
        exclude = ()
        widgets = {
            # 'user': forms.HiddenInput(),
            'project': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.project_id = kwargs.pop('project_id', None)
        self.user_id = kwargs.pop('user_id', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {
                'project': self.project_id
            }

        kwargs['initial'].update({'project': self.project_id})
        # kwargs['initial'].update({'user': self.user_id})
        kwargs['initial'].update({'user': 1})
        # kwargs['initial'].update({'user_id': self.user_id})

        super(ProgressEstimateLogForm, self).__init__(*args, **kwargs)
        # self.fields['date'].widget = widgets.AdminDateWidget()

    # To override the save method for the form.
    # def save(self, commit=True):
    #     user_id = self.request.user.id
    #
    #     save_obj = super(ProgressEstimateLogForm, self)
    #
    #     print 'saving'
    #     print save_obj
    #     save_obj.user = ERPUser.objects.filter(Q(id=1))
    #     return save_obj.save(commit)
    #
    # def clean_user(self):
    #     data = self.cleaned_data['user']
    #     self.cleaned_data['user'] = 1
    #     print 'cleaning user!!'
    #     # do some stuff
    #     return data
    #
    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super(ProgressEstimateLogForm, self).clean()
        cleaned_data['user'] = User.objects.get(pk=self.user_id)
        self.cleaned_data['project'] = Project.objects.get(pk=self.project_id)


        if not self.request.user.has_perm('ERP.change_log_status'):
            if self.instance.status != self.cleaned_data['status']:
                self.cleaned_data['status'] = self.instance.status

        return cleaned_data

    def save(self, commit=True):
        self.instance.project = Project.objects.get(pk=self.project_id)
        return super(ProgressEstimateLogForm, self).save(commit)


'''
    Forms for the log file form.
'''


class LogFileForm(forms.ModelForm):
    class Meta:
        model = LogFile
        fields = "__all__"
        test = ProgressEstimateLogForm()
        widgets = {
        }


class ProgressEstimateForm(forms.ModelForm):
    class Meta:
        model = ProgressEstimate
        fields = "__all__"

    def clean(self):

        is_new = self.instance.pk is None

        is_unlocked = not is_new and self.instance.estimate.lock_status == Estimate.UNLOCKED

        cleaned_data = super(ProgressEstimateForm, self).clean()

        estimate = cleaned_data['estimate']
        new_amount = cleaned_data['amount']
        accumulated_amount = estimate.get_accumulated_amount()
        contract_amount = estimate.contract.monto_contrato

        if is_new:
            accumulated_amount = accumulated_amount + new_amount
        else:
            old_amount = self.instance.amount
            accumulated_amount = accumulated_amount - old_amount + new_amount
            if is_unlocked and self.instance.type == ProgressEstimate.PROGRESS:
                # Payment amount can't be changed
                if old_amount != new_amount:
                    self._errors["amount"] = self.error_class(
                        ['El monto no puede cambiar una vez que se ha definido un finiquito.'])
                    raise ValidationError('Error en la cantidad')

        new_percentage = accumulated_amount / contract_amount

        if estimate.lock_status == 'L' and new_percentage > 0.8 and self.instance.type == ProgressEstimate.PROGRESS:
            self._errors["amount"] = self.error_class(
                ['El monto acumulado no puede superar el 80% si la estimación no ha sido liberada.'])
            raise ValidationError('Error en la cantidad')

        elif estimate.lock_status == 'U':
            estimate.lock_status = 'C'
            estimate.save()
        return cleaned_data


'''
    Forms for the progress estimate.
'''


class ContractForm(forms.ModelForm):
    class Meta:
        model = ContratoContratista
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        print args
        print '--'
        print kwargs
        self.request = kwargs.pop('request', None)
        super(ContractForm, self).__init__(*args, **kwargs)
        # self.fields['fecha_inicio'].widget = widgets.AdminDateWidget()
        # self.fields['fecha_termino'].widget = widgets.AdminDateWidget()
        # self.fields['fecha_firma'].widget = widgets.AdminDateWidget()


class ContractConceptsForm(forms.ModelForm):
    contract_id = None

    class Meta:
        model = ContractConcepts
        fields = ('contract', 'concept', 'amount')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.contract_id = kwargs.pop('contract_id', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        kwargs['initial'].update({'contract': self.contract_id})
        super(ContractConceptsForm, self).__init__(*args, **kwargs)
        if self.contract_id is not None:
            contract_obj = ContratoContratista.objects.get(pk=self.contract_id)

            self.fields['contract'].queryset = ContratoContratista.objects.filter(pk=self.contract_id)

            contract_concepts = ContractConcepts.objects.filter(contract__id=self.contract_id).values('concept_id')
            exclude = []
            for c in contract_concepts:
                exclude.append(c['concept_id'])

            self.fields['concept'].queryset = Concept_Input.objects.filter(
                line_item__id=contract_obj.line_item.id).exclude(id__in=exclude)

            if len(self.fields['concept'].queryset) == 0:
                messages.error(self.request,
                               "Ya no hay más conceptos que se puedan agregar al contrato.")


class EstimateSearchForm(forms.Form):
    current_project_id = 0

    def __init__(self, project_id):
        super(EstimateSearchForm, self).__init__()
        self.fields['line_item'].queryset = LineItem.objects.filter(project_id=project_id)

    start_date = forms.DateTimeField(initial=datetime.date.today(), widget=widgets.AdminDateWidget,
                                     label="Fecha de Inicio")
    end_date = forms.DateTimeField(initial=datetime.date.today(), widget=widgets.AdminDateWidget,
                                   label="Fecha de Término")

    line_item = forms.ModelChoiceField(queryset=LineItem.objects.all(),
                                       empty_label="Seleccionar Partida", label='', required=False)

    contractor = forms.ModelChoiceField(queryset=Contratista.objects.all(),
                                        empty_label="Seleccionar Contratista", label='', required=False)


class AddEstimateForm(forms.Form):
    project_id = None

    def __init__(self, project_id):
        super(AddEstimateForm, self).__init__()
        AddEstimateForm.project_id = project_id

    project = forms.IntegerField(initial=project_id)


class OwnerForm(forms.ModelForm):
    empresa_id = None

    class Meta:
        model = Propietario
        fields = (
            'nombrePropietario', 'rfc', 'empresa', 'email', 'telefono1', 'telefono2', 'pais', 'estado', 'municipio',
            'cp', 'calle', 'numero', 'colonia', 'version',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.company_id = kwargs.pop('company_id', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        kwargs['initial'].update({'empresa': self.company_id})
        super(OwnerForm, self).__init__(*args, **kwargs)

        if self.company_id is not None:
            self.fields['empresa'].queryset = Empresa.objects.filter(pk=self.company_id)

    def clean(self):
        cleaned_data = super(OwnerForm, self).clean()
        print 'cleaned-data'
        print cleaned_data
        return cleaned_data


class ContactForm(forms.ModelForm):
    contractor_id = None

    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.contractor_id = kwargs.pop('contratista_id', None)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

        # Selecting the current value for the contractor if it exists, otherwise, None.
        kwargs['initial'].update({'contractor': self.contractor_id})

        super(ContactForm, self).__init__(*args, **kwargs)

        # Filtering the values for the contractor if it , otherwise, None.
        if self.contractor_id is not None:
            self.fields['contractor'].queryset = Contratista.objects.filter(pk=self.contractor_id)


class EstimateDedutionsForm(forms.ModelForm):

    estimate_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Estimate
        fields = ('id', 'deduction_amount', 'deduction_comments',)

    def __init__(self, *args, **kwargs):
        super(EstimateDedutionsForm, self).__init__(*args, **kwargs)
        self.fields['deduction_amount'].required = True
        self.fields['deduction_comments'].required = True

    def is_valid(self):
        print 'Is valid______'
        valid = super(EstimateDedutionsForm, self).is_valid()
        if not valid:
            return valid
        if self.cleaned_data['deduction_comments'] is None or self.cleaned_data['deduction_comments'] == "":
            return False
        return True

