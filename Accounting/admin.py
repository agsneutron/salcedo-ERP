# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.db.models.query_utils import Q

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
    actions = None

    fieldsets = (
        ("Póliza", {
            'fields': (
            'fiscal_period', 'type_policy', 'folio', 'registry_date', 'description',)
        }),
    )

    list_display = ('folio','type_policy', 'fiscal_period', 'description')


@admin.register(FiscalPeriod)
class FiscalPeriodAdmin(admin.ModelAdmin):
    form = FiscalPeriodForm

    fieldsets = (
        ("Periodo Fiscal", {
            'fields': (
            'accounting_year', 'account_period', 'status')
        }),
    )

    list_display = ('account_period', 'accounting_year', 'status')
    actions = None
    search_fields = ('account_period', 'accounting_year')
    ordering = ('account_period', 'accounting_year', 'status')
    list_per_page = 25

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(FiscalPeriodAdmin, self).get_search_results(request, queryset, search_term)


        if search_term is not "":
            keywords = search_term.split(" ")

            years_array = None          # Set to none to control whether or not the user is searching for the year.
            months_numbers_array = []

            for word in keywords:
                # Finding the month number depending on the given word.
                result = FiscalPeriod.get_month_number_from_substring(word.lower())
                for number in result:
                    months_numbers_array.append(number)

                # Checking for the query in the years.
                try:
                    year = int(word)
                    if years_array is None:
                        # If None, but no exception ocurred, turn the variable into an array.
                        years_array = []
                        # Append the value.
                        years_array.append(year)
                    else:
                        # Append the value.
                        years_array.append(year)

                except ValueError:
                    pass

            # Filter for the months using the OR operator.
            queryset |= FiscalPeriod.objects.filter(Q(account_period__in=months_numbers_array))

            # Filter for the years using the AND operator.
            if years_array is not None:
                queryset &= FiscalPeriod.objects.filter(Q(accounting_year__in=years_array))

        return queryset, use_distinct



@admin.register(TypePolicy)
class TypePolicyAdmin(admin.ModelAdmin):
    form = TypePolicyForm

    fieldsets = (
        ("Tipo de Póliza", {
            'fields': (
            'name', 'balanced_accounts')
        }),
    )

    list_display = ('name', 'balanced_accounts')
    search_fields = ('name',)
    list_per_page = 25


@admin.register(CommercialAlly)
class CommercialAllyAdmin(admin.ModelAdmin):
    form = CommercialAllyForm

    fieldsets = (
        ("Aliado Comercial ", {
            'fields': (
            'name', 'curp','rfc','phone_number','cellphone_number','office_number','extension_number','street','outdoor_number',
            'indoor_number','colony','zip_code','country','state','town','accounting_account','bank',
            'bank_account_name','bank_account','employer_registration_number','services','tax_person_type','status', 'type',)
        }),
    )

    list_display = ('name', 'rfc','phone_number','type','status')
    actions = None


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



