# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-04 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0003_remove_employeeloandetail_deduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeloandetail',
            name='deduction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HumanResources.EmployeeEarningsDeductionsbyPeriod', verbose_name='Deduction'),
        ),
    ]