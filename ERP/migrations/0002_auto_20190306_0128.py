# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-06 01:28
from __future__ import unicode_literals

import ERP.models
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistribucionPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias_pactados', models.CharField(max_length=20, verbose_name='D\xedas Pactados')),
            ],
            options={
                'verbose_name': 'Distribuci\xf3n de Pago',
                'verbose_name_plural': 'Distribuci\xf3n de Pagos',
            },
        ),
        migrations.CreateModel(
            name='DistribucionPagoDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(verbose_name='Fecha de Pago')),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Porcentaje')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='Monto')),
                ('distribucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.DistribucionPago', verbose_name='Distribuci\xf3n del Pago')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentacionContrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_archivo', models.CharField(blank=True, max_length=50, verbose_name='Descripci\xf3n del Archivo ')),
                ('pdf_version', models.FileField(upload_to=ERP.models.upload_contract_file, verbose_name='Archivo')),
            ],
            options={
                'verbose_name': 'Documento de Contrato',
                'verbose_name_plural': 'Documentos de Contrato',
            },
        ),
        migrations.CreateModel(
            name='PartidasContratoContratista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_partida', models.CharField(blank=True, max_length=50, verbose_name='Monto de la Partida')),
                ('anticipo', models.DecimalField(blank=True, decimal_places=2, max_digits=50, verbose_name='Anticipo %')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_termino_propuesta', models.DateField(verbose_name='Fecha de Termino Propuesta')),
                ('fecha_termino_real', models.DateField(blank=True, null=True, verbose_name='Fecha de Termino Real')),
                ('observaciones', models.TextField(blank=True, max_length=500, verbose_name='Observaciones')),
            ],
            options={
                'verbose_name': 'Partida del Contrato',
                'verbose_name_plural': 'Partidas del Contrato',
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(max_length=200, verbose_name='Tipo de Pago')),
                ('descripcion', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripci\xf3n')),
            ],
        ),
        migrations.AlterModelOptions(
            name='contractconcepts',
            options={'verbose_name_plural': 'Conceptos del Contrato'},
        ),
        migrations.RemoveField(
            model_name='contratocontratista',
            name='dias_pactados',
        ),
        migrations.RemoveField(
            model_name='contratocontratista',
            name='fecha_termino',
        ),
        migrations.AddField(
            model_name='contractconcepts',
            name='OfThisEstimate',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12, verbose_name='De Esta Estimaci\xf3n'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contractconcepts',
            name='ThisEstimate',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12, verbose_name='A Esta Estimaci\xf3n'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contratocontratista',
            name='fecha_termino_propuesta',
            field=models.DateField(default='2019-01-01', verbose_name='Fecha de Termino Propuesta'),
        ),
        migrations.AddField(
            model_name='contratocontratista',
            name='fecha_termino_real',
            field=models.DateField(null=True, verbose_name='Fecha de Termino Real'),
        ),
        migrations.AddField(
            model_name='estimate',
            name='Total_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, max_length=2, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))], verbose_name='Total Pagado'),
        ),
        migrations.AddField(
            model_name='partidascontratocontratista',
            name='contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.ContratoContratista', verbose_name='Contrato'),
        ),
        migrations.AddField(
            model_name='partidascontratocontratista',
            name='line_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.LineItem', verbose_name='Partida'),
        ),
        migrations.AddField(
            model_name='documentacioncontrato',
            name='contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.ContratoContratista', verbose_name='Contrato'),
        ),
        migrations.AddField(
            model_name='distribucionpagodetail',
            name='tipo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.TipoPago', verbose_name='Tipo de Pago'),
        ),
        migrations.AddField(
            model_name='distribucionpago',
            name='contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.ContratoContratista', verbose_name='Contrato'),
        ),
        migrations.AddField(
            model_name='distribucionpago',
            name='line_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.LineItem', verbose_name='Partida'),
        ),
    ]
