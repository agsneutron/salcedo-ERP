# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-13 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0014_auto_20190313_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='contractlineitem',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='ERP.PartidasContratoContratista', verbose_name='Contrato - Partida'),
            preserve_default=False,
        ),
    ]