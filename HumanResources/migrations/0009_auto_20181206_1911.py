# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-06 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

   dependencies = [

   ]

   operations = [
       migrations.AlterField(
           model_name='employeeloandetail',
           name='pay_status',
           field=models.BooleanField(default=False, verbose_name='Estatus de Pago'),
       ),
   ]