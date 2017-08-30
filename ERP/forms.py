# coding=utf-8
from django import forms
from django.contrib.admin import widgets
from django.db import models
from django.forms import SelectDateWidget
from django.utils import timezone

import datetime

from ERP.models import Project, TipoProyectoDetalle, DocumentoFuente, Estimate, ProgressEstimateLog, LogFile, LineItem, ContratoContratista
from datetime import datetime
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
        self.fields['start_date'].widget = widgets.AdminDateWidget()
        self.fields['end_date'].widget = widgets.AdminDateWidget()
        self.fields['period'].widget = widgets.AdminDateWidget()
        self.fields['line_item'].queryset = LineItem.objects.filter(project__id=project_id)


'''
    Forms for the progress estimate log.
'''


class ProgressEstimateLogForm(forms.ModelForm):
    class Meta:
        model = ProgressEstimateLog
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'progress_estimate': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProgressEstimateLogForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
    # To override the save method for the form.
    def save(self, commit=True):
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
        self.fields['fecha_inicio'].widget = widgets.AdminDateWidget()
        self.fields['fecha_termino'].widget = widgets.AdminDateWidget()
        self.fields['fecha_firma'].widget = widgets.AdminDateWidget()



class EstimateSearchForm(forms.Form):
    def __init__(self, project_id):
        super(EstimateSearchForm, self).__init__()
        self.project_id = project_id

    start_date = forms.DateTimeField(initial=datetime.date.today, widget=widgets.AdminDateWidget,
                                     label="Fecha de Inicio")
    end_date = forms.DateTimeField(initial=datetime.date.today, widget=widgets.AdminDateWidget,
                                   label="Fecha de Término")

    TYPE_CHOICES = (
        ('C', "Concepto"),
        ('I', "Insumo"),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, initial='', widget=forms.Select(), required=True,
                             label="Tipo")

    line_item = forms.ModelChoiceField(queryset=LineItem.objects.filter(project_id=1),
                                       empty_label="Seleccionar Partida", label='')
