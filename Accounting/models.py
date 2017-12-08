# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Model for grouping code for accounts
class GroupingCode(models.Model):
    level = models.IntegerField(verbose_name="Nivel", )
    grouping_code = models.DecimalField(verbose_name="Código Agrupador", max_digits=20, decimal_places=2,)
    account_name = models.CharField(verbose_name="Nombre de la Cuenta y/o subcuenta", max_length=500,)