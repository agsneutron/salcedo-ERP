# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-12-13 02:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0002_bank_sat_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='sat_bank',
        ),
    ]
