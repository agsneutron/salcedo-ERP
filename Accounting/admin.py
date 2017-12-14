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

@admin.register(CommercialAlly)
class CommercialAllyAdmin(admin.ModelAdmin):
    form = CommercialAllyForm

    fieldsets = (
        ("Aliado Comercial ", {
            'fields': (
            'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
            'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
            'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status',)
        }),
    )

# @admin.register(Creditors)
# class CreditorsAdmin(admin.ModelAdmin):
#     form = CreditorsForm
#
#     fieldsets = (
#         ("Acreedores", {
#             'fields': (
#             'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
#             'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
#             'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status',)
#         }),
#     )

admin.site.register(GroupingCode)
admin.site.register(Account)
admin.site.register(CommercialAllyContact)


