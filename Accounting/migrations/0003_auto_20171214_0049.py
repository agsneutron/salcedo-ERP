# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-12-14 00:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0011_bank_sat_bank'),
        ('Accounting', '0002_commercialally'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialAllyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('rfc', models.CharField(max_length=20, verbose_name='RFC')),
                ('street', models.CharField(max_length=255, verbose_name='Calle')),
                ('outdoor_number', models.CharField(max_length=10, verbose_name='No. Exterior')),
                ('indoor_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='No. Interior')),
                ('colony', models.CharField(max_length=255, verbose_name='Colonia')),
                ('zip_code', models.CharField(max_length=5, verbose_name='C\xf3digo Postal')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Tel\xe9fono Principal')),
                ('secondary_number', models.CharField(blank=True, max_length=20, verbose_name='Tel\xe9fono Secundario')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('is_legal_representative', models.BooleanField(default=False, verbose_name='Es Representante Legal')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.Pais', verbose_name='Pa\xeds')),
                ('state', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='pais', on_delete=django.db.models.deletion.CASCADE, to='ERP.Estado', verbose_name='Estado')),
                ('town', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='state', chained_model_field='estado', on_delete=django.db.models.deletion.CASCADE, to='ERP.Municipio', verbose_name='Municipio')),
            ],
            options={
                'verbose_name_plural': 'Contactos',
            },
        ),
        migrations.AlterField(
            model_name='commercialally',
            name='type',
            field=models.IntegerField(choices=[(0, 'Proveedor'), (1, 'Acreedor'), (2, 'Tercero')], default=0, verbose_name='Tipo'),
        ),
    ]
