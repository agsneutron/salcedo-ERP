# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-04-11 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0006_auto_20190411_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typedocument',
            name='description',
            field=models.CharField(blank=True, default=False, max_length=256, verbose_name='Descripci\xf3n'),
        ),
    ]