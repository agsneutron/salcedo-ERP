# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-13 02:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0013_auto_20190313_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimate',
            name='contract',
        ),

    ]