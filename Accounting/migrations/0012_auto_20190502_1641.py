# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-02 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0011_auto_20190412_0223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Registro de Gastos', 'verbose_name_plural': 'Registros de Gastos'},
        ),
        migrations.AlterField(
            model_name='expense',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=50, verbose_name='Monto L\xedquido'),
        ),
        migrations.AlterField(
            model_name='expensedetail',
            name='deliveryto',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Entregado a'),
        ),
    ]
