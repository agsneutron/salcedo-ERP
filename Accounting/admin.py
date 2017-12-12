# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Accounting.models import *


@admin.register(AccountingPolicy)
class AccountingPolicyAdmin(admin.ModelAdmin):
    form = AccountingPolicy


    fieldsets = (
        ("Datos de Empleado", {
            'fields': ('fiscal_period', 'type_policy', 'folio', 'registry_date', 'description')
        }),
        ("Datos Personales", {
            'fields': (
                'name', 'first_last_name', 'second_last_name', 'birthdate', 'birthplace', 'gender', 'marital_status',
                'curp', 'rfc', 'tax_regime', 'social_security_number', 'social_security_type', 'blood_type','street', 'outdoor_number', 'indoor_number', 'colony',
                'country', 'state', 'town', 'zip_code', 'phone_number', 'cellphone_number', 'office_number',
                'extension_number', 'personal_email', 'work_email', 'driving_license_number',
                'driving_license_expiry_date')
        }),
    )


admin.site.register(GroupingCode)
admin.site.register(Account)
admin.site.register(Provider)