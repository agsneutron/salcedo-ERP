# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-06 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0006_auto_20181205_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeloandetail',
            name='pay_number',
            field=models.IntegerField(default=1, verbose_name='N\xfamero de Pago'),
        ),
    ]
