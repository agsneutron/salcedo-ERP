# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Accounting.models import *
from Accounting.forms import *


# Admin for the inline documents of the current education of an employee.
class AccountingPolicyDetailInline(admin.TabularInline):
    model = AccountingPolicyDetail
    extra = 1

    fieldsets = (
        ("Detalle", {
            'fields': ('account', 'description','debit','credit')
        }),
    )

@admin.register(AccountingPolicy)
class AccountingPolicyAdmin(admin.ModelAdmin):
    form = AccountingPolicyForm
    inlines = (AccountingPolicyDetailInline,)

    fieldsets = (
        ("Póliza", {
            'fields': (
            'fiscal_period', 'type_policy', 'folio', 'registry_date', 'description',)
        }),
    )

@admin.register(FiscalPeriod)
class FiscalPeriodAdmin(admin.ModelAdmin):
    form = FiscalPeriodForm

    fieldsets = (
        ("Periodo Fiscal", {
            'fields': (
            'accounting_year', 'account_period', 'status')
        }),
    )

@admin.register(TypePolicy)
class TypePolicyAdmin(admin.ModelAdmin):
    form = TypePolicyForm

    fieldsets = (
        ("Tipo de Póliza", {
            'fields': (
            'name', 'balanced_accounts')
        }),
    )

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    form = ProviderForm

    fieldsets = (
        ("Proveedor", {
            'fields': (
            'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
            'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
            'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status',)
        }),
    )

@admin.register(Creditors)
class CreditorsAdmin(admin.ModelAdmin):
    form = CreditorsForm

    fieldsets = (
        ("Acreedores", {
            'fields': (
            'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
            'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
            'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status',)
        }),
    )

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

    fieldsets = (
        ("Cuentas", {
            'fields': (
            'number','name','status','nature_account','ledger_account','level','item','grouping_code','subsidiary_account')
        }),
    )

admin.site.register(GroupingCode)



