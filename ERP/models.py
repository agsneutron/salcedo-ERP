# coding=utf-8
from __future__ import unicode_literals

from concurrency.fields import IntegerVersionField
import os
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.utils.encoding import smart_text
from django.utils.timezone import now
from users.models import ERPUser
from smart_selects.db_fields import ChainedForeignKey
from django.db import models
from Logs.controller import Logs
from django import forms
import datetime


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


class Area(models.Model):
    version = IntegerVersionField()
    nombreArea = models.TextField(verbose_name='Área', max_length=120, null=False, blank=False, editable=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                   editable=True)
    departamento = models.ForeignKey(Departamento, verbose_name="Departamento", null=False, blank=False)

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


class Puesto(models.Model):
    version = IntegerVersionField()
    nombrePuesto = models.TextField(verbose_name='Puesto', max_length=120, null=False, blank=False, editable=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                   editable=True)
    area = models.ForeignKey(Area, verbose_name='Área', null=False, blank=False)

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


class ModalidadContrato(models.Model):
    version = IntegerVersionField()
    modalidadContrato = models.CharField(verbose_name='Contrato', max_length=250, null=False, blank=False,
                                         editable=True)
    duracionContrato = models.CharField(verbose_name='Duración de Contrato', max_length=20, null=False, blank=False,
                                        editable=True)

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

    class Meta:
        verbose_name_plural = 'Contratista'

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
            Logs.log("Saving new Contratista", "Te")
            super(Contratista, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class Contact(models.Model):
    version = IntegerVersionField()
    contractor = models.ForeignKey(Contratista, verbose_name="Contratista", null=False, blank=True)
    name = models.CharField(verbose_name="Nombre", max_length=200, null=False, blank=False)
    street = models.CharField(verbose_name="Calle", max_length=200, null=False, blank=False)
    number = models.CharField(verbose_name="Número", max_length=8, null=False, blank=False)
    colony = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=True, blank=True, editable=True)
    post_code = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    phone_number_1 = models.CharField(verbose_name="Teléfono Principal", max_length=20, null=True, blank=True)
    phone_number_2 = models.CharField(verbose_name="Teléfono Secundario", max_length=20, null=True, blank=True)
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
                                  sort=True)


    class Meta:
        verbose_name_plural = 'Empresa'

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
            super(Empresa, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class ContratoContratista(models.Model):
    version = IntegerVersionField()
    clave_contrato = models.CharField(verbose_name='Clave del Contrato', max_length=32, null=False, blank=False)
    dependencia = models.CharField(verbose_name='dependencia', max_length=50, null=False, blank=False, editable=True)
    fecha_firma = models.DateTimeField(verbose_name='Fecha de Firma', editable=True)
    dias_pactados = models.CharField(verbose_name='Días Pactados', max_length=50, null=False, blank=False,
                                     editable=True)
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio', editable=True)
    fecha_termino = models.DateTimeField(verbose_name='Fecha de Termino', editable=True)
    lugar_ejecucion = models.TextField(verbose_name='Lugar de Ejecución', max_length=250, null=False, blank=False,
                                       editable=True)
    monto_contrato = models.DecimalField(verbose_name='Monto de Contrato', decimal_places=2, blank=False, null=False,
                                         default=0, max_digits=20)
    monto_contrato_iva = models.DecimalField(verbose_name='Monto de Contrato con IVA', decimal_places=2, blank=False,
                                             null=False, default=0, max_digits=20)
    pago_inicial = models.DecimalField(verbose_name='Pago Inicial', decimal_places=2, blank=False, null=False,
                                       default=0, max_digits=20)
    pago_final = models.DecimalField(verbose_name='Pago Final', decimal_places=2, blank=True, null=False, default=0,
                                     max_digits=20)
    observaciones = models.TextField(verbose_name='Observaciones', max_length=500, null=False, blank=False,
                                     editable=True)
    no_licitacion = models.CharField(verbose_name='Número de Licitación', max_length=50, null=False, blank=True,
                                     editable=True)
    codigo_obra = models.CharField(verbose_name='Código de Obra', max_length=50, null=False, blank=False, editable=True)
    objeto_contrato = models.TextField(verbose_name='Objeto de Contrato', max_length=250, null=False, blank=False,
                                       editable=True)

    # Foreign Keys:
    project = models.ForeignKey('Project', verbose_name='Proyecto', null=False, blank=False)
    modalidad_contrato = models.ForeignKey(ModalidadContrato, verbose_name='Modalidad Contrato', null=False,
                                           blank=False)
    contratista = models.ForeignKey(Contratista, verbose_name='Contratista', null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Contratos'

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
        return self.codigo_obra

    def __unicode__(self):
        return self.codigo_obra

        # def save(self, *args, **kwargs):
        #    canSave = True

        # if canSave:
        #    Logs.log("Saving new Contrato", "Te")
        #    super(Contrato, self).save(*args, **kwargs)
        # else:
        #    Logs.log("Couldn't save")


# Propietario
class Propietario(models.Model):
    version = IntegerVersionField()
    nombrePropietario = models.CharField(verbose_name="Nombre", max_length=200, null=False, blank=False)
    calle = models.CharField(verbose_name="Calle", max_length=200, null=False, blank=False)
    numero = models.CharField(verbose_name="Número", max_length=8, null=False, blank=False)
    colonia = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    # municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    # estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    # pais = models.ForeignKey(Pais, verbose_name="pais", null=False, blank=False)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=True, blank=True, editable=True)
    cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    telefono1 = models.CharField(verbose_name="Teléfono Principal", max_length=20, null=True, blank=True)
    telefono2 = models.CharField(verbose_name="Teléfono Secundario", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=100, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", null=False, blank=False)

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
    user = models.ManyToManyField(ERPUser, verbose_name="Usuarios con Acceso", through='AccessToProject', null=False,
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
    ubicacion_estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    ubicacion_municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    ubicacion_cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)

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
    hidraulica_fuente = models.CharField(verbose_name="fuente", max_length=200, null=True, blank=True)
    hidraulica_distancia = models.CharField(verbose_name="distacia", max_length=200, null=True, blank=True)
    hidraulica_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    hidraulica_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination,
                                            verbose_name="Documento de hidráulica")
    sanitaria_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    sanitaria_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    sanitaria_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    sanitaria_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    pluvial_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    pluvial_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    pluvial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    pluvial_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    vial_viaacceso = models.CharField(verbose_name="vias de acceso", max_length=200, null=True, blank=True)
    vial_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    vial_carriles = models.CharField(verbose_name="carriles", max_length=200, null=True, blank=True)
    vial_seccion = models.CharField(verbose_name="seccion", max_length=200, null=True, blank=True)
    vial_tipopavimento = models.CharField(verbose_name="tipo de pavimento", max_length=200, null=True, blank=True)
    vial_estadoconstruccion = models.CharField(verbose_name="estado de construcción", max_length=200, null=True,
                                               blank=True)
    vial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    vial_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    electricidad_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    electricidad_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    electricidad_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    electricidad_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    alumbradopublico_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    alumbradopublico_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    alumbradopublico_observaciones = models.CharField(verbose_name="dobservaciones", max_length=200, null=True,
                                                      blank=True)
    alumbradopublico_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    telefonia_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    telefonia_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    telefonia_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination, )
    tvcable_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    tvcable_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    equipamiento_a100 = models.CharField(verbose_name="a 100", max_length=200, null=True, blank=True)
    equipamiento_a200 = models.CharField(verbose_name="a 200", max_length=200, null=True, blank=True)
    equipamiento_a500 = models.CharField(verbose_name="da 500", max_length=200, null=True, blank=True)
    equipamiento_regional = models.CharField(verbose_name="regional", max_length=200, null=True, blank=True)
    costo_predio = models.DecimalField(verbose_name='costo del predio', decimal_places=2, blank=True, null=True,
                                       default=0, max_digits=20)
    costo_m2 = models.DecimalField(verbose_name='m2', decimal_places=2, blank=True, null=True, default=0,
                                   max_digits=20)
    costo_escrituras = models.DecimalField(verbose_name='escrituras m2', decimal_places=2, blank=True, null=True,
                                           default=0, max_digits=20)
    costo_levantamiento = models.DecimalField(verbose_name='levantamiento m2', decimal_places=2, blank=True,
                                              null=True, default=0, max_digits=20)
    estudiomercado_demanda = models.CharField(verbose_name="Demanda", max_length=200, null=True, blank=True)
    estudiomercado_oferta = models.CharField(verbose_name="Oferta", max_length=200, null=True, blank=True)
    estudiomercado_conclusiones = models.CharField(verbose_name="Conlusiones", max_length=200, null=True, blank=True)
    estudiomercado_recomendaciones = models.CharField(verbose_name="Recomendaciones", max_length=200, null=True,
                                                      blank=True)
    definicionproyecto_alternativa = models.CharField(verbose_name="Alernativa", max_length=200, null=True, blank=True)
    definicionproyecto_tamano = models.CharField(verbose_name="Tamaño", max_length=200, null=True, blank=True)
    definicionproyecto_programa = models.CharField(verbose_name="Programa", max_length=200, null=True, blank=True)

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
    programayarea_afectacion = models.DecimalField(verbose_name='afectación', decimal_places=2, blank=True, null=True,
                                                   default=0, max_digits=20)
    programayarea_documento = models.FileField(blank=True, null=True, upload_to=project_file_document_destination,
                                               verbose_name="Documento de programa y área")
    latitud = models.FloatField(default=0, blank=True, null=True, )
    longitud = models.FloatField(default=0, blank=True, null=True, )

    # tipoProyectoDetalle = models.ManyToManyField(TipoProyectoDetalle,null=True,blank=True, )





    class Meta:
        verbose_name_plural = 'Proyectos'

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
            super(Project, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


'''
    Model and upload function to the catalogs (lineitem|concepts) history.
'''


def uploaded_catalogs_destination(instance, filename):
    return '/'.join(['carga_de_catalogos', instance.project.key, filename])


class UploadedCatalogsHistory(models.Model):
    version = IntegerVersionField()
    line_items_file = models.FileField(upload_to=uploaded_catalogs_destination, null=True,
                                       verbose_name="Archivo de partidas")

    concepts_file = models.FileField(upload_to=uploaded_catalogs_destination, null=True,
                                     verbose_name="Archivo de conceptos")

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
    key = models.CharField(verbose_name="Clave", max_length=8, null=False, blank=True, unique=False, default="")

    # Foreign keys for the model.
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    parent_line_item = models.ForeignKey('self', verbose_name="Partida Padre", null=True, blank=True)

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
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description


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
    line_item = models.ForeignKey(LineItem, verbose_name="Partida", null=False, blank=False)
    unit = models.ForeignKey(Unit, verbose_name="Unidad", null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Conceptos'
        verbose_name = 'Concepto'
        unique_together = ("line_item", "key")

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['unit'] = str(self.unit.name)
        ans['quantity'] = str(self.quantity)
        ans['unitPrice'] = str(self.unit_price)
        return ans

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description


'''
    Model for the Estimates.
'''


class Estimate(models.Model):
    version = IntegerVersionField()
    start_date = models.DateTimeField(default=now(), null=True, blank=False, verbose_name="Fecha de inicio")
    end_date = models.DateTimeField(default=now(), null=True, blank=False, verbose_name="Fecha de fin")
    period = models.DateTimeField(default=now(), null=True, blank=False, verbose_name="Periodo")

    # Chained key attributes. Might be duplicated, but it is required to reach the expected behaviour.
    line_item = models.ForeignKey(LineItem, verbose_name="Partidas", null=True, blank=False, default=None)
    concept_input = ChainedForeignKey(Concept_Input,
                                      chained_field="line_item",
                                      chained_model_field="line_item",
                                      show_all=False,
                                      auto_choose=True,
                                      sort=True,
                                      null=False,
                                      blank=False,
                                      verbose_name="Concepto / Insumo"
                                      )

    class Meta:
        verbose_name_plural = 'Estimaciones'

    def __str__(self):
        return "Partida: " + self.line_item.description[
                             :45] + " Concepto: " + self.concept_input.description + " Periodo: " + str(self.period)

    def __unicode__(self):  # __unicode__ on Python 2
        line_item_display = ""
        concept_input_display = ""

        if len(self.line_item.description) > 40:
            line_item_display = self.line_item.description[0:40] + "..."
        else:
            line_item_display = self.line_item.description

        if len(self.concept_input.description) > 40:
            concept_input_display = self.concept_input.description[0:40] + "..."
        else:
            concept_input_display = self.concept_input.description

        return "Partida: " + line_item_display + " Concepto: " + concept_input_display + " Periodo: " + str(self.period)


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
    return '/'.join(['documentosFuente', instance.estimate.concept_input.line_item.project.key, filename])


class ProgressEstimate(models.Model):
    version = IntegerVersionField()
    estimate = models.ForeignKey(Estimate, verbose_name="Estimación", null=False, blank=False)
    key = models.CharField(verbose_name="Clave de la Estimación", max_length=8, null=False, blank=False)
    progress = models.DecimalField(verbose_name='Progreso', decimal_places=2, blank=False, null=False, default=0,
                                   max_digits=5)
    amount = models.DecimalField(verbose_name='Cantidad', decimal_places=1, blank=False, null=False, default=0,
                                 max_digits=4)
    generator_amount = models.DecimalField(verbose_name='Cantidad del Generador', decimal_places=2, blank=False,
                                           null=False, default=0,
                                           max_digits=20)
    generator_file = models.FileField(upload_to=content_file_generador, null=True,
                                      verbose_name="Archivo del Generador", blank=True)
    RETAINER = "R"
    PROGRESS = "P"
    ESTIMATE = "E"
    TYPE_CHOICES = (
        (RETAINER, 'Adelanto'),
        (PROGRESS, 'Avance'),
        (ESTIMATE, 'Estimado'),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=PROGRESS, verbose_name="Tipo")

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
        return self.estimate.concept_input.description + " - " + str(self.estimate.period) + " - " + self.key

    def __unicode__(self):
        return self.estimate.concept_input.description + " - " + str(self.estimate.period) + " - " + self.key


'''
    Model for handling the progress estimate log.
'''


class ProgressEstimateLog(models.Model):
    version = IntegerVersionField()
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    user = models.ForeignKey(ERPUser, verbose_name="Usuario", null=True, blank=True)
    description = models.TextField(verbose_name="Descripción", max_length=512, null=False, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=now(), null=True, verbose_name="Fecha")

    class Meta:
        verbose_name_plural = 'Bitácoras'

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


'''
    Model for the Log File.
'''


def progress_estimate_log_destination(instance, filename):
    return '/'.join(['bitacoras_de_proyecto', instance.progress_estimate_log.project.key, filename])


class LogFile(models.Model):
    version = IntegerVersionField()
    progress_estimate_log = models.ForeignKey(ProgressEstimateLog, verbose_name="Bitácora de estimación", null=False,
                                              blank=False)
    file = models.FileField(verbose_name="Archivo", null=True, blank=True, upload_to=progress_estimate_log_destination,
                            default="")
    mime = models.CharField(verbose_name="MIME", max_length=128, null=False, blank=False)

    def to_serializable_dict(self):
        answer = model_to_dict(self)
        answer['file'] = str(self.file)
        return answer

    class Meta:
        verbose_name_plural = 'Archivo de bitácoras'


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
    user = models.ForeignKey(ERPUser, verbose_name="Usuario")
    project = models.ForeignKey(Project, verbose_name="Obra", null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Accesos a Proyectos'
        verbose_name = 'Acceso a Proyecot'
        unique_together = ('user', 'project')

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['name'] = str(self.user.user.first_name)
        ans['project'] = str(self.project.nombreProyecto)
        return ans

    def __str__(self):
        return self.user.user.get_username() + " - " + self.project.nombreProyecto
