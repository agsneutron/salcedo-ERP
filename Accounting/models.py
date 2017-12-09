# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Model for grouping code for accounts
class GroupingCode(models.Model):
    level = models.CharField(verbose_name="Nivel", max_length=5,)
    grouping_code = models.DecimalField(verbose_name="Código Agrupador", max_digits=20, decimal_places=2,)
    account_name = models.CharField(verbose_name="Nombre de la Cuenta y/o subcuenta", max_length=500,)

    def __str__(self):
        return str(self.grouping_code) + ": " + self.account_name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.grouping_code) + ": " + self.account_name

    class Meta:
        verbose_name_plural = 'Código Agrupador de Cuentas del SAT.'
        verbose_name = 'Código Agrupador de Cuentas del SAT.'

class Account(models.Model):
    ACTIVE = 1
    NON_ACTIVE = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Activa'),
        (NON_ACTIVE, 'Inactiva'),
    )

    DEBIT = 1    #PAYABLE RECEIVABLE
    CREDIT = 2
    DEBIT_CREDIT_CHOICES = (
        (DEBIT, "Deudora"),
        (CREDIT, "Acreedora"),
    )

    LEDGER = 1
    NO_LEDGER = 2
    LG_ACCOUNT_CHOICES = (
        (LEDGER,"Si"),
        (NO_LEDGER,"No"),
    )

    number = models.IntegerField(verbose_name="Número de Cuenta", null=False,)
    name = models.CharField(verbose_name="Nombre de la Cuenta", max_length=500, null=False,)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE, verbose_name='Estatus')

    credit_debit = models.IntegerField(choices=DEBIT_CREDIT_CHOICES, default=DEBIT, verbose_name='Naturaleza de Cuenta')
    ledger_account = models.IntegerField(choices=LG_ACCOUNT_CHOICES, default=LEDGER, verbose_name='Cuenta de Mayor')
    level = models.CharField(verbose_name="Nivel", max_length=500, null=False,)
    rubro = models.CharField(verbose_name="Rubro", max_length=500, null=False,)



    #foreign
    grouping_code = models.ForeignKey(GroupingCode, verbose_name="Código Agrupador SAT",)
    subccount = models.ForeignKey('self', verbose_name='Subcuenta de', null=True, blank=True)

    def __str__(self):
        return str(self.number) + ": " + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.number) + ": " + self.name

    class Meta:
        verbose_name_plural = 'Cuentas'
        verbose_name = 'Cuenta'