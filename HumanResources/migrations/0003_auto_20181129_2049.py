# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-29 20:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [

    ]

    operations = [
        migrations.AlterField(
            model_name='employeedropout',
            name='date',
            field=models.DateField(verbose_name='Fecha de Baja*'),
        ),
        migrations.AlterField(
            model_name='employeedropout',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HumanResources.Employee', verbose_name='Empleado*'),
        ),
        migrations.AlterField(
            model_name='employeedropout',
            name='observations',
            field=tinymce.models.HTMLField(blank=True, max_length=4096, null=True, validators=[django.core.validators.RegexValidator(message='\xc9ste campo no acepta caracateres como: +*/{] .', regex="[a-zA-Z\xe0\xe1\xe2\xe4\xe3\xe5\u0105\u010d\u0107\u0119\xe8\xe9\xea\xeb\u0117\u012f\xec\xed\xee\xef\u0142\u0144\xf2\xf3\xf4\xf6\xf5\xf8\xf9\xfa\xfb\xfc\u0173\u016b\xff\xfd\u017c\u017a\xf1\xe7\u010d\u0161\u017e\xc0\xc1\xc2\xc4\xc3\xc5\u0104\u0106\u010c\u0116\u0118\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\u012e\u0141\u0143\xd2\xd3\xd4\xd6\xd5\xd8\xd9\xda\xdb\xdc\u0172\u016a\u0178\xdd\u017b\u0179\xd1\xdf\xc7\u0152\xc6\u010c\u0160\u017d\u2202\xf0 ,.'-]")], verbose_name='Observaciones'),
        ),
        migrations.AlterField(
            model_name='employeedropout',
            name='reason',
            field=models.CharField(blank=True, max_length=4096, null=True, validators=[django.core.validators.RegexValidator(message='\xc9ste campo no acepta caracateres como: +*/{] .', regex="[a-zA-Z\xe0\xe1\xe2\xe4\xe3\xe5\u0105\u010d\u0107\u0119\xe8\xe9\xea\xeb\u0117\u012f\xec\xed\xee\xef\u0142\u0144\xf2\xf3\xf4\xf6\xf5\xf8\xf9\xfa\xfb\xfc\u0173\u016b\xff\xfd\u017c\u017a\xf1\xe7\u010d\u0161\u017e\xc0\xc1\xc2\xc4\xc3\xc5\u0104\u0106\u010c\u0116\u0118\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\u012e\u0141\u0143\xd2\xd3\xd4\xd6\xd5\xd8\xd9\xda\xdb\xdc\u0172\u016a\u0178\xdd\u017b\u0179\xd1\xdf\xc7\u0152\xc6\u010c\u0160\u017d\u2202\xf0 ,.'-]")], verbose_name='Motivo'),
        ),
        migrations.AlterField(
            model_name='employeedropout',
            name='severance_pay',
            field=models.FloatField(null=True, validators=[django.core.validators.RegexValidator(message='Este campo solo acepta n\xfameros.', regex='[0-9]')], verbose_name='Liquidaci\xf3n*'),
        ),
        migrations.AlterField(
            model_name='employeedropout',
            name='type',
            field=models.IntegerField(choices=[(1, 'Termino de Contrato'), (2, 'Separaci\xf3n Voluntaria'), (3, 'Abandono del Empleo'), (4, 'Defunci\xf3n'), (5, 'Ausentismo'), (6, 'Rescisi\xf3n de Contrato'), (7, 'Pensionado'), (8, 'Otra')], default=1, verbose_name='Motivo de Baja*'),
        ),
        migrations.AlterField(
            model_name='payrollgroup',
            name='checker_type',
            field=models.IntegerField(choices=[(1, 'Autom\xe1tico'), (2, 'Manual')], default=1, verbose_name='Tipo de Checador*'),
        ),
        migrations.AlterField(
            model_name='payrollgroup',
            name='direction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='HumanResources.Direction', verbose_name='Direcci\xf3n*'),
        ),
        migrations.AlterField(
            model_name='payrollgroup',
            name='internal_company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SharedCatalogs.InternalCompany', verbose_name='Empresa*'),
        ),
        migrations.AlterField(
            model_name='payrollgroup',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='\xc9ste campo no acepta caracateres como: +*/{] .', regex="[a-zA-Z\xe0\xe1\xe2\xe4\xe3\xe5\u0105\u010d\u0107\u0119\xe8\xe9\xea\xeb\u0117\u012f\xec\xed\xee\xef\u0142\u0144\xf2\xf3\xf4\xf6\xf5\xf8\xf9\xfa\xfb\xfc\u0173\u016b\xff\xfd\u017c\u017a\xf1\xe7\u010d\u0161\u017e\xc0\xc1\xc2\xc4\xc3\xc5\u0104\u0106\u010c\u0116\u0118\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\u012e\u0141\u0143\xd2\xd3\xd4\xd6\xd5\xd8\xd9\xda\xdb\xdc\u0172\u016a\u0178\xdd\u017b\u0179\xd1\xdf\xc7\u0152\xc6\u010c\u0160\u017d\u2202\xf0 ,.'-]")], verbose_name='Nombre*'),
        ),
        migrations.AlterField(
            model_name='payrollgroup',
            name='payroll_classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HumanResources.PayrollClassification', verbose_name='Clasificaci\xf3n de N\xf3mina*'),
        ),
        migrations.AlterField(
            model_name='payrolltype',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='\xc9ste campo no acepta caracateres como: +*/{] .', regex="[a-zA-Z\xe0\xe1\xe2\xe4\xe3\xe5\u0105\u010d\u0107\u0119\xe8\xe9\xea\xeb\u0117\u012f\xec\xed\xee\xef\u0142\u0144\xf2\xf3\xf4\xf6\xf5\xf8\xf9\xfa\xfb\xfc\u0173\u016b\xff\xfd\u017c\u017a\xf1\xe7\u010d\u0161\u017e\xc0\xc1\xc2\xc4\xc3\xc5\u0104\u0106\u010c\u0116\u0118\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\u012e\u0141\u0143\xd2\xd3\xd4\xd6\xd5\xd8\xd9\xda\xdb\xdc\u0172\u016a\u0178\xdd\u017b\u0179\xd1\xdf\xc7\u0152\xc6\u010c\u0160\u017d\u2202\xf0 ,.'-]")], verbose_name='Nombre*'),
        ),
    ]