# coding=utf-8
from __future__ import unicode_literals

from datetime import date

import tinymce
from django.db import models
from django.utils.timezone import now

# Model for grouping code for accounts
from django.forms import model_to_dict
from django.utils.timezone import now
from smart_selects.db_fields import ChainedForeignKey

from ERP.models import Pais, Estado, Municipio
from Logs.controller import Logs
from django.contrib import messages

# Shared Catalogs Imports.
from SharedCatalogs.models import Pais, Estado, Municipio, Bank, SATBank, GroupingCode, Account, InternalCompany


# Model for accounting policy
class FiscalPeriod(models.Model):
    OPENED = 1
    CLOSED = 2
    AUDITED = 3

    STATUS_CHOICES = (
        (OPENED, 'Abierto'),
        (CLOSED, 'Cerrado'),
        (AUDITED, 'Auditado'),
    )

    accounting_year = models.IntegerField(verbose_name="Ejercicio Contable", null=False, )

    MONTH_CHOICES = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )
    account_period = models.IntegerField(verbose_name="Mes", choices=MONTH_CHOICES, default=1)

    status = models.IntegerField(choices=STATUS_CHOICES, default=OPENED, verbose_name='Estatus')

    def __str__(self):
        return self.get_account_period_display() + " " + str(self.accounting_year)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.get_account_period_display() + " " + str(self.accounting_year)

    @staticmethod
    def get_month_name_from_number(number):
        return FiscalPeriod.MONTH_CHOICES[number - 1][1]

    @staticmethod
    def get_month_number_from_substring(substring):
        months = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12
        }

        months_numbers_array = []
        for key, value in months.items():
            if substring in key:
                months_numbers_array.append(value)

        return months_numbers_array

    class Meta:
        verbose_name_plural = 'Años contables'
        verbose_name = 'Año Contable'


# Model for accounting policy
class TypePolicy(models.Model):
    name = models.CharField(verbose_name='Tipo de Póliza', null=False, blank=False, max_length=256)
    balanced_accounts = models.BooleanField(verbose_name="Cuadrar póliza", default=False)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Tipos de Póliza'
        verbose_name = 'Tipo de Póliza'


# Model for accounting policy
class AccountingPolicy(models.Model):
    fiscal_period = models.ForeignKey(FiscalPeriod, verbose_name='Periodo Fiscal', null=False, blank=False)
    type_policy = models.ForeignKey(TypePolicy, verbose_name='Tipo de Póliza', null=False, blank=False)
    folio = models.IntegerField("Folio", blank=True, null=True)
    registry_date = models.DateField(default=now, null=False, blank=False, verbose_name="Fecha de Registro")
    description = models.CharField(verbose_name="Concepto", max_length=4096, null=False, blank=False)
    reference = models.CharField(verbose_name="Referencia", max_length=1024, null=False, blank=False)
    internal_company = models.ForeignKey(InternalCompany, verbose_name='Empresa Interna', null=True, blank=True)

    def __str__(self):
        return str(self.type_policy) + ": " + str(self.folio) + " del periodo fiscal " + str(self.fiscal_period)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.type_policy) + ": " + str(self.folio) + " del periodo fiscal " + str(self.fiscal_period)

    class Meta:
        verbose_name_plural = 'Pólizas Contables'
        verbose_name = 'Póliza contable'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['registry_date'] = str(self.registry_date)
        ans['fiscal_period_year'] = str(self.fiscal_period.accounting_year)
        ans['fiscal_period_month'] = str(self.fiscal_period.get_account_period_display())
        ans['type_policy_name'] = str(self.type_policy.name)
        return ans


# Model for accounting policy
class AccountingPolicyDetail(models.Model):
    accounting_policy = models.ForeignKey(AccountingPolicy, verbose_name='Póliza', null=False, blank=False)
    account = models.ForeignKey(Account, verbose_name='Cuenta', null=False, blank=False, limit_choices_to={
        'type_account': 'D',
    })
    description = models.CharField(verbose_name="Concepto", max_length=4096, null=False, blank=False)
    debit = models.FloatField(verbose_name="Debe", null=False, blank=False, default=0)
    credit = models.FloatField(verbose_name="Haber", null=False, blank=False, default=0)
    registry_date = models.DateField(null=False, blank=False, verbose_name="Fecha de Registro")

    def __str__(self):
        return str(self.account.number) + ": " + self.account.name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.account.number) + ": " + self.account.name

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['registry_date'] = self.registry_date.strftime('%m/%d/%Y')
        return ans

    class Meta:
        verbose_name_plural = 'Detalle de Pólizas'
        verbose_name = 'Detalle de Póliza'

    def save(self, *args, **kwargs):
        self.registry_date = now()
        super(AccountingPolicyDetail, self).save(*args, **kwargs)


class CommercialAlly(models.Model):
    ACTIVE = 1
    NON_ACTIVE = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Activo'),
        (NON_ACTIVE, 'Inactivo'),
    )

    PROVIDER = 0
    CREDITOR = 1
    THIRD_PARTY = 2

    # If you edit this, modify method CommercialAlly.get_delete_redirect_page.
    COMMERCIAL_ALLY_TYPE_CHOICES = (
        (PROVIDER, 'Proveedor'),
        (CREDITOR, 'Acreedor'),
        (THIRD_PARTY, 'Tercero'),
    )

    name = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    colony = models.CharField(verbose_name="Colonia", max_length=255, null=False, blank=False)
    street = models.CharField(verbose_name="Calle", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    zip_code = models.CharField(verbose_name="Código Postal", max_length=5, null=False, blank=False)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)
    curp = models.CharField(verbose_name="CURP", max_length=18, null=False, blank=False, unique=True)
    phone_number = models.CharField(verbose_name="Teléfono", max_length=20, null=False, blank=False)
    phone_number_2 = models.CharField(verbose_name="Teléfono 2", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Email", max_length=255, null=False, blank=False)
    cellphone_number = models.CharField(verbose_name="Celular", max_length=20, null=False, blank=True)
    office_number = models.CharField(verbose_name="Teléfono de Oficina", max_length=20, null=False, blank=True)
    extension_number = models.CharField(verbose_name="Número de Extensión", max_length=10, null=False, blank=True)

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

    last_edit_date = models.DateTimeField(auto_now_add=True)
    register_date = models.DateField(default=date.today)

    accounting_account = models.ForeignKey(Account, verbose_name="Cuenta Contable", blank=False, null=False)
    bank = models.ForeignKey(Bank, verbose_name="Banco", null=True, blank=False)
    bank_account_name = models.CharField(verbose_name="Nombre del Titular", max_length=512, default="", null=True,
                                         blank=True)
    bank_account = models.CharField(verbose_name="Cuenta Bancaria", max_length=16, default="", null=True, blank=True)
    # CLABE = models.CharField(verbose_name="CLABE Interbancaria", max_length=18, default="", null=True, blank=True)
    employer_registration_number = models.CharField(verbose_name="Número de Registro Patronal", max_length=24,
                                                    default="", null=True, blank=True)
    services = tinymce.models.HTMLField(verbose_name='Servicios que presta', null=True, blank=True,max_length=4096)


    FISICA = "f"
    MORAL = "m"

    TYPE_CHOICES = (
        (FISICA, 'Física'),
        (MORAL, 'Moral'),
    )
    tax_person_type = models.CharField(verbose_name="Tipo de Persona", max_length=1, default=MORAL, null=False,
                                       blank=False, choices=TYPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE, verbose_name='Estatus')
    type = models.IntegerField(choices=COMMERCIAL_ALLY_TYPE_CHOICES, default=PROVIDER, verbose_name='Tipo')

    class Meta:
        verbose_name_plural = 'Aliado Comercial'
        verbose_name = 'Aliado Comercial'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['register_date'] = self.register_date.strftime('%m/%d/%Y')
        ans['accounting_account'] = str(self.accounting_account.number)
        ans['type'] = self.get_type_display()
        # ans['id'] = str(self.id)
        # ans['name'] = str(self.name)
        # ans['street'] = str(self.street)
        # ans['number'] = str(self.number)
        # ans['outdoor_number'] = str(self.colonia)
        # ans['town'] = str(self.municipio.nombreMunicipio)
        # ans['state'] = str(self.estado.nombreEstado)
        # ans['country'] = str(self.pais.nombrePais)
        # ans['cp'] = str(self.cp)
        # ans['rfc'] = str(self.rfc)

        return ans

    def __str__(self):
        return self.name

    def get_delete_redirect_page(self):
        if self.type == self.PROVIDER:
            return 'searchprovider'
        elif self.type == self.CREDITOR:
            return 'searchcreditors'
        else:
            return 'searchthird'

    def save(self, *args, **kwargs):
        can_save = True

        if can_save:
            self.last_edit_date = now()
            Logs.log("Saving new commercial ally", "Te")
            super(CommercialAlly, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class CommercialAllyContact(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)
    street = models.CharField(verbose_name="Calle", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    colony = models.CharField(verbose_name="Colonia", max_length=255, null=False, blank=False)
    zip_code = models.CharField(verbose_name="Código Postal", max_length=5, null=False, blank=False)
    phone_number = models.CharField(verbose_name="Teléfono Principal", max_length=20, null=False, blank=False)
    secondary_number = models.CharField(verbose_name="Teléfono Secundario", max_length=20, null=False, blank=True)
    email = models.CharField(verbose_name="Email", max_length=255, null=False, blank=False)
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

    is_legal_representative = models.BooleanField(verbose_name="Es Representante Legal", default=False)
    commercialally = models.ForeignKey(CommercialAlly, verbose_name="Aliado Comercial", null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Contactos'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        # ans['id'] = str(self.id)

        return ans

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        can_save = True

        if can_save:
            Logs.log("Saving new commercial ally contact", "Te")
            super(CommercialAllyContact, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")
