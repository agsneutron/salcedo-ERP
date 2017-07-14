# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.forms.models import model_to_dict

from django.db import models
from Logs.controller import Logs

# Create your models here.

'''
    Model for the Projects.
'''
class Project(models.Model):
    key = models.CharField(verbose_name="Clave del Proyecto", max_length=255, null=False, blank=False, unique=True)
    name = models.TextField(verbose_name="Nombre del Proyecto", max_length=1024, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Proyectos'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['name'] = str(self.name)
        return ans

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


'''
    Model for the Line Items.
'''
class LineItem(models.Model):
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    parentLineItem = models.ForeignKey('self', verbose_name="Partida Padre", null=True, blank=True)
    description = models.CharField(verbose_name="Descripción", max_length=255, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = 'Partidas'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['project'] = str(self.project.name)
        ans['parentLineItem'] = str(self.parentLineItem)
        ans['description'] = str(self.description)
        return ans

    def __str__(self):
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description

'''
    Master model to manage the concepts historical.
'''
class ConceptMaster(models.Model):
    lineItem = models.ForeignKey(LineItem, verbose_name="Partida", null=False, blank=False)
    parentConcept = models.ForeignKey('self', verbose_name="Concepto Padre", null=True, blank=True)
    key = models.CharField(verbose_name="Clave", max_length=32, null=False, blank=False, unique=True, editable=True)
    description = models.TextField(verbose_name="Descripción", max_length=4096, null=False, blank=False, editable=True)


    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['parentConcept'] = str(self.parentConcept)
        ans['description'] = str(self.description)
        return ans

    def __str__(self):
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description


'''
    Model for the units.
'''
class Unit(models.Model):
    name = models.CharField(verbose_name="Nombre de la Unidad", max_length=255, null=False, blank=False, unique=True)
    abbreviation = models.CharField(verbose_name="Abreviación", max_length=16, null=False, blank=False, unique=True)

    CONTINUOUS = "C"
    DISCRETE = "D"
    QUANTIFICATION_CHOICES = (
        (CONTINUOUS, 'Continuous'),
        (DISCRETE, 'Discrete'),
    )
    quantification = models.CharField(max_length=1, choices=QUANTIFICATION_CHOICES, default=CONTINUOUS)

    class Meta:
        verbose_name_plural = 'Unidades'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['name'] = str(self.name)
        ans['abbreviation'] = str(self.abbreviation)
        return ans

    def __str__(self):
        return self.abbreviation + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


'''
    Model for the concepts.
'''
class ConceptDetail(models.Model):
    ARCHIVED = "A"
    CURRENT = "C"
    STATUS_CHOICES =(
        (ARCHIVED, 'Archivado'),
        (CURRENT, 'Actual'),
    )

    master = models.ForeignKey(ConceptMaster, verbose_name="master", null=False, blank=False)
    unit = models.ForeignKey(Unit, verbose_name="Unidad", null=False , blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ARCHIVED)
    quantity = models.DecimalField(verbose_name='Cantidad', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    unitPrice = models.DecimalField(verbose_name='Precio Unitario', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=None, null=True)

    class Meta:
        verbose_name_plural = 'Conceptos'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['unit'] = str(self.unit.name)
        ans['status'] = str(self.status)
        ans['quantity'] = str(self.quantity)
        ans['unitPrice'] = str(self.unitPrice)
        return ans

    def __str__(self):
        return self.master.description


    def save(self, *args, **kwargs):
        canSave = True

        if self.end_date is not None and self.start_date >= self.end_date:
            Logs.log("The start date is greater than the end date")
            canSave = False


        if canSave:
            Logs.log("Saving new concept", "Te")
            super(ConceptDetail, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


'''
    Model for the Estimates.
'''
class Estimate(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=None, null=True)

    class Meta:
        verbose_name_plural = 'Estimaciones'


'''
    Model for the Progress Estimates.
'''
class ProgressEstimate(models.Model):
    estimate = models.ForeignKey(Estimate, verbose_name="Estimación", null=False , blank=False)
    key = models.CharField(verbose_name="Clave de la Estimación", max_length=8, null=False, blank=False)
    progress = models.DecimalField(verbose_name='Progreso', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    amount = models.DecimalField(verbose_name='Cantidad', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    RETAINER = "R"
    PROGRESS = "P"
    ESTIMATE = "E"
    TYPE_CHOICES =(
        (RETAINER, 'Adelanto'),
        (PROGRESS, 'Avance'),
        (ESTIMATE, 'Estimado'),
    )

    type = models.ForeignKey(Unit, verbose_name="Tipo", null=False, blank=False)


    class Meta:
        verbose_name_plural = 'Avances'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['key'] = str(self.key)
        ans['progress'] = str(self.progress)
        ans['amount'] = str(self.amount)
        ans['type'] = str(self.type)
        return ans
