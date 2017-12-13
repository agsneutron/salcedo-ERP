# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Accounting.models import *
from Accounting.forms import *


@admin.register(AccountingPolicy)
class AccountingPolicyAdmin(admin.ModelAdmin):
    form = AccountingPolicyForm



admin.site.register(GroupingCode)
admin.site.register(Account)
admin.site.register(Provider)
admin.site.register(AccountingPolicy)


