# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Accounting.models import *
from Accounting.forms import *

# Shared Catalogs Imports.
from SharedCatalogs.models import GroupingCode, Account


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
        ("", {
            'fields': (
            'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
            'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
            'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status', 'type',)
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CommercialAllyAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        type = request.GET.get('type')
        title = ""
        extra['type'] = type
        if type == "0":
            title = "Proveedor"
        elif type == "1":
            title = "Acreedor"
        elif type == "2":
            title = "Tercero"

        extra['title'] = str(title)
        print "title" + title
        print "type" + type

        return super(CommercialAllyAdmin, self).add_view(request, form_url, extra_context=extra)


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
admin.site.register(CommercialAllyContact)



