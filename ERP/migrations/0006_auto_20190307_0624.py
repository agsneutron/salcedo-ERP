# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-07 06:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0005_auto_20190307_0513'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='distribucionpago',
            unique_together=set([('contrato', 'line_item')]),
        ),
    ]
