# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.forms.models import model_to_dict

# Create your models here.
from django.forms import model_to_dict
from smart_selects.db_fields import ChainedForeignKey

rfc_regex = RegexValidator(regex="^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$",
                             message="El RFC que proporcionas es incorrecto.")

onlynum_regex = RegexValidator(regex="[0-9]",
                             message="Este campo solo acepta números.")


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


class SATBank(models.Model):
    key = models.CharField(verbose_name="Clave Cuenta SAT", null=False, max_length=3)
    name = models.CharField(verbose_name="Nombre Cuenta SAT", max_length=100, null=False, )
    business_name = models.CharField(verbose_name="Razón social", max_length=500, null=False, )

    def __str__(self):
        return self.key + ": " + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.key + ": " + self.name

    class Meta:
        verbose_name_plural = 'Bancos del SAT.'
        verbose_name = 'Bancos del SAT.'


class Bank(models.Model):
    name = models.CharField(max_length=2512, null=False, blank=False, verbose_name="Nombre")
    sat_bank = models.OneToOneField(SATBank, verbose_name="Banco del SAT", null=True, blank=True)
    accounting_account = models.ForeignKey('Account', verbose_name="Cuenta Contable", blank=False, null=False)
    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


class GroupingCode(models.Model):
    level = models.IntegerField(verbose_name="Nivel", null=True, default=0)
    grouping_code = models.DecimalField(verbose_name="Código Agrupador", max_digits=20, decimal_places=2, )
    account_name = models.CharField(verbose_name="Nombre de la Cuenta y/o subcuenta", max_length=500, )

    def __str__(self):
        return str(self.grouping_code) + " " + self.account_name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.grouping_code) + " " + self.account_name

    def __hash__(self):
        return self.grouping_code

    def __eq__(self, other):
        if other is None:
            return False

        if type(other) != GroupingCode:
            return False

        return self.grouping_code == other.grouping_code

    class Meta:
        verbose_name_plural = 'Código Agrupador de Cuentas del SAT.'
        verbose_name = 'Código Agrupador de Cuentas del SAT.'


class ItemAccount(models.Model):
    key = models.IntegerField(verbose_name="clave", null=False, unique=True)
    name = models.CharField(verbose_name="Nombre del Rubro", max_length=100, )

    def __str__(self):
        return str(self.key) + ": " + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.key) + ": " + self.name

    class Meta:
        verbose_name_plural = 'Rubros de Cuentas'
        verbose_name = 'Rubro de Cuenta'


class Account(models.Model):
    ACTIVE = 1
    NON_ACTIVE = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Activa'),
        (NON_ACTIVE, 'Inactiva'),
    )

    DEBIT = 1  # PAYABLE RECEIVABLE
    CREDIT = 2
    DEBIT_CREDIT_CHOICES = (
        (DEBIT, "Deudora"),
        (CREDIT, "Acreedora"),
    )

    ACCUMULATION = 'A'
    DETAIL = 'D'
    TYPE_ACCOUNT_CHOICES = (
        (ACCUMULATION, "Acumulativa"),
        (DETAIL, "Detalle"),
    )

    number = models.DecimalField(verbose_name='Número de Cuenta', decimal_places=0, blank=False, null=False,
                                         default=0, max_digits=25)
    name = models.CharField(verbose_name="Nombre de la Cuenta", max_length=500, null=False, )
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE, verbose_name='Estatus')

    nature_account = models.IntegerField(choices=DEBIT_CREDIT_CHOICES, default=DEBIT,
                                         verbose_name='Naturaleza de Cuenta')
    #ledger_account = models.IntegerField(choices=LG_ACCOUNT_CHOICES, default=LEDGER, verbose_name='Cuenta de Mayor', null=True)
    #level = models.CharField(verbose_name="Nivel", max_length=500, null=True, )

    type_account = models.CharField(choices=TYPE_ACCOUNT_CHOICES, verbose_name='Tipo de Cuenta',
                                         null=False,max_length=1)
    # foreign
    grouping_code = models.ForeignKey(GroupingCode, verbose_name="Código Agrupador SAT", )
    subsidiary_account = models.ForeignKey('self', verbose_name='Subcuenta de', null=True, blank=True)
    internal_company = models.ForeignKey('InternalCompany', verbose_name='Empresa Interna', null=True, blank=True)

    def __str__(self):
        return str(self.number) + ": " + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.number) + ": " + self.name

    class Meta:
        verbose_name_plural = 'Cuentas'
        verbose_name = 'Cuenta'

    def to_serializable_dict(self):
        dict = model_to_dict(self)
        dict['nature_account'] = self.get_nature_account_display()
        #dict['ledger_account'] = self.get_ledger_account_display()
        dict['grouping_code'] = self.grouping_code.account_name
        dict['status'] = self.get_status_display()
        if self.subsidiary_account is not None:
            dict['subsidiary_account'] = self.subsidiary_account.number

        return dict


class InternalCompany(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=256, null=False, blank=False)
    rfc = models.CharField(verbose_name="RFC de la Empresa", max_length=15, null=False, blank=False, unique=True,
                           validators=[rfc_regex])
    colony = models.CharField(verbose_name="Colonia*", max_length=255, null=False, blank=False)
    street = models.CharField(verbose_name="Calle*", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior*", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    zip_code = models.CharField(verbose_name="Código Postal*", null=False, blank=False, validators=[onlynum_regex],
                                max_length=5)

    # Attribute for the Chained Keys.
    country = models.ForeignKey(Pais, verbose_name="País*", null=False, blank=False)
    state = ChainedForeignKey(Estado,
                              chained_field="country",
                              chained_model_field="pais",
                              show_all=False,
                              auto_choose=True,
                              sort=True,
                              verbose_name="Estado*")
    town = ChainedForeignKey(Municipio,
                             chained_field="state",
                             chained_model_field="estado",
                             show_all=False,
                             auto_choose=True,
                             sort=True,
                             verbose_name="Municipio*")

    class Meta:
        verbose_name_plural = "Empresas Internas"
        verbose_name = "Empresa Interna"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name