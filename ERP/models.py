# coding=utf-8
from __future__ import unicode_literals

from concurrency.fields import IntegerVersionField
import os

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Count
from django.db.models import Sum
from django.db.models.fields.related import ManyToManyField
from django.db.models.query_utils import Q
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.utils.encoding import smart_text
from django.utils.timezone import now
from tinymce.models import HTMLField

from users.models import ERPUser
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from django.db import models

from django.db.models.signals import post_save

from Logs.controller import Logs
from django import forms
import datetime

import locale

from django.template import Library

#from HumanResources.models import Bank


# Create your models here.

# *********************************************************************
#                                Estado                               *
# *********************************************************************

class Pais(models.Model):
    nombrePais = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['pais'] = self.nombrePais
        return ans

    def __str__(self):
        return self.nombrePais

    def __unicode__(self):
        return self.nombrePais

    class Meta:
        verbose_name_plural = 'Países'
        verbose_name = "País"


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    pais = models.ForeignKey(Pais, null=False, blank=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class Municipio(models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['estado'] = self.estado.nombreEstado
        return ans

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio


class TipoConstruccion(models.Model):
    version = IntegerVersionField()
    nombreTipoConstruccion = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Tipos de Construcción'
        verbose_name = 'Tipo de Construcción'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['tipoconstruccion'] = self.nombreTipoConstruccion
        return ans

    def __str__(self):
        return self.nombreTipoConstruccion

    def __unicode__(self):
        return self.nombreTipoConstruccion


class Departamento(models.Model):
    version = IntegerVersionField()
    nombreDepartamento = models.TextField(verbose_name='Departamento', max_length=120, null=False, blank=False,
                                          editable=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                   editable=True)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Departamento'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreDepartamento'] = str(self.nombreDepartamento)
        return ans

    def __str__(self):
        return self.nombreDepartamento

    def __unicode__(self):
        return self.nombreDepartamento

    def save(self, *args, **kwargs):
        can_save = True

        if can_save:
            Logs.log("Saving new project", "Te")
            super(Departamento, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Department", "Te")
            self.last_edit_date = now()
            super(Departamento, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Area(models.Model):
    version = IntegerVersionField()
    nombreArea = models.TextField(verbose_name='Área', max_length=120, null=False, blank=False, editable=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                   editable=True)
    departamento = models.ForeignKey(Departamento, verbose_name="Departamento", null=False, blank=False)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Area'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreArea'] = str(self.nombreArea)
        ans['departamento'] = str(self.departamento.nombreDepartamento)
        return ans

    def __str__(self):
        return self.nombreArea

    def __unicode__(self):
        return self.nombreArea

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Area", "Te")
            super(Area, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empresa", "Te")
            self.last_edit_date = now()
            super(Area, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Puesto(models.Model):
    version = IntegerVersionField()
    nombrePuesto = models.TextField(verbose_name='Puesto', max_length=120, null=False, blank=False, editable=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                   editable=True)
    area = models.ForeignKey(Area, verbose_name='Área', null=False, blank=False)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Puesto'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombrePuesto'] = str(self.nombrePuesto)
        ans['area'] = str(self.area.nombreArea)
        return ans

    def __str__(self):
        return self.nombrePuesto

    def __unicode__(self):
        return self.nombrePuesto

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Puesto", "Te")
            super(Puesto, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empresa", "Te")
            self.last_edit_date = now()
            super(Puesto, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class ModalidadContrato(models.Model):
    version = IntegerVersionField()
    modalidadContrato = models.CharField(verbose_name='Contrato', max_length=250, null=False, blank=False,
                                         editable=True)
    duracionContrato = models.CharField(verbose_name='Duración de Contrato', max_length=20, null=False, blank=False,
                                        editable=True)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ModalidadContrato'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['modalidadContrato'] = str(self.modalidadContrato)
        ans['duracionContrato'] = str(self.duracionContrato)
        return ans

    def __str__(self):
        return self.modalidadContrato

    def __str__(self):
        return self.nombreContratista

    def __unicode__(self):
        return self.modalidadContrato

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new ModalidadContrato", "Te")
            self.last_edit_date = now()
            super(ModalidadContrato, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Empleado(models.Model):
    version = IntegerVersionField()
    nombreEmpleado = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    calle = models.TextField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
    numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
    colonia = models.TextField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
    municipio = models.ForeignKey(Municipio, verbose_name='Municipio', null=False, blank=False)
    estado = models.ForeignKey(Estado, verbose_name='Estado', null=False, blank=False)
    pais = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
    rfc = models.TextField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)
    fecha_contrato = models.DateTimeField(verbose_name='Fecha de Contrato', auto_now_add=True)
    modalidad_contrato = models.ForeignKey(ModalidadContrato, verbose_name='Contrato', null=False, blank=False)
    puesto = models.ForeignKey(Puesto, verbose_name='Puesto', null=False, blank=False)
    sueldo_inicial = models.DecimalField(verbose_name='Sueldo Inicial', decimal_places=2, blank=False, null=False,
                                         default=0, max_digits=20)
    sueldo_actual = models.DecimalField(verbose_name='Sueldo Actual', decimal_places=2, blank=False, null=False,
                                        default=0, max_digits=20)
    antiguedad = models.CharField(verbose_name='Antigüedad', max_length=50, null=False, blank=False, editable=True)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Empleado'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreEmpleado'] = str(self.nombreEmpleado)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombreEstado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['rfc'] = str(self.rfc)
        ans['fecha_contrato'] = str(self.fecha_contrato)
        ans['modalidad_contrato'] = str(self.modalidad_contrato.modalidadContrato)
        ans['puesto'] = str(self.puesto.nombrePuesto)
        ans['sueldo_inicial'] = str(self.sueldo_inicial)
        ans['sueldo_actual'] = str(self.sueldo_actual)
        ans['antiguedad'] = str(self.antiguedad)
        return ans

    def __str__(self):
        return self.nombreEmpleado

    def __unicode__(self):
        return self.nombreEmpleado

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empleado", "Te")
            self.last_edit_date = now()
            super(Empleado, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Contratista(models.Model):
    version = IntegerVersionField()
    nombreContratista = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    calle = models.CharField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
    numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
    colonia = models.CharField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
    cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=30, null=True, blank=True, editable=True)
    telefono_dos = models.CharField(verbose_name='Teléfono No.2', max_length=30, null=True, blank=True, editable=True)
    email = models.CharField(verbose_name='Correo Electrónico', max_length=60, null=False, blank=False, editable=True)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)

    # Chained key attributes. Might be duplicated, but it is required to reach the expected behaviour.
    pais = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    estado = ChainedForeignKey(Estado,
                               chained_field="pais",
                               chained_model_field="pais",
                               show_all=False,
                               auto_choose=True,
                               sort=True)
    municipio = ChainedForeignKey(Municipio,
                                  chained_field="estado",
                                  chained_model_field="estado",
                                  show_all=False,
                                  auto_choose=True,
                                  sort=True)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    # Aggregated fields as part of the requirements found in the training.
    bank = models.ForeignKey('Bank', verbose_name="Banco", null=True, blank=False)
    bank_account_name = models.CharField(verbose_name="Nombre de la Persona", max_length=512, default="", null=True, blank=True)
    bank_account = models.CharField(verbose_name="Cuenta Bancaria", max_length=16, default="", null=True, blank=True)
    CLABE = models.CharField(verbose_name="CLABE Interbancaria", max_length=18, default="", null=True, blank=True)
    employer_registration_number = models.CharField(verbose_name="Número de Registro Patronal", max_length=24, default="", null=True, blank=True)
    infonavit = models.CharField(verbose_name="Infonavit", max_length=24, default="", null=True, blank=True)
    services = models.CharField(verbose_name="Servicios que presta", max_length=4096, default="", null=True, blank=True)

    FISICA = "f"
    MORAL = "m"

    TYPE_CHOICES = (
        (FISICA, 'Física'),
        (MORAL, 'Moral'),
    )
    tax_person_type = models.CharField(verbose_name="Tipo de Persona", max_length=1, default=MORAL, null=False, blank=False, choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = 'Contratista'

        permissions = (
            ("view_list_contratista", "Can see contractor listing"),
        )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreContratista'] = str(self.nombreContratista)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombreEstado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['rfc'] = str(self.rfc)

        return ans

    def __str__(self):
        return self.nombreContratista

    def save(self, *args, **kwargs):
        can_save = True

        if can_save:
            self.last_edit_date = now()
            Logs.log("Saving new Contratista", "Te")
            super(Contratista, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Contact(models.Model):
    version = IntegerVersionField()
    contractor = models.ForeignKey(Contratista, verbose_name="Contratista", null=False, blank=True)
    name = models.CharField(verbose_name="Nombre", max_length=200, null=False, blank=False)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=True, blank=True, editable=True)
    street = models.CharField(verbose_name="Calle", max_length=200, null=False, blank=False)
    number = models.CharField(verbose_name="Número", max_length=8, null=False, blank=False)
    colony = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    post_code = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    phone_number_1 = models.CharField(verbose_name="Teléfono Principal", max_length=20, null=True, blank=True)
    phone_number_2 = models.CharField(verbose_name="Teléfono Alternativo", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=100, null=True, blank=True)

    # Attribute for the Chained Keys.
    country = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    state = ChainedForeignKey(Estado,
                              chained_field="country",
                              chained_model_field="pais",
                              show_all=False,
                              auto_choose=True,
                              sort=True,
                              verbose_name="Estado")
    town = ChainedForeignKey(Municipio,
                             chained_field="state",
                             chained_model_field="estado",
                             show_all=False,
                             auto_choose=True,
                             sort=True,
                             verbose_name="Municipio")

    # Aggregated fields as part of the requirements found in the training.
    is_legal_representantive = models.BooleanField(verbose_name="Representante Legal", default=False, null=False)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['number'] = str(self.number)
        ans['colony'] = str(self.colony)
        ans['town'] = str(self.town)
        ans['estado'] = str(self.state)
        ans['pais'] = str(self.country.nombrePais)
        ans['post_code'] = str(self.post_code)
        ans['phone_number_1'] = str(self.phone_number_1)
        ans['phone_number_2'] = str(self.phone_number_2)
        ans['contractor'] = str(self.contractor.nombreContratista)
        return ans

    def __str__(self):
        return self.name


class Empresa(models.Model):
    version = IntegerVersionField()

    nombreEmpresa = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    calle = models.CharField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
    numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
    colonia = models.CharField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
    # municipio = models.ForeignKey(Municipio, verbose_name='Municipio', null=False, blank=False)
    # estado = models.ForeignKey(Estado, verbose_name='Estado', null=False, blank=False)
    # pais = models.ForeignKey(Pais, verbose_name='Pais', null=False, blank=False)
    cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=30, null=True, blank=True, editable=True)
    telefono_dos = models.CharField(verbose_name='Teléfono No.2', max_length=30, null=True, blank=True, editable=True)
    email = models.CharField(verbose_name='Correo Electrónico', max_length=60, null=False, blank=True, editable=True)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)

    # Attribute for the Chained Keys.
    pais = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    estado = ChainedForeignKey(Estado,
                               chained_field="pais",
                               chained_model_field="pais",
                               show_all=False,
                               auto_choose=True,
                               sort=True,
                               verbose_name="Estado")
    municipio = ChainedForeignKey(Municipio,
                                  chained_field="estado",
                                  chained_model_field="estado",
                                  show_all=False,
                                  auto_choose=True,
                                  sort=True, )

    PUBLIC = "pu"
    PRIVATE = "pr"

    TYPE_CHOICES = (
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado'),
    )

    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=PUBLIC, verbose_name="Tipo")

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Empresa'

        permissions = (
            ("view_list_empresa", "Can see client listing"),
        )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreEmpresa'] = str(self.nombreEmpresa)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombreEstado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['telefono'] = str(self.telefono)
        ans['rfc'] = str(self.rfc)

        return ans

    def __str__(self):
        return self.nombreEmpresa

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empresa", "Te")
            self.last_edit_date = now()
            super(Empresa, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


def upload_contract_file(instance, filename):
    return '/'.join(['documentosFuente', instance.project.key, 'contracts',instance.contratista.nombreContratista])


class ContratoContratista(models.Model):
    version = IntegerVersionField()
    clave_contrato = models.CharField(verbose_name='Clave del Contrato', max_length=32, null=False, blank=False)
    dependencia = models.CharField(verbose_name='dependencia', max_length=50, null=False, blank=False, editable=True)
    fecha_firma = models.DateField(verbose_name='Fecha de Firma', editable=True)
    dias_pactados = models.CharField(verbose_name='Días Pactados', max_length=50, null=False, blank=False,
                                     editable=True)
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', editable=True)
    fecha_termino = models.DateField(verbose_name='Fecha de Termino', editable=True)
    lugar_ejecucion = models.TextField(verbose_name='Lugar de Ejecución', max_length=250, null=False, blank=False,
                                       editable=True)
    monto_contrato = models.DecimalField(verbose_name='Monto de Contrato', decimal_places=2, blank=False, null=False,
                                         default=0, max_digits=20)
    porcentaje_iva = models.DecimalField(verbose_name='Porcentaje del IVA', decimal_places=2, blank=False,
                                         null=False, default=0, max_digits=5)
    observaciones = models.TextField(verbose_name='Observaciones', max_length=500, null=False, blank=False,
                                     editable=True)
    no_licitacion = models.CharField(verbose_name='Número de Licitación', max_length=50, null=False, blank=True,
                                     editable=True)
    objeto_contrato = models.TextField(verbose_name='Objeto de Contrato', max_length=250, null=False, blank=False,
                                       editable=True)
    last_edit_date = models.DateTimeField(auto_now_add=True)

    # Foreign Keys:
    project = models.ForeignKey('Project', verbose_name='Proyecto', null=False, blank=False)
    modalidad_contrato = models.ForeignKey(ModalidadContrato, verbose_name='Modalidad Contrato', null=False,
                                           blank=False)
    contratista = models.ForeignKey(Contratista, verbose_name='Contratista', null=False, blank=False)

    line_item = ChainedForeignKey(
        'LineItem',
        chained_field="project",
        chained_model_field="project",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name="Partida"
    )

    concepts = ManyToManyField('Concept_Input', verbose_name="Conceptos", through='ContractConcepts')

    # Aggregated fields as part of the requirements found in the training.
    payment_distribution= models.CharField(verbose_name="Distribución del pago", max_length=1024, default="", null=True, blank=True)
    assigment_number = models.IntegerField(verbose_name="Número de asignación",  null=False, blank=False)
    pdf_version = models.FileField(verbose_name="Archivo PDF del contrato", upload_to=upload_contract_file)
    advanced_payment = models.FloatField(verbose_name="Anticipio", null=False, blank=False, default=0)


    class Meta:
        verbose_name_plural = 'Contratos'

        permissions = (
            ("view_list_contratocontratista", "Can see contractor contract listing"),
        )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['no_licitacion'] = str(self.contratista.nombreContratista)
        ans['modalidad_contrato'] = str(self.modalidad_contrato.modalidadContrato)
        ans['dependencia'] = str(self.dependencia)
        ans['codigo_obra'] = str(self.codigo_obra)
        ans['contratista'] = str(self.contratista.nombreContratista)
        ans['objeto_contrato'] = str(self.objeto_contrato)
        ans['fecha_firma'] = str(self.fecha_firma)
        ans['dias_pactados'] = str(self.dias_pactados)
        ans['fecha_inicio'] = str(self.fecha_inicio)
        ans['fecha_termino'] = str(self.fecha_termino)
        ans['lugar_ejecucion'] = str(self.lugar_ejecucion)
        ans['monto_contrato'] = str(self.monto_contrato)
        ans['monto_contrato_iva'] = str(self.monto_contrato_iva)
        ans['pago_inicial'] = str(self.pago_inicial)
        ans['pago_final'] = str(self.pago_final)
        ans['observaciones'] = str(self.observaciones)

        return ans

    def __str__(self):
        return "Clave del Contrato: " + self.clave_contrato + " -  Contratista: " + self.contratista.nombreContratista

    def __unicode__(self):
        return "Clave del Contrato: " + self.clave_contrato + " -  Contratista: " + self.contratista.nombreContratista

        # def save(self, *args, **kwargs):
        #    canSave = True

        # if canSave:
        #    Logs.log("Saving new Contrato", "Te")
        #    super(Contrato, self).save(*args, **kwargs)
        # else:
        #    Logs.log("Couldn't save")


# Class to define the concepts in a Contractor Contract.
class ContractConcepts(models.Model):
    contract = models.ForeignKey(ContratoContratista, verbose_name="Contrato", null=False, blank=False)
    concept = models.ForeignKey('Concept_Input', verbose_name="Concepto", null=False, blank=False)
    amount = models.DecimalField(verbose_name="Cantidad", null=False, blank=False, decimal_places=2, max_digits=12)


# Propietario
class Propietario(models.Model):
    version = IntegerVersionField()
    nombrePropietario = models.CharField(verbose_name="Nombre", max_length=200, null=False, blank=False)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=True, blank=True, editable=True)
    calle = models.CharField(verbose_name="Calle", max_length=200, null=False, blank=False)
    numero = models.CharField(verbose_name="Número", max_length=8, null=False, blank=False)
    colonia = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    # municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    # estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    # pais = models.ForeignKey(Pais, verbose_name="pais", null=False, blank=False)
    cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    telefono1 = models.CharField(verbose_name="Teléfono Principal", max_length=20, null=True, blank=True)
    telefono2 = models.CharField(verbose_name="Teléfono Secundario", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=100, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", null=False, blank=False)
    last_edit_date = models.DateTimeField(auto_now_add=True)
    # Attribute for the Chained Keys.
    pais = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    estado = ChainedForeignKey(Estado,
                               chained_field="pais",
                               chained_model_field="pais",
                               show_all=False,
                               auto_choose=True,
                               sort=True)
    municipio = ChainedForeignKey(Municipio,
                                  chained_field="estado",
                                  chained_model_field="estado",
                                  show_all=False,
                                  auto_choose=True,
                                  sort=True)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombrePropietario'] = str(self.nombrePropietario)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombreEstado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['telefono1'] = str(self.telefono1)
        ans['telefono_2'] = str(self.telefono2)
        ans['email'] = str(self.email)
        ans['empresa'] = str(self.empresa.nombreEmpresa)
        return ans

    def __str__(self):
        return self.nombrePropietario

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Propietario", "Te")
            super(Propietario, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


def content_file_documento_fuente(instance, filename):
    return '/'.join(['documentosFuente', instance.proyecto.key, filename])


class DocumentoFuente(models.Model):
    version = IntegerVersionField()
    descripcion = models.CharField(max_length=50, )
    documento = models.FileField(upload_to=content_file_documento_fuente, )
    tipoProyectoDetalle = models.ForeignKey('TipoProyectoDetalle', )

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion

    def delete(self, using=None):
        self.documento.delete()
        super(DocumentoFuente, self).delete(using)


# ProgramaVivienda
class TipoProyectoDetalle(models.Model):
    version = IntegerVersionField()
    proyecto = models.ForeignKey('Project', verbose_name="proyecto", null=True, blank=True)
    nombreTipoProyecto = models.CharField(verbose_name="tipo Proyecto", max_length=8, null=False, blank=False)
    numero = models.DecimalField(verbose_name='número', decimal_places=2, blank=False,
                                 null=False,
                                 default=0, max_digits=20)
    m2terreno = models.DecimalField(verbose_name='terreno (m2)', decimal_places=2, blank=False, null=False,
                                    default=0,
                                    max_digits=20)
    documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )

    class Meta:
        unique_together = [("proyecto", "nombreTipoProyecto")]
        verbose_name = "Detalle del Tipo de Proyecto"
        verbose_name_plural = "Detalles del Tipo de Proyecto"

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans

    def __str__(self):
        return self.nombreTipoProyecto

    def __unicode__(self):
        return self.nombreTipoProyecto


def project_file_document_destination(instance, filename):
    return '/'.join(['documentos_del_proyecto', instance.key, filename])


def cover_file_document_destination(instance, filename):
    return '/'.join(['documentos_del_proyecto', instance.key, 'cover_' + filename])


# Projects model.
class Project(models.Model):
    version = IntegerVersionField()
    users = models.ManyToManyField(User, verbose_name="Usuarios con Acceso", through='AccessToProject', null=False,
                                   blank=False)
    key = models.CharField(verbose_name="Clave del Proyecto", max_length=255, null=False, blank=False, unique=True)
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa Cliente", null=True, blank=False)
    nombreProyecto = models.CharField(verbose_name="nombre del proyecto", max_length=100, null=False, blank=False)
    fecha_inicial = models.DateField(default=None, null=False)
    fecha_final = models.DateField(default=None, null=False)
    tipo_construccion = models.ForeignKey(TipoConstruccion, verbose_name="Tipo de construcción", null=False,
                                          blank=False)
    portada = models.FileField(blank=True, null=True, upload_to=cover_file_document_destination,
                               verbose_name="Foto de Portada")

    ubicacion_calle = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    ubicacion_numero = models.CharField(verbose_name="numero", max_length=8, null=False, blank=False)
    ubicacion_colonia = models.CharField(verbose_name="numero", max_length=200, null=False, blank=False)
    ubicacion_pais = models.ForeignKey(Pais, verbose_name="país", null=False, blank=False)
    ubicacion_estado = ChainedForeignKey(Estado,
                                         chained_field="ubicacion_pais",
                                         chained_model_field="pais",
                                         show_all=False,
                                         auto_choose=True,
                                         sort=True)

    ubicacion_municipio = ChainedForeignKey(Municipio,
                                            chained_field="ubicacion_estado",
                                            chained_model_field="estado",
                                            show_all=False,
                                            auto_choose=True,
                                            sort=True)
    # ubicacion_estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    # ubicacion_municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    ubicacion_cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)

    latitud = models.FloatField(default=0, blank=True, null=True, )
    longitud = models.FloatField(default=0, blank=True, null=True, )

    area_superficie_escritura = models.DecimalField(verbose_name='superficie escritura', decimal_places=2, blank=False,
                                                    null=False, default=0, max_digits=20)
    area_superficie_levantamiento = models.DecimalField(verbose_name='superficie levantamiento', decimal_places=2,
                                                        blank=False, null=False, default=0, max_digits=20)

    estadolegal_documento_propiedad = models.CharField(verbose_name="Documento de propiedad", max_length=200, null=True,
                                                       blank=True)
    estadolegal_gravamen = models.CharField(verbose_name="gravamen", max_length=200, null=True, blank=True)
    estadolegal_predial = models.CharField(verbose_name="predial", max_length=200, null=True, blank=True)

    estadolegal_agua = models.CharField(verbose_name="agua", max_length=200, null=True, blank=True)

    # File Fields
    documento_propiedad = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    documento_gravamen = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    documento_agua = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    documento_predial = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    documento_agua = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    restriccion_vial = models.CharField(verbose_name="vial", max_length=200, null=True, blank=True)
    restriccion_cna = models.CharField(verbose_name="cna", max_length=200, null=True, blank=True)
    restriccion_cfe = models.CharField(verbose_name="cfe", max_length=200, null=True, blank=True)
    restriccion_pemex = models.CharField(verbose_name="pemex", max_length=200, null=True, blank=True)
    restriccion_inha = models.CharField(verbose_name="inha", max_length=200, null=True, blank=True)
    restriccion_otros = models.CharField(verbose_name="otros", max_length=200, null=True, blank=True)
    restriccion_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)

    # Fields required for the 'Uso de Suelo' report in the 'Analisis' section.
    usosuelo_pmdu = models.CharField(verbose_name="pmdu", max_length=200, null=True, blank=True)
    usosuelo_densidad = models.CharField(verbose_name="densidad", max_length=200, null=True, blank=True)
    usosuelo_loteminimo = models.DecimalField(verbose_name='lote mínimo', decimal_places=2, blank=True, null=True,
                                              default=0, max_digits=20)
    usosuelo_m2construccion = models.DecimalField(verbose_name='m2 de construcción', decimal_places=2, blank=True,
                                                  null=True, default=0, max_digits=20)
    usosuelo_arealibre = models.CharField(verbose_name="area libre", max_length=200, null=True, blank=True)
    usosuelo_altura = models.CharField(verbose_name="altura", max_length=200, null=True, blank=True)
    usosuelo_densidadrequerida = models.CharField(verbose_name="densidad requerida", max_length=200, null=True,
                                                  blank=True)

    # Fields required for the 'Hidraulica' report in the 'Analisis' section.
    hidraulica_fuente = models.CharField(verbose_name="fuente", max_length=200, null=True, blank=True)
    hidraulica_distancia = models.CharField(verbose_name="distacia", max_length=200, null=True, blank=True)
    hidraulica_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    hidraulica_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination,
                                            verbose_name="Documento de hidráulica")

    # Fields required for the 'Sanitaria' report in the 'Analisis' section.
    sanitaria_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    sanitaria_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    sanitaria_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    sanitaria_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Pluvial' report in the 'Analisis' section.
    pluvial_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    pluvial_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    pluvial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    pluvial_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Vial' report in the 'Analisis II' section.
    vial_viaacceso = models.CharField(verbose_name="vias de acceso", max_length=200, null=True, blank=True)
    vial_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    vial_carriles = models.CharField(verbose_name="carriles", max_length=200, null=True, blank=True)
    vial_seccion = models.CharField(verbose_name="seccion", max_length=200, null=True, blank=True)
    vial_tipopavimento = models.CharField(verbose_name="tipo de pavimento", max_length=200, null=True, blank=True)
    vial_estadoconstruccion = models.CharField(verbose_name="estado de construcción", max_length=200, null=True,
                                               blank=True)
    vial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    vial_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Electricidad' report in the 'Analisis II' section.
    electricidad_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    electricidad_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    electricidad_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    electricidad_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Alumbrado Público' report in the 'Analisis II' section.
    alumbradopublico_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    alumbradopublico_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    alumbradopublico_observaciones = models.CharField(verbose_name="dobservaciones", max_length=200, null=True,
                                                      blank=True)
    alumbradopublico_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Telefonia' report in the 'Analisis II' section.
    telefonia_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    telefonia_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    telefonia_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )

    # Fields required for the 'Tv Cable' report in the 'Analisis II' section.
    tvcable_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    tvcable_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)

    # Fields required for the 'Equipamiento' report in the 'Analisis II' section.
    equipamiento_a100 = models.CharField(verbose_name="a 100", max_length=200, null=True, blank=True)
    equipamiento_a200 = models.CharField(verbose_name="a 200", max_length=200, null=True, blank=True)
    equipamiento_a500 = models.CharField(verbose_name="da 500", max_length=200, null=True, blank=True)
    equipamiento_regional = models.CharField(verbose_name="regional", max_length=200, null=True, blank=True)

    # Fields required for the 'Costo' report in the 'Costo / Mercado' section.
    costo_predio = models.DecimalField(verbose_name='costo del predio', decimal_places=2, blank=True, null=True,
                                       default=0, max_digits=20)
    costo_m2 = models.DecimalField(verbose_name='m2', decimal_places=2, blank=True, null=True, default=0,
                                   max_digits=20)
    costo_escrituras = models.DecimalField(verbose_name='escrituras m2', decimal_places=2, blank=True, null=True,
                                           default=0, max_digits=20)
    costo_levantamiento = models.DecimalField(verbose_name='levantamiento m2', decimal_places=2, blank=True,
                                              null=True, default=0, max_digits=20)

    # Fields required for the 'Estudio del Mercado' report in the 'Costo / Mercado' section.
    estudiomercado_demanda = models.CharField(verbose_name="Demanda", max_length=200, null=True, blank=True)
    estudiomercado_oferta = models.CharField(verbose_name="Oferta", max_length=200, null=True, blank=True)
    estudiomercado_conclusiones = models.CharField(verbose_name="Conclusiones", max_length=200, null=True, blank=True)
    estudiomercado_recomendaciones = models.CharField(verbose_name="Recomendaciones", max_length=200, null=True,
                                                      blank=True)

    # Fields required for the 'DEfinición del Proyecto' report in the 'Costo / Mercado' section.
    definicionproyecto_alternativa = models.CharField(verbose_name="Alernativa", max_length=200, null=True, blank=True)
    definicionproyecto_tamano = models.CharField(verbose_name="Tamaño", max_length=200, null=True, blank=True)
    definicionproyecto_programa = models.CharField(verbose_name="Programa", max_length=200, null=True, blank=True)

    # Fields required for the 'Programas y Áreas' report in the 'Programa' section.
    programayarea_areaprivativa = models.DecimalField(verbose_name='area privada', decimal_places=2, blank=True,
                                                      null=True, default=0, max_digits=20)
    programayarea_caseta = models.DecimalField(verbose_name='caseta', decimal_places=2, blank=True, null=True,
                                               default=0, max_digits=20)
    programayarea_jardin = models.DecimalField(verbose_name='jardín', decimal_places=2, blank=True, null=True,
                                               default=0, max_digits=20)
    programayarea_vialidad = models.DecimalField(verbose_name='vialidad', decimal_places=2, blank=True, null=True,
                                                 default=0, max_digits=20)
    programayarea_areaverde = models.DecimalField(verbose_name='área verde', decimal_places=2, blank=True, null=True,
                                                  default=0, max_digits=20)
    programayarea_estacionamientovisita = models.DecimalField(verbose_name='estacionamiento visita', decimal_places=2,
                                                              blank=True, null=True, default=0, max_digits=20)

    # Fields required for the 'Afectacion' report in the 'Costo / Mercado' section.
    programayarea_afectacion = models.DecimalField(verbose_name='afectación', decimal_places=2, blank=True, null=True,
                                                   default=0, max_digits=20)
    programayarea_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination,
                                               verbose_name="Documento de programa y área")

    last_edit_date = models.DateTimeField(auto_now_add=True)

    # Many to many to create the project / section relation.
    sections = models.ManyToManyField('Section', through='ProjectSections', name='Secciones')

    class Meta:
        verbose_name_plural = 'Proyectos'

        permissions = (
            ("view_list_project", "Can see project listing"),
        )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['key'] = str(self.key)
        ans['nombreProyecto'] = unicode(str(self.nombreProyecto))
        ans['propietario'] = str(self.propietario.nombrePropietario)
        ans['ubicacion_municipio'] = unicode(str(self.ubicacion_municipio.nombreMunicipio))
        ans['ubicacion_estado'] = 'eh'  # unicode(str(self.ubicacion_estado.nombreEstado))
        ans['ubicacion_pais'] = unicode(str(self.ubicacion_pais.nombrePais))

        return ans

    def __str__(self):
        return self.nombreProyecto

    def __unicode__(self):
        return self.nombreProyecto

    def save(self, *args, **kwargs):
        canSave = True

        if self.fecha_final is not None and self.fecha_inicial >= self.fecha_final:
            Logs.log("The start date is greater than the end date")
            canSave = False

        if canSave:
            Logs.log("Saving new project", "Te")
            self.last_edit_date = now()
            super(Project, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class PaymentSchedule(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    MONTH_CHOICES = (
        (JANUARY, 'Enero'),
        (FEBRUARY, 'Febrero'),
        (MARCH, 'Marzo'),
        (APRIL, 'Abril'),
        (MAY, 'Mayo'),
        (JUNE, 'Junio'),
        (JULY, 'Julio'),
        (AUGUST, 'Agosto'),
        (SEPTEMBER, 'Septiembre'),
        (OCTOBER, 'Octubre'),
        (NOVEMBER, 'Noviembre'),
        (DECEMBER, 'Diciembre'),
    )
    month = models.IntegerField(verbose_name="Mes", max_length=2, choices=MONTH_CHOICES, default=JANUARY)

    YEAR_CHOICES = (
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
        (2019, '2019'),
        (2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'), (2025, '2025'),
        (2026, '2026'), (2027, '2027'), (2028, '2028'), (2029, '2029'), (2030, '2030')
    )

    year = models.IntegerField(verbose_name="Año", max_length=4,
                               choices=YEAR_CHOICES, default=2017)

    amount = models.DecimalField(verbose_name='Monto', decimal_places=2, blank=False, null=False,
                                 default=0, max_digits=20,
                                 validators=[MinValueValidator(Decimal('0.0'))])

    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Programación de Pagos'
        verbose_name = 'Programación de Pagos'
        unique_together = ('project', 'year', 'month')


@receiver(post_save, sender=Project, dispatch_uid='assing_sections')
def assign_sections(sender, instance, **kwargs):
    # Creating the sections for each saved project.
    sections = Section.objects.all()
    for section in sections:
        saved_section = ProjectSections.objects.filter(Q(project=instance) & Q(section=section))

        # If no record was found for the specific section.
        if not saved_section.exists():
            project_section = ProjectSections(project=instance, section=section, last_edit_date=now(), status=1)
            print "Saving..."
            project_section.save()


class Section(models.Model):
    section_name = models.CharField(max_length=200)
    short_section_name = models.CharField(max_length=50)
    parent_section = models.ForeignKey('Section', blank=True, default=None, null=True)

    class Meta:
        verbose_name_plural = 'Secciones'
        verbose_name = 'Sección'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['section_name'] = self.section_name
        return ans

    def __str__(self):
        if self.parent_section is not None:
            return self.parent_section.section_name + " - " + self.section_name
        else:
            return self.section_name

    def __unicode__(self):
        if self.parent_section is not None:
            return self.parent_section.section_name + " - " + self.section_name
        else:
            return self.section_name


class ProjectSections(models.Model):
    status = models.IntegerField(verbose_name="Estatus", null=False, blank=False)
    last_edit_date = models.DateTimeField(auto_now_add=True)
    # Foreign keys.
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    section = models.ForeignKey(Section, verbose_name="Sección", null=False, blank=False)

    def __str__(self):
        return str(self.project.key + " - " + self.section.section_name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.project.key + " - " + self.section.section_name)

    class Meta:
        verbose_name_plural = 'Secciones de Proyecto'
        verbose_name = 'Sección de Proyecto'

    def save(self, *args, **kwargs):
        super(ProjectSections, self).save(*args, **kwargs)


'''
    Model and upload function to the catalogs (lineitem|concepts) history.
'''


def uploaded_catalogs_destination(instance, filename):
    return '/'.join(['carga_de_catalogos', instance.project.key, filename])


class UploadedCatalogsHistory(models.Model):
    version = IntegerVersionField()
    line_items_file = models.FileField(upload_to=uploaded_catalogs_destination, null=True,
                                       verbose_name="Archivo de Partidas")

    concepts_file = models.FileField(upload_to=uploaded_catalogs_destination, null=True,
                                     verbose_name="Archivo de Conceptos")

    upload_date = models.DateTimeField(null=False, verbose_name="Fecha de carga", auto_now=True)

    # Foreign keys.
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)

    def __str__(self):
        return str(self.upload_date)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.upload_date)

    class Meta:
        verbose_name_plural = 'Cargas de catálogos'
        verbose_name = 'Carga de catálogo'

    def save(self, *args, **kwargs):
        super(UploadedCatalogsHistory, self).save(*args, **kwargs)


'''
    Model and upload function to the inputs explosion (lineitem|concepts) history.
'''


def uploaded_explotions_destination(instance, filename):
    return '/'.join(['explosion_de_insumos', instance.project.key, filename])


class UploadedInputExplotionsHistory(models.Model):
    version = IntegerVersionField()
    file = models.FileField(upload_to=uploaded_explotions_destination, null=True,
                            verbose_name="Explosión de Insumos")

    upload_date = models.DateTimeField(null=False, verbose_name="Fecha de carga", auto_now=True)

    # Foreign keys.
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)

    def __str__(self):
        return str(self.upload_date)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.upload_date)

    class Meta:
        verbose_name_plural = 'Cargas de explosiones de insumos'
        verbose_name = 'Carga de explosión de insumos'


'''
    Model for the Line Items.
'''


class LineItem(models.Model):
    version = IntegerVersionField()
    # Model attributes.
    description = models.CharField(verbose_name="Descripción", max_length=255, null=False, blank=False, unique=False)
    key = models.CharField(verbose_name="Clave", max_length=15, null=False, blank=True, unique=False, default="")

    # Foreign keys for the model.
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    parent_line_item = models.ForeignKey('self', verbose_name="Partida Padre", null=True, blank=True,
                                         related_name='parent')
    top_parent_line_item = models.ForeignKey('self', verbose_name="Partida Padre", null=True, blank=True,
                                             related_name='top_parent')

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Partidas'
        verbose_name = 'Partida'
        unique_together = ('project', 'key')

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['project'] = str(self.project.nombreProyecto)
        ans['parentLineItem'] = str(self.parent_line_item)
        ans['description'] = str(self.description)
        return ans

    def __str__(self):
        return self.key + " - "+self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.key + " - " + self.description

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Line Item", "Te")
            self.last_edit_date = now()
            super(LineItem, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    # Gets a query used by the can_be_deleted method. This helps find recursively if any child has been estimated.
    def get_query_for_estimate_search(self):
        # Get all the elements that have this object as parent
        q = Q(id=self.id)
        items = LineItem.objects.filter(parent_line_item=self.id)
        for item in items:
            q = q | item.get_query_for_estimate_search()
        return q

    def can_be_deleted(self):
        # Get all Line items with this line item as top_parent

        query = self.get_query_for_estimate_search()

        line_items = LineItem.objects.filter(query).values('id')

        for li in line_items:
            contracts = ContractConcepts.objects.filter(concept__line_item_id=li['id']).values('contract_id')
            for contract in contracts:
                contract_id = contract['contract_id']
                estimates = Estimate.objects.filter(contract_id=contract_id)

                if len(estimates) > 0:
                    return False

        return True

    def delete(self, using=None, keep_parents=False):
        if self.can_be_deleted():
            return super(LineItem, self).delete(using, keep_parents)
        print 'LineItem can\'t be deleted, it has already been estimated in the Line Item Tree'
        return False


'''
    Model for the units.
'''


class Unit(models.Model):
    version = IntegerVersionField()
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


class Concept_Input(models.Model):
    version = IntegerVersionField()
    # Choices (Dictionary) for the status attribute.
    CANCELED = "C"
    ACTIVE = "A"
    ESTATUS_CHOICES = (
        (CANCELED, 'Cancelada'),
        (ACTIVE, 'Activa'),
    )

    # Choices for the type attribute.
    CONCEPT = "C"
    INPUT = "I"
    TYPE_CHOICES = (
        (CONCEPT, 'Concepto'),
        (INPUT, 'Insumo'),
    )

    key = models.CharField(verbose_name="Clave", max_length=32, null=False, blank=False, unique=False, editable=True)
    description = models.TextField(verbose_name="Descripción", max_length=4096, null=False, blank=False, editable=True)
    status = models.CharField(max_length=2, choices=ESTATUS_CHOICES, default=ACTIVE)
    quantity = models.DecimalField(verbose_name='Cantidad', decimal_places=2, blank=False, null=False, default=0,
                                   max_digits=20)
    unit_price = models.DecimalField(verbose_name='Precio Unitario', decimal_places=2, blank=False, null=False,
                                     default=0, max_digits=20)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=CONCEPT)

    # Foreign Keys.
    line_item = models.ForeignKey(LineItem, verbose_name="Partida", null=False, blank=False, related_name='line_item')
    unit = models.ForeignKey(Unit, verbose_name="Unidad", null=False, blank=False)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Conceptos'
        verbose_name = 'Concepto'
        unique_together = ("line_item", "key")

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['unit'] = str(self.unit.name)
        ans['quantity'] = str(self.quantity)
        ans['unit_price'] = str(self.unit_price)

        return ans

    def __str__(self):
        return self.key + ' - ' + self.description

    def __unicode__(self):
        return self.key + ' - ' + self.description

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            self.last_edit_date = now()
            super(Concept_Input, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


'''
    Model for the Estimates.
'''


class Estimate(models.Model):
    version = IntegerVersionField()
    start_date = models.DateField(default=now(), null=True, blank=False, verbose_name="Fecha de inicio")
    end_date = models.DateField(default=now(), null=True, blank=False, verbose_name="Fecha de fin")
    period = models.DateField(default=now(), null=True, blank=False, verbose_name="Periodo")

    # Chained key attributes 'project'. Might be unnecessary, but it is required to reach the expected behaviour.
    contract = models.ForeignKey(ContratoContratista, verbose_name="Contrato", null=False, blank=False, default=None)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    contract_amount_override = models.DecimalField(verbose_name='Total Real', decimal_places=2, blank=False, null=False,
                                                   default=0, max_digits=20,
                                                   validators=[MinValueValidator(Decimal('0.0'))])

    # Fields to provide the Advance (payment) functionality.
    advance_payment_amount = models.DecimalField(verbose_name='Anticipo', decimal_places=2, blank=False, null=False,
                                                 default=0, max_digits=20,
                                                 validators=[MinValueValidator(Decimal('0.0'))])

    advance_payment_date = models.DateField(verbose_name="Fecha de Pago del Anticipo", null=True, blank=True)

    PAID = "P"
    NOT_PAID = "NP"

    ADVANCE_PAYMENT_STATUS_CHOICES = (
        (PAID, 'Pagado'),
        (NOT_PAID, 'No Pagado'),
    )
    advance_payment_status = models.CharField(max_length=2, choices=ADVANCE_PAYMENT_STATUS_CHOICES, default=NOT_PAID,
                                              verbose_name="Estatus del Anticipo")

    LOCKED = "L"
    UNLOCKED = "U"
    CLOSED = "C"

    ESTIMATE_LOCK_CHOICES = (
        (LOCKED, 'Bloqueada'),
        (UNLOCKED, 'Desbloquada'),
        (CLOSED, 'Cerrada'),
    )
    lock_status = models.CharField(max_length=1, choices=ESTIMATE_LOCK_CHOICES, default=LOCKED,
                                   verbose_name="Bloqueo de la Estimación")

    deduction_comments = HTMLField(verbose_name='Razones por las que Hubo Deducciones')

    # Fields to provide the Advance (payment) functionality.
    deduction_amount = models.DecimalField(verbose_name='Deducciones Por Mala Calidad', decimal_places=2, blank=False, null=False,
                                                 default=0, max_digits=20,
                                                 validators=[MinValueValidator(Decimal('0.0'))])

    # Director General
    #
    # Director  de Obras
    #
    # Vicepresidente Empresarial
    #
    # Jefe de Administración
    #
    # Presidente

    class Meta:
        verbose_name_plural = 'Estimaciones'

        permissions = (
            ("can_unlock_estimate", "Can unlock an estimate"),
        )

    def __str__(self):
        return self.contract.project.nombreProyecto + " - " + "Estimación del Contrato: " + self.contract.clave_contrato + " del Contratista: " + self.contract.contratista.nombreContratista

    def __unicode__(self):  # __unicode__ on Python 2
        return self.contract.project.nombreProyecto + " - " + "Estimación del Contrato: " + self.contract.clave_contrato + " del Contratista: " + self.contract.contratista.nombreContratista

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Estimate", "Te")
            self.last_edit_date = now()
            super(Estimate, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    def get_accumulated_amount(self, include_settlement=False):
        if include_settlement:
            accumulated_qs = ProgressEstimate.objects.filter(estimate_id=self.id).values(
                'estimate_id').annotate(
                Count('estimate_id'), accumulated=Sum('amount'))
        else:
            accumulated_qs = ProgressEstimate.objects.filter(
                Q(estimate_id=self.id) & Q(type=ProgressEstimate.PROGRESS)).values(
                'estimate_id').annotate(
                Count('estimate_id'), accumulated=Sum('amount'))

        if len(accumulated_qs) == 0:
            return self.advance_payment_amount

        accumulated = accumulated_qs[0]['accumulated']
        accumulated += self.advance_payment_amount

        return accumulated

    def is_unlocked(self):
        return self.lock_status == self.UNLOCKED

    def is_locked(self):
        return self.lock_status == self.LOCKED

    def is_open(self):
        return self.lock_status != self.CLOSED

    def get_html_approval_list(self):

        authorizations = EstimateAdvanceAuthorization.objects.filter(estimate_id=self.id)
        html = "<div style=\"text-align:left;\">"

        if len(authorizations) == 0:
            html += 'Este pago aún no ha sido autorizado.'
        else:
            for auth in authorizations:
                html += auth.full_name + "<br>"

        html += "</div>"
        return html

    def has_been_approved(self):
        authorizations = EstimateAdvanceAuthorization.objects.filter(estimate_id=self.id)
        return len(authorizations) > 0

    def has_been_approved_by(self, user_id):
        authorizations = EstimateAdvanceAuthorization.objects.filter(Q(estimate_id=self.id) & Q(user_id=user_id))
        return len(authorizations) > 0

    def user_can_approve(self, user_id):
        user = User.objects.get(pk=user_id)
        permissions = ['users.is_general_director',
                       'users.is_project_director',
                       'users.is_vicepresident',
                       'users.is_head_manager',
                       'users.is_president']

        for p in permissions:
            if user.has_perm(p):
                return True
        return False

    '''
    Model for the Progress Estimates.
'''


def generator_file_storage(instance, filename):
    project_key = instance.proyecto.key
    line_item_key = instance.estimate.concept_input.line_item.key
    concept_key = instance.estimate.concept_input.key
    estimate_id = instance.estimate.id
    progress_estimate_key = instance.key

    return '/'.join(
        ['documentosFuente', project_key, line_item_key, concept_key, estimate_id, progress_estimate_key, filename])


def content_file_generador(instance, filename):
    return '/'.join(['documentosFuente', instance.estimate.contract.project.key, filename])


class ProgressEstimate(models.Model):
    version = IntegerVersionField()
    estimate = models.ForeignKey(Estimate, verbose_name="Estimación", null=False, blank=False)
    key = models.CharField(verbose_name="Clave del Avance", max_length=9, null=False, blank=False)

    amount = models.DecimalField(verbose_name='Monto ($)', decimal_places=6, blank=False, null=False, default=0,
                                 max_digits=20)
    generator_amount = models.DecimalField(verbose_name='Cantidad del Generador', decimal_places=2, blank=False,
                                           null=False, default=0,
                                           max_digits=20)
    generator_file = models.FileField(upload_to=content_file_generador, null=True,
                                      verbose_name="Justificación", blank=True)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    PROGRESS = "P"
    SETTLEMENT = "S"
    TYPE_CHOICES = (
        (PROGRESS, 'Avance'),
        (SETTLEMENT, 'Finiquito'),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=PROGRESS, verbose_name="Tipo")

    PAID = "P"
    NOT_PAID = "NP"

    PAYMENT_STATUS_CHOICES = (
        (PAID, 'Pagado'),
        (NOT_PAID, 'No Pagado'),
    )
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default=NOT_PAID,
                                      verbose_name="Estatus del Pago")

    class Meta:
        verbose_name_plural = 'Avances de la Estimación'
        verbose_name = 'Avance de la Estimación'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['key'] = str(self.key)
        ans['progress'] = str(self.progress)
        ans['amount'] = str(self.amount)
        ans['type'] = str(self.type)
        return ans

    def __str__(self):
        return "Estimación " + self.key + "del Contrato " + self.estimate.contract.clave_contrato + " en el periodo: " \
               + str(self.estimate.period)

    def __unicode__(self):
        return "Estimación " + self.key + "del Contrato " + self.estimate.contract.clave_contrato + " en el periodo: " \
               + str(self.estimate.period)

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empresa", "Te")
            self.last_edit_date = now()
            super(ProgressEstimate, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

    def can_be_edited(self):
        return self.payment_status == self.NOT_PAID

    def get_html_approval_list(self):

        authorizations = ProgressEstimateAuthorization.objects.filter(progress_estimate_id=self.id)
        html = "<div style=\"text-align:left;\">"

        if len(authorizations) == 0:
            html += 'Este pago aún no ha sido autorizado.'
        else:
            for auth in authorizations:
                html += auth.full_name + "<br>"

        html += "</div>"
        return html

    def has_been_approved(self):
        authorizations = ProgressEstimateAuthorization.objects.filter(progress_estimate_id=self.id)
        return len(authorizations) > 0

    def has_been_approved_by(self, user_id):
        authorizations = ProgressEstimateAuthorization.objects.filter(
            Q(progress_estimate_id=self.id) & Q(user_id=user_id))
        return len(authorizations) > 0


'''
    Model for handling the progress estimate log.
'''


class ProgressEstimateLog(models.Model):
    version = IntegerVersionField()
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="Usuario", null=True, blank=True)
    description = models.TextField(verbose_name="Notas", max_length=512, null=False, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=now(), null=True, verbose_name="Fecha")

    last_edit_date = models.DateTimeField(auto_now_add=True)

    NOT_REVIEWED = 'N'
    REVIEWED = 'R'
    APPROVED = 'A'

    STATUS_CHOICES = (
        (NOT_REVIEWED, 'Sin Revisar'),
        (REVIEWED, 'Revisada'),
        (APPROVED, 'Aprobada'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NOT_REVIEWED,
                                   verbose_name="Estado de la Bitácora")



    class Meta:
        verbose_name_plural = 'Bitácoras'

        permissions = (
            ("change_log_status", "Can change project log status"),
        )

    def to_serializable_dict(self):
        answer = model_to_dict(self)
        # answer['date'] = str(self.date)
        answer['register_date'] = str(self.register_date)
        return answer

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description

    def __init__(self, *args, **kwargs):
        super(ProgressEstimateLog, self).__init__(*args, **kwargs)
        # self.user = ERPUser.objects.get(pk=1)
        # print 'user_id: ' + str(self.user.id)

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Bitacora", "Te")
            self.last_edit_date = now()
            super(ProgressEstimateLog, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


'''
    Model for the Log File.
'''


def progress_estimate_log_destination(instance, filename):
    return '/'.join(['bitacoras_de_proyecto', instance.progress_estimate_log.project.key, filename])


class LogFile(models.Model):
    version = IntegerVersionField()
    progress_estimate_log = models.ForeignKey(ProgressEstimateLog, verbose_name="Bitácora de estimación", null=False,
                                              blank=False)
    file = models.FileField(verbose_name="Archivo", null=True, blank=True, upload_to=progress_estimate_log_destination)

    last_edit_date = models.DateTimeField(auto_now_add=True)

    def to_serializable_dict(self):
        answer = model_to_dict(self)
        answer['file'] = str(self.file)
        return answer

    class Meta:
        verbose_name_plural = 'Archivo de bitácoras'

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new LogFile", "Te")
            self.last_edit_date = now()
            super(LogFile, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class SystemLogEntry(models.Model):
    action_time = models.DateTimeField(
        'action time',
        default=timezone.now,
        editable=False,
    )
    user = models.ForeignKey(
        ERPUser,
        models.CASCADE,
        verbose_name='user',
        unique=False
    )

    # Translators: 'repr' means representation (https://docs.python.org/3/library/functions.html#repr)
    label = models.CharField('label', max_length=200)
    # change_message is either a string or a JSON structure
    information = models.TextField('information', blank=True)

    # priority
    priority = models.IntegerField(verbose_name='Prioridad', null=False, blank=False, editable=False)

    class Meta:
        verbose_name = 'system log entry'
        verbose_name_plural = 'system log entries'
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        return "Value: " + self.information


class AccessToProject(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name="Obra", null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Accesos a Proyectos'
        verbose_name = 'Acceso a Proyectos'
        unique_together = ('user', 'project')

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['name'] = str(self.user.user.first_name)
        ans['project'] = str(self.project.nombreProyecto)
        return ans

    def __str__(self):
        return self.user.get_username() + " - " + self.project.nombreProyecto

    @staticmethod
    def user_has_access_to_project(user_id, project_id):
        access_objects = AccessToProject.objects.filter(Q(user_id=user_id) & Q(project_id=project_id))
        return len(access_objects) > 0

    @staticmethod
    def get_projects_for_user(user_id):
        projects = AccessToProject.objects.filter(user_id=user_id).values('project_id')
        project_ids = []
        for p in projects:
            project_ids.append(p['project_id'])
        return project_ids


class ProgressEstimateAuthorization(models.Model):
    version = IntegerVersionField()
    full_name = models.CharField(max_length=256, )
    user = models.ForeignKey(User, verbose_name="Usuario", null=False, blank=False)
    progress_estimate = models.ForeignKey(ProgressEstimate, verbose_name="Avance", null=False, blank=False)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name


class EstimateAdvanceAuthorization(models.Model):
    version = IntegerVersionField()
    full_name = models.CharField(max_length=256, )
    user = models.ForeignKey(User, verbose_name="Usuario", null=False, blank=False)
    estimate = models.ForeignKey(Estimate, verbose_name="Avance", null=False, blank=False)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name



class Bank(models.Model):
    name = models.CharField(max_length=2512, null=False, blank=False, verbose_name="Nombre")

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name