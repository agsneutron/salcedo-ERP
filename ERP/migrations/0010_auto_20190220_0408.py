# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-20 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0009_auto_20190220_0339'),
    ]

    operations = [

        migrations.AlterField(
            model_name='contratocontratista',
            name='fecha_termino_propuesta',
            field=models.DateField(default='2019-01-01', verbose_name='Fecha de Termino Propuesta'),
            preserve_default=False,
        ),
    ]
