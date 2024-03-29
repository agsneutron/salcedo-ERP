# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-04-11 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0005_auto_20190404_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Tipo de Documento')),
                ('description', models.BooleanField(default=False, verbose_name='Descripci\xf3n')),
            ],
            options={
                'verbose_name': 'Tipo de Documento',
                'verbose_name_plural': 'Tipos de Documento',
            },
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Registro de Gastos', 'verbose_name_plural': 'Registro de Gastos'},
        ),
        migrations.AddField(
            model_name='expense',
            name='total_ammount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True, verbose_name='Valor Total'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='monto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True, verbose_name='Monto Liquido'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='reference',
            field=models.CharField(max_length=1024, verbose_name='Documento'),
        ),
    ]
