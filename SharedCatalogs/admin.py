# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from SharedCatalogs.forms import InternalCompanyForm
from SharedCatalogs.models import InternalCompany, SATBank

@admin.register(InternalCompany)
class InternalCompanyAdmin(admin.ModelAdmin):
    form = InternalCompanyForm

    fieldsets = (
        ("Empresa", {
            'fields': (
                'name', 'rfc', 'colony', 'street', 'outdoor_number', 'indoor_number', 'zip_code', 'country', 'state', 'town', 'logo_file')
        }),
    )


admin.site.register(SATBank)