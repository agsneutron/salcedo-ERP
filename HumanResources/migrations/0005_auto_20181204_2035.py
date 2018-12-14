# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-04 20:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0004_merge_20181204_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefinancialdata',
            name='CLABE',
            field=models.CharField(default=0, max_length=40, validators=[django.core.validators.RegexValidator(message='Este campo solo acepta n\xfameros.', regex='[0-9]')], verbose_name='Clave Interbancaria (CLABE)*'),
        ),
        migrations.AlterField(
            model_name='employeefinancialdata',
            name='account_number',
            field=models.CharField(default=0, max_length=20, validators=[django.core.validators.RegexValidator(message='Este campo solo acepta n\xfameros.', regex='[0-9]')], verbose_name='N\xfamero de Cuenta*'),
        ),
        migrations.AlterField(
            model_name='employeefinancialdata',
            name='payment_method',
            field=models.CharField(choices=[('D', 'Deposito'), ('E', 'Efectivo'), ('T', 'Transferencia Interbancaria')], default='D', max_length=1, verbose_name='Forma de Pago*'),
        ),
        migrations.AlterField(
            model_name='infonavitdata',
            name='credit_term',
            field=models.CharField(max_length=200, verbose_name='Duraci\xf3n de Cr\xe9dito*'),
        ),
        migrations.AlterField(
            model_name='infonavitdata',
            name='discount_amount',
            field=models.CharField(max_length=30, verbose_name='Monto de Descuento*'),
        ),
        migrations.AlterField(
            model_name='infonavitdata',
            name='discount_type',
            field=models.CharField(max_length=30, verbose_name='Tipo de Descuento*'),
        ),
        migrations.AlterField(
            model_name='infonavitdata',
            name='start_date',
            field=models.DateField(verbose_name='Fecha de Inicio*'),
        ),
    ]