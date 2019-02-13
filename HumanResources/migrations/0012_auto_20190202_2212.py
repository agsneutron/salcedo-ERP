# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-02 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0011_auto_20190202_0547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infonavitdata',
            name='employee',
        ),
        migrations.AlterField(
            model_name='employeepositiondescription',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HumanResources.Employee', verbose_name='Empleado'),
        ),
    ]
