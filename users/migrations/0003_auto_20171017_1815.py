# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-17 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171017_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erpuser',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to=users.models.profile_picture_document_destination, verbose_name='Foto de Perfil'),
        ),
    ]