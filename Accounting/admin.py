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



admin.site.register(GroupingCode)
admin.site.register(Account)
admin.site.register(Provider)

