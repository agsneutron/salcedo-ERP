# coding=utf-8
from django import forms
from django.contrib.admin import widgets
from django.db import models
from django.db.models import Q
from django.contrib import messages
from django.forms import SelectDateWidget
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from users.models import ERPUser

import datetime

from ERP.models import Project, TipoProyectoDetalle, DocumentoFuente, Estimate, ProgressEstimateLog, LogFile, LineItem, \
    ContratoContratista, Propietario, Empresa, Contact, Contratista, ContractConcepts, Concept_Input
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
    Forms for the progress estimate.
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
            line_item_id = kwargs['instance'].concept_input.line_item.id
            self.fields['line_item'].queryset = LineItem.objects.filter(id=line_item_id)
        else:
            self.fields['line_item'].queryset = LineItem.objects.filter(project_id=project_id)
            # self.fields['start_date'].widget = widgets.AdminDateWidget()
            # self.fields['end_date'].widget = widgets.AdminDateWidget()
            # self.fields['period'].widget = widgets.AdminDateWidget()

    # def save(self, commit=True):
    #
    #     if self.fields['advance_payment_status'] == Estimate.PAID and self.fields[
    #         'advance_payment_amount'] is not None and self.fields['advance_payment_amount'] > 0:
    #         return super(EstimateForm, self).save(commit)
    #     else:
    #         # return super(EstimateForm, self).save(commit)
    #         messages.set_level(self.request, messages.ERROR)
    #         messages.error(self.request, 'El estatus del pago no puede ser "Pagado" si la cantidad es inválida.')

    def clean(self):
        cleaned_data = super(EstimateForm, self).clean()
        status = cleaned_data.get("advance_payment_status")
        amount = cleaned_data.get("advance_payment_amount")

        print 'cleaning'

        if status == Estimate.PAID and amount <= 0:

            self._errors["advance_payment_status"] = self.error_class(['El estatus del pago no puede ser "Pagado" si la cantidad es 0.0.'])
            # self.fields['advance_payment_amount'].
            raise forms.ValidationError("Error")


'''
    Forms for the progress estimate log.
'''


class ProgressEstimateLogForm(forms.ModelForm):
    class Meta:
        model = ProgressEstimateLog
        fields = '__all__'
        # exclude = ('user',)
        widgets = {
            # 'user': forms.HiddenInput(),
            'progress_estimate': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.project_id = kwargs.pop('project_id', None)
        self.user_id = kwargs.pop('user_id', None)

        print 'kwargs:'
        print kwargs

        # print "User_ID:" + str(self.user_id)
        print "project_id:" + str(self.project_id)

        if not kwargs.get('initial'):
            kwargs['initial'] = {}

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
        cleaned_data['user'] = ERPUser.objects.get(pk=self.user_id)
        return cleaned_data


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


'''
    Forms for the progress estimate.
'''


class ContractForm(forms.ModelForm):
    class Meta:
        model = ContratoContratista
        fields = '__all__'

    def __init__(self, *args, **kwargs):
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
            self.fields['concept'].queryset = Concept_Input.objects.filter(line_item__id=contract_obj.line_item.id)




class EstimateSearchForm(forms.Form):
    def __init__(self, project_id):
        super(EstimateSearchForm, self).__init__()
        self.project_id = project_id

    start_date = forms.DateTimeField(initial=datetime.date.today(), widget=widgets.AdminDateWidget,
                                     label="Fecha de Inicio")
    end_date = forms.DateTimeField(initial=datetime.date.today(), widget=widgets.AdminDateWidget,
                                   label="Fecha de Término")

    TYPE_CHOICES = (
        ('C', "Concepto"),
        ('I', "Insumo"),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, initial='', widget=forms.Select(), required=True,
                             label="Tipo")

    line_item = forms.ModelChoiceField(queryset=LineItem.objects.filter(project_id=1),
                                       empty_label="Seleccionar Partida", label='')


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
