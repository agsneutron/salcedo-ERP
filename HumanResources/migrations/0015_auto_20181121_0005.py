# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-21 00:05
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('SharedCatalogs', '0003_auto_20181120_2028'),
        ('HumanResources', '0014_payrollgroup_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='colony',
            field=models.CharField(default=1, max_length=255, verbose_name='Colonia*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SharedCatalogs.Pais', verbose_name='Pa\xeds*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='indoor_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='No. Interior'),
        ),
        migrations.AddField(
            model_name='direction',
            name='outdoor_number',
            field=models.CharField(default=1, max_length=10, verbose_name='No. Exterior*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='rfc',
            field=models.CharField(default=1, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='El RFC que proporcionas es incorrecto.', regex='^([A-Z\xd1&]{3,4}) ?(?:- ?)?(\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\\d|3[01])) ?(?:- ?)?([A-Z\\d]{2})([A\\d])$')], verbose_name='RFC de la Empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='pais', default=1, on_delete=django.db.models.deletion.CASCADE, to='SharedCatalogs.Estado', verbose_name='Estado*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='street',
            field=models.CharField(default=1, max_length=255, verbose_name='Calle*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='town',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='state', chained_model_field='estado', default=33, on_delete=django.db.models.deletion.CASCADE, to='SharedCatalogs.Municipio', verbose_name='Municipio*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='direction',
            name='zip_code',
            field=models.CharField(default=1, max_length=5, validators=[django.core.validators.RegexValidator(message='Este campo solo acepta n\xfameros.', regex='[0-9]')], verbose_name='C\xf3digo Postal*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payrollgroup',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='HumanResources.Direction', verbose_name='Empresa'),
        ),
    ]
