# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-20 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharedCatalogs', '0002_auto_20180209_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupingcode',
            name='level',
            field=models.IntegerField(default=0, null=True, verbose_name='Nivel'),
        ),
    ]
