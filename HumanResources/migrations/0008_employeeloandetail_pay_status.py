# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-06 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0007_employeeloandetail_pay_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeloandetail',
            name='pay_status',
            field=models.BinaryField(default=0, verbose_name='Estatus de Pago'),
        ),
    ]