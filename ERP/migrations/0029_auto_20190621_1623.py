# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-21 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0028_auto_20190620_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressestimate',
            name='amount',
            field=models.DecimalField(decimal_places=9, default=0, max_digits=20, verbose_name='Monto ($)'),
        ),
        migrations.AlterField(
            model_name='progressestimate',
            name='generator_amount',
            field=models.DecimalField(decimal_places=9, default=0, max_digits=20, verbose_name='Cantidad del Generador'),
        ),
        migrations.AlterField(
            model_name='progressestimate',
            name='paid_out',
            field=models.DecimalField(decimal_places=9, default=0.0, max_digits=20, verbose_name='Pagado'),
        ),
    ]
