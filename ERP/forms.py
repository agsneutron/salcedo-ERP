from django import forms
from ERP.models import Project, TipoProyectoDetalle
from datetime import datetime
from django.utils.safestring import mark_safe
import os
from django.conf import settings

class TipoProyectoDetalleAddForm(forms.ModelForm):
    class Meta:
        model = TipoProyectoDetalle
        fields = '__all__'

    def save(self, commit=True):
        instance = super(TipoProyectoDetalleAddForm, self).save(commit=False)
        return super(TipoProyectoDetalleAddForm, self).save(commit)

class AddProyectoForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'


    def save(self, commit=True):
        instance = super(AddProyectoForm, self).save(commit=False)

        return super(AddProyectoForm, self).save(commit=commit)