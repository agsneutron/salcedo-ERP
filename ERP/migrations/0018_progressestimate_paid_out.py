# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-15 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0017_remove_progressestimate_paid_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressestimate',
            name='paid_out',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Pagado'),
        ),
    ]
