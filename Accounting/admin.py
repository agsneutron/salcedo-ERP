# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Accounting.models import *

admin.site.register(GroupingCode)
admin.site.register(Account)