# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Libraries.
from tinymce import models as tinymce_models

from django.contrib.auth.models import User

from django.core.checks import messages
from django.db import models
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from Logs.controller import Logs
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

# Third Party Libraries
from smart_selects.db_fields import ChainedForeignKey

# Importing model from other apps.
from ERP.models import Pais, Estado, Municipio, Project, Bank
from SharedCatalogs.models import Account
from utilities import getParameters

# Create your models here.
from multiselectfield import MultiSelectField
from django.forms.models import model_to_dict
from django.db.models import Sum


# To represent ISRTable.
class ISRTable(models.Model):
    lower_limit = models.FloatField(verbose_name="Límite Inferior", null=False, blank=False, default=0)
    upper_limit = models.FloatField(verbose_name="Límite Superior", null=False, blank=False, default=0)
    fixed_fee = models.FloatField(verbose_name="Cuota Fija", null=False, blank=False, default=0)
    rate = models.FloatField(verbose_name="Tasa Aplicable", null=False, blank=False, default=0)

    class Meta:
        verbose_name_plural = "Tabla de ISR"
        verbose_name = "Tabla de ISR"

    def __str__(self):
        return self.lower_limit

    def __unicode__(self):  # __unicode__ on Python 2
        return self.lower_limit


class PayrollClassification(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=100, null=False, blank=False, unique=False, default='')

    class Meta:
        verbose_name_plural = "Clasificación de Nómina"
        verbose_name = "Clasificación de Nómina"

    def __str__(self):
        return str(self.name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.name)


class PayrollGroup(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200, null=False, blank=False, unique=False)
    payroll_classification = models.ForeignKey(PayrollClassification, verbose_name="Clasificación de Nómina",
                                               null=False, blank=False)

    CHECKER_TYPE_AUTOMATIC = 1
    CHECKER_TYPE_MANUAL = 2
    CHECKER_TYPE_CHOICES = (
        (CHECKER_TYPE_AUTOMATIC, 'Automático'),
        (CHECKER_TYPE_MANUAL, 'Manual')
    )
    checker_type = models.IntegerField(choices=CHECKER_TYPE_CHOICES, default=CHECKER_TYPE_AUTOMATIC,
                                       verbose_name='Tipo de Checador')

    project = models.ForeignKey(Project, verbose_name="Proyecto", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Grupo de Nómina"
        verbose_name = "Grupo de Nómina"

    def __str__(self):
        return str(self.name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.name)

        # Method to save the employee document file.


def upload_employee_photo(instance, filename):
    return '/'.join(['human_resources', 'employee_documents', instance.employee_key, filename])


# Employee General Information.
class Employee(models.Model):
    employee_key = models.CharField(verbose_name="Clave", max_length=64, null=False, blank=False, unique=False)
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno", max_length=255, null=False, blank=False)

    photo = models.FileField(upload_to=upload_employee_photo, null=True, blank=True, verbose_name="Foto")

    TYPE_A = 1
    TYPE_B = 2
    EMPLOYEE_TYPE_CHOICES = (
        (TYPE_A, 'Empleado Tipo A'),
        (TYPE_B, 'Empleado Tipo B'),
    )
    type = models.IntegerField(choices=EMPLOYEE_TYPE_CHOICES, default=TYPE_A, verbose_name='Tipo de Empleado')
    registry_date = models.DateField(default=now, null=False, blank=False, verbose_name="Fecha de Registro")

    STATUS_ACTIVE = 1
    STATUS_INNACTIVE = 2
    EMPLOYEE_STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_INNACTIVE, 'Inactivo'),
    )

    status = models.IntegerField(choices=EMPLOYEE_STATUS_CHOICES, default=STATUS_ACTIVE,
                                 verbose_name='Estatus del Empleado')
    birthdate = models.DateField(null=False, blank=False, verbose_name="Fecha de Nacimiento")
    birthplace = models.CharField(null=False, blank=False, verbose_name="Lugar de Nacimiento", max_length=255)

    GENDER_A = 1
    GENDER_B = 2
    EMPLOYEE_GENDER_CHOICES = (
        (GENDER_A, 'Femenino'),
        (GENDER_B, 'Masculino'),
    )
    gender = models.IntegerField(choices=EMPLOYEE_GENDER_CHOICES, default=GENDER_A, verbose_name='Género')

    MARITAL_STATUS_A = 1
    MARITAL_STATUS_B = 2
    EMPLOYEE_MARITAL_STATUS_CHOICES = (
        (MARITAL_STATUS_A, 'Soltero'),
        (MARITAL_STATUS_B, 'Casado'),
    )
    marital_status = models.IntegerField(choices=EMPLOYEE_MARITAL_STATUS_CHOICES, default=MARITAL_STATUS_A,
                                         verbose_name='Estado Civil')
    curp = models.CharField(verbose_name="CURP", max_length=18, null=False, blank=False, unique=True)
    rfc = models.CharField(verbose_name="RFC", max_length=13, null=False, blank=False, unique=True)
    phone_number = models.CharField(verbose_name="Teléfono", max_length=20, null=False, blank=False)
    cellphone_number = models.CharField(verbose_name="Celular", max_length=20, null=False, blank=True)
    office_number = models.CharField(verbose_name="Teléfono de Oficina", max_length=20, null=False, blank=True)
    extension_number = models.CharField(verbose_name="Número de Extensión", max_length=10, null=False, blank=True)
    personal_email = models.CharField(verbose_name="Correo Electrónico Personal", max_length=255, null=True,
                                      blank=False)
    work_email = models.CharField(verbose_name="Correo Electrónico Laboral", max_length=255, null=False, blank=False)

    social_security_number = models.CharField(verbose_name="Número de Póliza de Seguro", max_length=20, null=False,
                                              blank=False)
    social_security_type = models.CharField(verbose_name="Tipo de Seguro", null=True, blank=False, max_length=100)

    colony = models.CharField(verbose_name="Colonia", max_length=255, null=False, blank=False)
    street = models.CharField(verbose_name="Calle", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    zip_code = models.CharField(verbose_name="Código Postal", max_length=5, null=False, blank=False)

    BLOOD_TYPE_AP = 1
    BLOOD_TYPE_AM = 2
    BLOOD_TYPE_BP = 3
    BLOOD_TYPE_BM = 4
    BLOOD_TYPE_OP = 5
    BLOOD_TYPE_OM = 6
    BLOOD_TYPE_ABP = 7
    BLOOD_TYPE_ABM = 8

    BLOOD_TYPE_CHOICES = (
        (BLOOD_TYPE_AP, 'A+'),
        (BLOOD_TYPE_AM, 'A-'),
        (BLOOD_TYPE_BP, 'B+'),
        (BLOOD_TYPE_BM, 'B-'),
        (BLOOD_TYPE_OP, 'O+'),
        (BLOOD_TYPE_OM, 'O-'),
        (BLOOD_TYPE_ABP, 'AB+'),
        (BLOOD_TYPE_ABM, 'AB-'),
    )
    blood_type = models.IntegerField(choices=BLOOD_TYPE_CHOICES, default=BLOOD_TYPE_AP, verbose_name='Tipo Sanguíneo')
    driving_license_number = models.CharField(verbose_name="Número de Licencia de Conducir", max_length=20, null=False,
                                              blank=True)
    driving_license_expiry_date = models.DateField(null=False, blank=True,
                                                   verbose_name="Expiración de Licencia para Conducir")

    # Foreign Keys.

    # Attribute for the Chained Keys.
    country = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    state = ChainedForeignKey(Estado,
                              chained_field="country",
                              chained_model_field="pais",
                              show_all=False,
                              auto_choose=True,
                              sort=True,
                              verbose_name="Estado")
    town = ChainedForeignKey(Municipio,
                             chained_field="state",
                             chained_model_field="estado",
                             show_all=False,
                             auto_choose=True,
                             sort=True,
                             verbose_name="Municipio")
    tax_regime = models.ForeignKey('TaxRegime', verbose_name="Régimen Fiscal", null=False, blank=False)

    # Many to Many Foreign Keys.
    tags = models.ManyToManyField("Tag", verbose_name="Etiquetas", through="EmployeeHasTag")
    tests = models.ManyToManyField("Test", verbose_name="Pruebas", through="TestApplication")

    def get_full_name(self):
        return self.name + " " + self.first_last_name + " " + self.second_last_name


    def __str__(self):
        return self.employee_key + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee_key + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name

    def to_serializable_dict(self):
        dict = model_to_dict(self)
        dict['birthdate'] = str(self.birthdate)
        dict['driving_license_expiry_date'] = str(self.driving_license_expiry_date)

        return dict

    class Meta:
        verbose_name_plural = 'Empleados'
        verbose_name = 'Empleado'

    # To get all the fixed earnings for an employee.
    def get_fixed_earnings(self):
        employee_earnings = EmployeeEarningsDeductions.objects.filter(Q(employee__id=self.id) &
                                                                      Q(concept__type=EarningsDeductions.PERCEPCION) &
                                                                      Q(concept__status=EarningsDeductions.ACTIVA))

        return employee_earnings

    # To get all the variable earnings for an employee in a specific period.
    def get_variable_earnings_for_period(self, payroll_period=None):
        employee_earnings_by_period = EmployeeEarningsDeductionsbyPeriod.objects.filter(Q(employee__id=self.id) &
                                                                                        Q(
                                                                                            payroll_period__id=payroll_period.id) &
                                                                                        Q(
                                                                                            concept__type=EarningsDeductions.PERCEPCION) &
                                                                                        Q(
                                                                                            concept__status=EarningsDeductions.ACTIVA))
        return employee_earnings_by_period

    # To get all the fixed deductions for an employee.
    def get_fixed_deductions(self):
        employee_deductions = EmployeeEarningsDeductions.objects.filter(Q(employee__id=self.id) &
                                                                        Q(concept__type=EarningsDeductions.DEDUCCION) &
                                                                        Q(concept__status=EarningsDeductions.ACTIVA))

        return employee_deductions

    # To get all the variable deductions for an employee in a specific period.
    def get_variable_deductions_for_period(self, payroll_period=None):
        employee_deductions_by_period = EmployeeEarningsDeductionsbyPeriod.objects.filter(Q(employee__id=self.id) &
                                                                                          Q(
                                                                                              payroll_period__id=payroll_period.id) &
                                                                                          Q(
                                                                                              concept__type=EarningsDeductions.DEDUCCION) &
                                                                                          Q(
                                                                                              concept__status=EarningsDeductions.ACTIVA))
        return employee_deductions_by_period

    # To get all the absences for an employee in a specific period.
    def get_employee_absences_for_period(self, payroll_period=None):
        absences = EmployeeAssistance.objects.filter(Q(employee__id=self.id) &
                                                     Q(payroll_period__id=payroll_period.id) &
                                                     Q(absence=True))

        return absences

    # To get all the absences for an employee that haven't been justified in a specific period.
    def get_unjustified_employee_absences_for_period(self, payroll_period=None):
        absences = EmployeeAssistance.objects.filter(Q(employee__id=self.id) &
                                                     Q(payroll_period__id=payroll_period.id) &
                                                     Q(absence=True) &
                                                     Q(justified=False))

        return absences




# Method to save the employee document file.
def upload_employee_contract(instance, filename):
    return '/'.join(['human_resources', 'employee_documents', instance.employee.employee_key, 'contracts', filename])


class EmployeeContract(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)

    contract_key = models.CharField(verbose_name="Clave del Contrato", max_length=64, null=False, blank=False, unique=True)


    CONTRACT_TYPE_PERMANENT = 'P'
    CONTRACT_TYPE_TEMPORAL = 'T'

    CONTRACT_TYPE_CHOICES = (
        (CONTRACT_TYPE_PERMANENT, 'Permanente'),
        (CONTRACT_TYPE_TEMPORAL, 'Temporal'),
    )

    contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPE_CHOICES, default=CONTRACT_TYPE_PERMANENT,
                                      verbose_name='Tipo de Contrato')


    description = tinymce_models.HTMLField(verbose_name='Descripción', null=True, blank=True, max_length=4096)

    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    end_date = models.DateField(verbose_name="Fecha de Término", null=True, blank=True)


    contract_file = models.FileField(upload_to=upload_employee_contract, null=True, verbose_name="Contrato Escaneado")


    def __str__(self):
        return self.contract_key+ ": " + self.employee.name+ " " + self.employee.first_last_name + " " + self.employee.second_last_name


    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

# Employee Checker Data.
class CheckerData(models.Model):
    CHECKER_TYPE_A = 1
    CHECKER_TYPE_B = 2
    CHECKER_TYPE_C = 3
    CHECKER_TYPE_CHOICES = (
        (CHECKER_TYPE_A, 'Automático'),
        (CHECKER_TYPE_B, 'Manual'),
        (CHECKER_TYPE_C, 'Sin Checador'),
    )

    checks_entry = models.BooleanField(verbose_name="Checa Entrada", default=True)
    checks_exit = models.BooleanField(verbose_name="Checa Salida", default=True)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Datos de Checador del Empleado'
        verbose_name = 'Datos de Checador del Empleado'


# Tax Regimes.
class TaxRegime(models.Model):
    name = models.CharField(verbose_name="Régimen Fiscal", max_length=255, null=False, blank=False, unique=False)

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = 'Regímenes Fiscales'
        verbose_name = 'Régimen Fiscal'


# Method to save the employee document file.
def upload_employee_document(instance, filename):
    return '/'.join(['human_resources', 'employee_documents', instance.employee.employee_key, filename])


# Employee Documents.
class EmployeeDocument(models.Model):
    file = models.FileField(upload_to=upload_employee_document, null=True, verbose_name="Archivo")
    comments = models.CharField(verbose_name="Comentarios", max_length=2048, null=False, blank=False, unique=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    document_type = models.ForeignKey('DocumentType', verbose_name='Tipo de Documento', null=False, blank=False)

    def __str__(self):
        return self.file.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.file.name

    class Meta:
        verbose_name_plural = 'Documentos Probatorios'
        verbose_name = 'Documento Probatorio'


# Employee Document Type.
class DocumentType(models.Model):
    name = models.CharField(verbose_name="Tipo de Documento", max_length=255, null=False, blank=False, unique=False)

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = 'Tipos de Documento'
        verbose_name = 'Tipo de Documento'


# Tags to describe the Employee.
class Tag(models.Model):
    name = models.CharField(verbose_name="Nombre de la Etiqueta", max_length=64, null=False, blank=False, unique=False)

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = 'Etiquetas'
        verbose_name = 'Etiqueta'


# Assigned Tags to an Employee.
class EmployeeHasTag(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    tag = models.ForeignKey(Tag, verbose_name="Etiqueta", null=False, blank=False)

    class Meta:
        unique_together = ('employee', 'tag')
        verbose_name = "Etiquetas del Empleado"
        verbose_name_plural = "Etiquetas del Empleado"

    def __str__(self):
        return self.tag.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.tag.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name


# Current Education of the Employee.
class CurrentEducation(models.Model):
    EDUCATION_TYPE_A = 1
    EDUCATION_TYPE_B = 2
    EDUCATION_TYPE_C = 3
    EDUCATION_TYPE_D = 4
    EDUCATION_TYPE_E = 5
    EDUCATION_TYPE_F = 6
    EDUCATION_TYPE_G = 7
    EDUCATION_TYPE_H = 8
    EDUCATION_TYPE_I = 9
    EDUCATION_TYPE_J = 10
    EDUCATION_TYPE_K = 11
    EDUCATION_TYPE_L = 12
    EDUCATION_TYPE_CHOICES = (
        (EDUCATION_TYPE_A, 'Sin Estudios'),
        (EDUCATION_TYPE_B, 'Primaria'),
        (EDUCATION_TYPE_C, 'Secundaria'),
        (EDUCATION_TYPE_D, 'Preparatoria'),
        (EDUCATION_TYPE_E, 'Técnico'),
        (EDUCATION_TYPE_F, 'Certificación'),
        (EDUCATION_TYPE_G, 'Licenciatura (Trunca)'),
        (EDUCATION_TYPE_H, 'Licenciatura (Sin Título)'),
        (EDUCATION_TYPE_I, 'Licenciatura (Título)'),
        (EDUCATION_TYPE_J, 'Especialidad'),
        (EDUCATION_TYPE_K, 'Maestría'),
        (EDUCATION_TYPE_L, 'Doctorado')
    )
    type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES, default=EDUCATION_TYPE_A,
                               verbose_name='Tipo de Educación')
    name = models.CharField(verbose_name="Nombre", max_length=2048, null=False, blank=False)
    institution = models.CharField(verbose_name="Institución", max_length=1024, null=False, blank=False)
    sunday = models.BooleanField(verbose_name="Domingo", default=False)
    monday = models.BooleanField(verbose_name="Lunes", default=False)
    tuesday = models.BooleanField(verbose_name="Martes", default=False)
    wednesday = models.BooleanField(verbose_name="Miércoles", default=False)
    thursday = models.BooleanField(verbose_name="Jueves", default=False)
    friday = models.BooleanField(verbose_name="Viernes", default=False)
    saturday = models.BooleanField(verbose_name="Sábado", default=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name = "Formación Académica Actual del Empleado"
        verbose_name_plural = "Formación Académica Actual del Empleado"

    def __str__(self):
        return self.get_type_display() + ": " + self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.get_type_display() + ": " + self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name


# Method to save the employee's current education file.
def upload_employee_current_education_document(instance, filename):
    return '/'.join(
        ['human_resources', 'employee_documents', 'current_education', instance.current_education.employee.employee_key,
         filename])


# Employee Current Education Documents.
class CurrentEducationDocument(models.Model):
    file = models.FileField(upload_to=upload_employee_current_education_document, null=True, verbose_name="Archivo",
                            blank=True)
    comments = models.CharField(verbose_name="Comentarios", max_length=2048, null=True, blank=True, unique=False)

    # Foreign Keys.
    current_education = models.ForeignKey(CurrentEducation, verbose_name='Formación Actual del Empleado', null=False,
                                          blank=False)

    def __str__(self):
        return self.file.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.file.name

    class Meta:
        verbose_name_plural = 'Documentos de la Formación Actual del Empleado'
        verbose_name = 'Documento de la Formación Actual del Empleado'


# Method to save the employee's current education file.
def upload_employee_education_document(instance, filename):
    return '/'.join(['human_resources', 'employee_documents', 'education', instance.employee.employee_key, filename])


# Employee Education Records.
class Education(models.Model):
    EDUCATION_TYPE_A = 1
    EDUCATION_TYPE_B = 2
    EDUCATION_TYPE_C = 3
    EDUCATION_TYPE_D = 4
    EDUCATION_TYPE_E = 5
    EDUCATION_TYPE_F = 6
    EDUCATION_TYPE_G = 7
    EDUCATION_TYPE_H = 8
    EDUCATION_TYPE_I = 9
    EDUCATION_TYPE_J = 10
    EDUCATION_TYPE_K = 11
    EDUCATION_TYPE_L = 12
    EDUCATION_TYPE_CHOICES = (
        (EDUCATION_TYPE_A, 'Sin Estudios'),
        (EDUCATION_TYPE_B, 'Primaria'),
        (EDUCATION_TYPE_C, 'Secundaria'),
        (EDUCATION_TYPE_D, 'Preparatoria'),
        (EDUCATION_TYPE_E, 'Técnico'),
        (EDUCATION_TYPE_F, 'Certificación'),
        (EDUCATION_TYPE_G, 'Licenciatura (Trunca)'),
        (EDUCATION_TYPE_H, 'Licenciatura (Sin Título)'),
        (EDUCATION_TYPE_I, 'Licenciatura (Título)'),
        (EDUCATION_TYPE_J, 'Especialidad'),
        (EDUCATION_TYPE_K, 'Maestría'),
        (EDUCATION_TYPE_L, 'Doctorado')
    )
    type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES, default=EDUCATION_TYPE_A,
                               verbose_name='Tipo de Educación')
    name = models.CharField(verbose_name="Nombre", max_length=2048, null=False, blank=False)
    institution = models.CharField(verbose_name="Institución", max_length=1024, null=False, blank=False)
    license_code = models.CharField(verbose_name="Código o Número de Cédula", max_length=512, null=False, blank=False)
    evidence = models.FileField(verbose_name="Comprobante", upload_to=upload_employee_education_document, null=True,
                                blank=True)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name = "Formación Académica del Empleado"
        verbose_name_plural = "Formación Académica del Empleado"

    def __str__(self):
        return self.get_type_display() + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.get_type_display() + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name


# Test model to define the structure of it.
class Test(models.Model):
    key = models.CharField(verbose_name="Clave de la Prueba", max_length=512, null=False, blank=False)
    name = models.CharField(verbose_name="Nombre de la Prueba", max_length=512, null=False, blank=False)
    notes = models.CharField(verbose_name="Notas", max_length=1024, null=False, blank=False)
    class Meta:
        verbose_name_plural = "Pruebas a Empleados"
        verbose_name = "Pruebas a Empleados"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


# To represent the application of an employee to a test.
class TestApplication(models.Model):
    application_date = models.DateField(verbose_name="Fecha de Aplicación", null=False, blank=False)
    result = models.CharField(verbose_name="Resultado", max_length=512, null=False, blank=False)
    comments = models.CharField(verbose_name="Comentarios", max_length=2048, null=True, blank=True)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    test = models.ForeignKey(Test, verbose_name="Prueba", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Aplicaciones de Pruebas del Empleado"
        verbose_name = "Aplicación de Prueba del Empleado"

    def __str__(self):
        return self.test.name + ": " + self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.test.name + ": " + self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name


# To represent the structure of an employee's contract.
'''class EmployeeContract(models.Model):
    contract_key = models.CharField(verbose_name="Clave del Contrato", max_length=128, null=False, blank=False)
    description = models.CharField(verbose_name="Descripción del Contrato", max_length=4096, null=False, blank=False)
    specifications = models.CharField(verbose_name="Especificaciones del Contrato", max_length=4096, null=False,
                                      blank=False)
    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    end_date = models.DateField(verbose_name="Fecha de Término", null=True, blank=True)
    base_salary = models.FloatField(verbose_name="Salario", null=False, blank=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=True, blank=False)

    class Meta:
        verbose_name_plural = "Contratos del Empleado"
        verbose_name = "Contrato del Empleado"

    def __str__(self):
        return self.contract_key

    def __unicode__(self):  # __unicode__ on Python 2
        return self.contract_key'''


# To represent an employee's family member.
class FamilyMember(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno", max_length=255, null=False, blank=False)
    relationship = models.CharField(verbose_name="Parentesco", max_length=128, null=False, blank=True)
    career = models.CharField(verbose_name="Profesión", max_length=128, null=False, blank=True)
    age = models.IntegerField(verbose_name="Edad", null=True, blank=True, default=0)
    phone_number = models.CharField(verbose_name="Número de Teléfono", max_length=20, null=True, blank=True)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Familiares"
        verbose_name = "Familiar"

    def __str__(self):
        return self.name + " " + self.first_last_name + " " + self.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + " " + self.first_last_name + " " + self.second_last_name


# To represent an employee's emergency contact.
class EmergencyContact(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno", max_length=255, null=False, blank=False)
    phone_number = models.CharField(verbose_name="Número de Teléfono", max_length=20, null=True, blank=True)
    cellphone_number = models.CharField(verbose_name="Número de Celular", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=255, null=True, blank=True)

    colony = models.CharField(verbose_name="Colonia", max_length=255, null=False, blank=False)
    street = models.CharField(verbose_name="Calle", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    zip_code = models.CharField(verbose_name="Código Postal", max_length=5, null=False, blank=False)

    # Foreign Keys.

    # Attribute for the Chained Keys.
    country = models.ForeignKey(Pais, verbose_name="País", null=False, blank=False)
    state = ChainedForeignKey(Estado,
                              chained_field="country",
                              chained_model_field="pais",
                              show_all=False,
                              auto_choose=True,
                              sort=True,
                              verbose_name="Estado")
    town = ChainedForeignKey(Municipio,
                             chained_field="state",
                             chained_model_field="estado",
                             show_all=False,
                             auto_choose=True,
                             sort=True,
                             verbose_name="Municipio")
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Contactos de Emergencia"
        verbose_name = "Contacto de Emergencia"

    def __str__(self):
        return self.name + " " + self.first_last_name + " " + self.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + " " + self.first_last_name + " " + self.second_last_name


# To represent an employee's work reference.
class WorkReference(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False,
                            blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno",
                                       max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno",
                                        max_length=255, null=False, blank=False)
    company_name = models.CharField(verbose_name="Empresa", max_length=255, null=False, blank=False)
    first_phone_number = models.CharField(verbose_name="Número de Teléfono #1", max_length=20, null=False, blank=False)
    second_phone_number = models.CharField(verbose_name="Número de Teléfono #2", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=255, null=True, blank=True)
    notes = models.CharField(verbose_name="Notas", max_length=2048, null=True, blank=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Referencias Laborales"
        verbose_name = "Referencia Laboral"

    def __str__(self):
        return self.company_name + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.company_name + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name


# To represent an employee's dropout.
class EmployeeDropOut(models.Model):
    date = models.DateField(verbose_name="Fecha de Baja", null=False, blank=False)

    DROP_TYPE_A = 1
    DROP_TYPE_B = 2
    DROP_TYPE_C = 3
    DROP_TYPE_CHOICES = (
        (DROP_TYPE_A, 'Despido'),
        (DROP_TYPE_B, 'Renuncia'),
        (DROP_TYPE_C, 'Incapacidad'),
    )
    type = models.IntegerField(choices=DROP_TYPE_CHOICES, default=DROP_TYPE_A, verbose_name='Tipo de Baja')
    reason = models.CharField(verbose_name="Motivo", max_length=4096, null=False, blank=True)
    severance_pay = models.FloatField(verbose_name="Liquidación", null=True, blank=False)
    observations = tinymce_models.HTMLField(verbose_name='Observaciones', null=True, blank=True, max_length=4096)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Bajas de Empleados"
        verbose_name = "Baja de Empleado"

    def __str__(self):
        return self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name


class EmployeeAssistance(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    payroll_period = models.ForeignKey('PayrollPeriod', verbose_name="Periodo de nómina", null=False, blank=False)

    record_date = models.DateField(default=now, null=False, blank=False, verbose_name="Fecha")
    entry_time = models.TimeField(default=now, null=False, blank=False, verbose_name="Hora de Entrada")
    exit_time = models.TimeField(default=now, null=False, blank=False, verbose_name="Hora de Salida")
    absence = models.BooleanField(verbose_name="Ausente", default=True)
    justified = models.BooleanField(verbose_name="Justificada", default=False)

    class Meta:
        verbose_name_plural = "Asistencias"
        verbose_name = "Asistencia"
        unique_together = ('employee', 'payroll_period', 'record_date')

    def __str__(self):
        return self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name + \
               " registro de asistencia del " + str(self.record_date)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name + \
               " registro de asistencia del " + str(self.record_date)


def uploaded_absences_proofs(instance, filename):
    return '/'.join(
        ['absences_proof_uploads', str(instance.payroll_period.id) + instance.payroll_period.name, filename])


class AbsenceProof(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    payroll_period = models.ForeignKey('PayrollPeriod', verbose_name="Periodo de nómina", null=False, blank=False)

    document = models.FileField(verbose_name="Documento", blank=False, null=False, upload_to=uploaded_absences_proofs)
    description = models.CharField(verbose_name="Descripción", max_length=4096, null=False, blank=True)


def uploaded_employees_assistance_destination(instance, filename):
    return '/'.join(['assistance_uploads', str(instance.payroll_period.id) + instance.payroll_period.name, filename])


class UploadedEmployeeAssistanceHistory(models.Model):
    '''payroll_group = models.ForeignKey(PayrollGroup, verbose_name="Grupo", null=False, blank=False)
    payroll_period = ChainedForeignKey('PayrollPeriod',
                               chained_field="payroll_group",
                               chained_model_field="payroll_group",
                               show_all=False,
                               auto_choose=True,
                               sort=True,
                               unique=True)'''

    payroll_period = models.ForeignKey('PayrollPeriod', verbose_name="Periodo de nómina", null=False, blank=False)
    assistance_file = models.FileField(upload_to=uploaded_employees_assistance_destination, null=True,
                                       verbose_name="Archivo de Asistencias")

    class Meta:
        verbose_name_plural = "Archivos de Asistencias"
        verbose_name = "Archivo de asistencias"

    def __str__(self):
        return "Del " + str(self.payroll_period.start_period) + " al " + str(self.payroll_period.end_period) + \
               " - " + self.assistance_file.name

    def __unicode__(self):  # __unicode__ on Python 2
        return "Del " + str(self.payroll_period.start_period) + " al " + str(self.payroll_period.end_period) + \
               " - " + self.assistance_file.name


class EmployeeLoan(models.Model):
    PLAN_A = 1
    PLAN_B = 2
    PLAN_TYPE_CHOICES = (
        (PLAN_A, 'Plan A (12 periodos)'),
        (PLAN_B, 'Plan B (14 periodos)'),
    )
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    amount = models.FloatField(verbose_name="Cantidad", null=False, blank=False, default=0)
    payment_plan = models.IntegerField(verbose_name="Plan de Pago", choices=PLAN_TYPE_CHOICES, default=PLAN_A)
    request_date = models.DateField(verbose_name="Fecha de Solicitud", null=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Préstamos"
        verbose_name = "Préstamo"

    def __str__(self):
        return self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name


class EmployeeRequisition(models.Model):
    direction = models.ForeignKey('Direction', verbose_name='Dirección', null=False, blank=False)
    subdirection = models.ForeignKey('Subdirection', verbose_name='Subdirección', null=False, blank=False)
    area = models.ForeignKey('Area', verbose_name='Área', null=False, blank=False)
    department = models.ForeignKey('Department', verbose_name='Departamento', null=False, blank=False)



    description = models.CharField(verbose_name="Descripción", max_length=256, null=False, blank=False,
                           unique=False)

    vacancy_number = models.IntegerField(verbose_name='Número de Vacantes', null=False, default=1,
                                         validators={MinValueValidator(1)})

    minimum_requirements = tinymce_models.HTMLField(verbose_name='Requisitos Mínimos', null=True, blank=True,
                                                    max_length=4096)
    characteristics = tinymce_models.HTMLField(verbose_name='Características del Puesto', null=True, blank=True,
                                               max_length=4096)

    reason = tinymce_models.HTMLField(verbose_name='Razón', null=True, blank=True,
                                               max_length=4096)

    user = models.ForeignKey(User, verbose_name="Solicitado por:", null=True, blank=True)



    def __str__(self):
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description


    class Meta:
        verbose_name = "Requisición de Personal"
        verbose_name_plural = "Requisiciones de Personal"



# To represent a Job Profile.
class JobProfile(models.Model):
    job = models.CharField(verbose_name="Puesto", max_length=2048, null=False, blank=False,
                           unique=False)
    abilities =tinymce_models.HTMLField(verbose_name="Habilidades", max_length=2048, null=False, blank=True,
                                 unique=False)
    aptitudes = tinymce_models.HTMLField(verbose_name="Aptitudes", max_length=2048, null=False, blank=True,
                                 unique=False)
    knowledge = tinymce_models.HTMLField(verbose_name="Conocimientos", max_length=2048, null=False, blank=True,
                                 unique=False)
    competitions = tinymce_models.HTMLField(verbose_name="Competencias", max_length=2048, null=False, blank=True,
                                    unique=False)
    scholarship = tinymce_models.HTMLField(verbose_name="Escolaridad ", max_length=2048, null=False, blank=True,
                                   unique=False)
    experience = tinymce_models.HTMLField(verbose_name="Experiencia", max_length=2048, null=False, blank=True,
                                  unique=False)

    jobdescription = tinymce_models.HTMLField(verbose_name="Descripción del Puesto ", max_length=2048, null=False, blank=True,
                                   unique=False)
    minimumrequirements = tinymce_models.HTMLField(verbose_name="Requisitos Mínimos del Puesto", max_length=2048, null=False, blank=True,
                                  unique=False)


    entry_time = models.TimeField(verbose_name="Horario de Entrada", null=False, blank=False)
    exit_time = models.TimeField(verbose_name="Horario de Salida", null=False, blank=False)
    sunday = models.BooleanField(verbose_name="Domingo", default=False)
    monday = models.BooleanField(verbose_name="Lunes", default=True)
    tuesday = models.BooleanField(verbose_name="Martes", default=True)
    wednesday = models.BooleanField(verbose_name="Miércoles", default=True)
    thursday = models.BooleanField(verbose_name="Jueves", default=True)
    friday = models.BooleanField(verbose_name="Viernes", default=True)
    saturday = models.BooleanField(verbose_name="Sábado", default=True)

    # Foreign Keys.
    direction = models.ForeignKey('Direction', verbose_name='Dirección', null=False, blank=False)
    subdirection = models.ForeignKey('Subdirection', verbose_name='Subdirección', null=False, blank=False)
    area = models.ForeignKey('Area', verbose_name='Área', null=False, blank=False)
    department = models.ForeignKey('Department', verbose_name='Departamento', null=False, blank=False)
    minimumsalary = models.DecimalField(verbose_name='Salario Mínimo', max_digits=20, decimal_places=2, null=True,
                                        default=0.0)
    maximumsalary = models.DecimalField(verbose_name='Salario Máximo', max_digits=20, decimal_places=2, null=True,
                                        default=0.0)

    class Meta:
        verbose_name_plural = "Perfiles de Puesto"
        verbose_name = "Perfil de Puesto"

    def __str__(self):
        return self.job

    def __unicode__(self):  # __unicode__ on Python 2
        return self.job


# To represent a Direction.
class Direction(models.Model):
    name = models.CharField(verbose_name="Dirección", max_length=2048, null=False, blank=False,
                            unique=False)

    class Meta:
        verbose_name_plural = "Direcciones"
        verbose_name = "Dirección"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


# To represent a Subdirection.
class Subdirection(models.Model):
    name = models.CharField(verbose_name="Subdirección", max_length=2048, null=False, blank=False,
                            unique=False)

    class Meta:
        verbose_name_plural = "Subdirecciones"
        verbose_name = "Subdirección"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


# To represent an Area.
class Area(models.Model):
    name = models.CharField(verbose_name="Área", max_length=2048, null=False, blank=False,
                            unique=False)

    class Meta:
        verbose_name_plural = "Áreas"
        verbose_name = "Área"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


# To represent a DEpartment.
class Department(models.Model):
    name = models.CharField(verbose_name="Departamento", max_length=2048, null=False, blank=False,
                            unique=False)

    class Meta:
        verbose_name_plural = "Departamentos"
        verbose_name = "Departamento"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    def to_serilizable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['name'] = str(self.name)
        return ans


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Model for an specific employee position description.


class EmployeePositionDescription(models.Model):
    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    end_date = models.DateField(verbose_name="Fecha de Termino", null=False, blank=False)
    physical_location = models.CharField(verbose_name="Ubicación Física", max_length=250, null=False, blank=True)
    entry_time = models.TimeField(verbose_name="Hora de Entrada", null=True, auto_now_add=False)
    departure_time = models.TimeField(verbose_name="Hora de Salida", null=True, auto_now_add=False)
    observations = models.CharField(verbose_name="Observaciones", null=True, blank=False, max_length=500)
    monday = models.BooleanField(verbose_name="Lunes", default=True)
    tuesday = models.BooleanField(verbose_name="Martes", default=True)
    wednesday = models.BooleanField(verbose_name="Miércoles", default=True)
    thursday = models.BooleanField(verbose_name="Jueves", default=True)
    friday = models.BooleanField(verbose_name="Viernes", default=True)
    saturday = models.BooleanField(verbose_name="Sábado", default=True)
    sunday = models.BooleanField(verbose_name="Domingo", default=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    payroll_group = models.ForeignKey(PayrollGroup, verbose_name="Grupo de Nómina", null=False, blank=False)
    direction = models.ForeignKey(Direction, verbose_name='Dirección', null=False, blank=False)
    subdirection = models.ForeignKey(Subdirection, verbose_name='Subdirección', null=False, blank=False)
    # subdirection = ChainedForeignKey(Subdirection,
    #                                  chained_field="direction",
    #                                  chained_model_field="direction",
    #                                  show_all=False,
    #                                  auto_choose=True,
    #                                  sort=True)
    department = models.ForeignKey(Department, verbose_name='Departamento', null=False, blank=False)
    # department = ChainedForeignKey(Department,
    #                                chained_field="subdirection",
    #                                chained_model_field="subdirection",
    #                                show_all=False,
    #                                auto_choose=True,
    #                                sort=True)
    area = models.ForeignKey(Area, verbose_name='Área', null=False, blank=False)
    # area = ChainedForeignKeyChainedForeignKey(Area,
    #                          chained_field="subdirection",
    #                          chained_model_field="subdirection",
    #                          show_all=False,
    #                          auto_choose=True,
    #                          sort=True)

    job_profile = models.ForeignKey(JobProfile, verbose_name='Puesto', null=False, blank=False)
    contract = models.CharField(verbose_name="Contrato", null=False, blank=False, max_length=45)

    # immediate_boss = models.ForeignKey(Instance_Position, verbose_name="Jefe Inmediato", null=False, blank=False)


    class Meta:
        verbose_name_plural = "Descripción de Puesto del Empleado"
        verbose_name = "Descripción de Puesto del Empleado"

    def __str__(self):
        return self.payroll_group.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.payroll_group.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def to_serilizable_dic(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['payroll_group'] = str(self.payroll_group.name)
        return ans


class EmployeeFinancialData(models.Model):
    DEPOSITO = 'D'
    EFECTIVO = 'E'
    TRANSFERENCIA = 'T'
    PAYMENT_METHOD_CHOICES = (
        ('D', 'Deposito'),
        ('E', 'Efectivo'),
        ('T', 'Transferencia Interbancaria'),
    )

    account_number = models.IntegerField(verbose_name='Número de Cuenta', null=False, default=0)
    CLABE = models.IntegerField(verbose_name='CLABE', null=False, default=0)
    monthly_salary = models.DecimalField(verbose_name='Salario Mensual', max_digits=20, decimal_places=2, null=True)
    daily_salary = models.DecimalField(verbose_name='Salario Diario', max_digits=20, decimal_places=2, null=True)
    aggregate_daily_salary = models.DecimalField(verbose_name='Salario Diario Acumulado', max_digits=20,
                                                 decimal_places=2, null=True)
    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default=DEPOSITO,
                                      verbose_name='Forma de Pago')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default=DEPOSITO,
                                      verbose_name='Forma de Pago')
    bank = models.ForeignKey(Bank, null=False, blank=False, verbose_name="Banco")

    class Meta:
        verbose_name_plural = "Datos Financieros del Empleado"
        verbose_name = "Datos Financieros del Empleado"


class InfonavitData(models.Model):
    infonavit_credit_number = models.CharField(verbose_name="Número de Crédito", null=False, blank=False,
                                               max_length=30, )
    discount_type = models.CharField(verbose_name="Tipo de Descuento", null=False, blank=False, max_length=30, )
    discount_amount = models.CharField(verbose_name="Monto de Descuento", null=False, blank=False, max_length=30, )
    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    credit_term = models.CharField(verbose_name="Duración de Crédito", null=False, blank=False, max_length=200)
    comments = models.TextField(verbose_name="Observaciones", null=True, blank=True, max_length=500, )

    # Foreign Keys.
    employee_financial_data = models.OneToOneField(EmployeeFinancialData)

    class Meta:
        verbose_name_plural = "Datos del Infonavit del Empleado"
        verbose_name = "Datos del Infonavit del Empleado"

    def __str__(self):
        return "Crédito :" + self.infonavit_credit_number + " del empleado " + self.employee_financial_data.employee.employee_key

    def __unicode__(self):  # __unicode__ on Python 2
        return "Crédito :" + self.infonavit_credit_number + " del empleado " + self.employee_financial_data.employee.employee_key


class EarningsDeductions(models.Model):
    FIJA = 'F'
    VARIABLE = 'V'
    EARNINGDEDUCTIONSCATEGORY_CHOICES = (
        ('F', 'Fija'),
        ('V', 'Variable'),
    )

    DEDUCCION = 'D'
    PERCEPCION = 'P'
    EARNINGDEDUCTIONTYPE_CHOICES = (
        (DEDUCCION, 'Deducción'),
        (PERCEPCION, 'Percepción'),
    )

    SI = 'Y'
    NO = 'N'
    YNTYPE_CHOICES = (
        (SI, 'Si'),
        (NO, 'No'),
    )

    ACTIVA = 'A'
    NO_ACTIVA = 'N'
    STATUS_CHOICES = (
        (ACTIVA, 'ACTIVA'),
        (NO_ACTIVA, 'NO ACTIVA'),
    )

    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30, )
    percent_taxable = models.IntegerField("Porcentaje Gravable", blank=False, null=False)
    sat_key = models.CharField(verbose_name="Clave SAT", null=False, blank=False, max_length=30, )
    #law_type = models.CharField(verbose_name="Tipo de Ley", null=False, blank=False, max_length=30, )
    status = models.CharField(verbose_name="Estatus", null=False, blank=False, max_length=1, choices=STATUS_CHOICES,
                              default=ACTIVA)
    account = models.ForeignKey(Account, verbose_name='Cuenta', null=True, blank=True,)
        #models.IntegerField("Cuenta Contable", blank=False, null=False)
    comments = models.TextField(verbose_name="Observaciones", null=False, blank=False, max_length=500, )
    type = models.CharField(max_length=1, choices=EARNINGDEDUCTIONTYPE_CHOICES, default=DEDUCCION, verbose_name="Tipo")
    taxable = models.CharField(max_length=1, choices=YNTYPE_CHOICES, default=NO, verbose_name="Gravable")
    category = models.CharField(max_length=1, choices=EARNINGDEDUCTIONSCATEGORY_CHOICES, default=FIJA,
                                verbose_name="Categoria")
    penalty = models.CharField(max_length=1, choices=YNTYPE_CHOICES, default=NO, verbose_name="Penalización")

    class Meta:
        verbose_name_plural = "Percepciones y Deducciones"
        verbose_name = "Percepciones y Deducciones"

    def __str__(self):
        return self.type + "-" + self.name + " - " + str(self.account.id)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.type + "-" + self.name


    def get_accumulated_for_period(self, payroll_period_id):
        total_fixed = 0
        records = EmployeeEarningsDeductions.objects.filter(concept_id=self.id)
        for record in records:
            total_fixed += record.ammount

        total_variable = 0
        records = EmployeeEarningsDeductionsbyPeriod.objects.filter(Q(concept_id=self.id) & Q(payroll_period_id=payroll_period_id))
        for record in records:
            total_variable += record.ammount

        return total_fixed, total_variable

    def save(self, *args, **kwargs):
        can_save = True

        if can_save:
            Logs.log("Saving new EarningsDeductions", "Te")
            super(EarningsDeductions, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


class EmployeeEarningsDeductions(models.Model):
    '''
        To keep a history of the applied employee earnings and deductions.
    '''
    ammount = models.DecimalField(verbose_name="Monto", decimal_places=2, blank=False, null=False,
                                  default=0, max_digits=20,
                                  validators=[MinValueValidator(Decimal('0.0'))])
    date = models.DateField(verbose_name="Fecha", null=False, blank=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    concept = models.ForeignKey(EarningsDeductions, verbose_name="Concepto", null=False, blank=False, limit_choices_to={
        'category': 'F', 'status':'A',
    })

    class Meta:
        verbose_name_plural = "Deducciones y Percepciones por Empleado"
        verbose_name = "Deducciones y Percepciones por Empleado"
        unique_together = (('concept', 'employee'),)


class PayrollType(models.Model):
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30, )

    class Meta:
        verbose_name_plural = "Tipo de Nómina"
        verbose_name = "Tipos de Nómina"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


class PayrollToProcess(models.Model):
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30, )
    # Foreign Keys.
    payroll_type = models.ForeignKey(PayrollType, verbose_name="Tipo de Nómina", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Nómina a Procesar"
        verbose_name = "Nómina a Procesar"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


class PayrollPeriod(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    MONTH_CHOICES = (
        (JANUARY, 'Enero'),
        (FEBRUARY, 'Febrero'),
        (MARCH, 'Marzo'),
        (APRIL, 'Abril'),
        (MAY, 'Mayo'),
        (JUNE, 'Junio'),
        (JULY, 'Julio'),
        (AUGUST, 'Agosto'),
        (SEPTEMBER, 'Septiembre'),
        (OCTOBER, 'Octubre'),
        (NOVEMBER, 'Noviembre'),
        (DECEMBER, 'Diciembre'),
    )
    payroll_group = models.ForeignKey(PayrollGroup, verbose_name="Grupo de Nómina", null=False, blank=False)
    payroll_to_process = models.ForeignKey(PayrollToProcess, verbose_name="Nómina a procesar", null=False, blank=False)
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30, )
    month = models.IntegerField(verbose_name="Mes", choices=MONTH_CHOICES, default=JANUARY)
    year = models.IntegerField(verbose_name="Año", null=False, blank=False, default=2017,
                               validators=[MaxValueValidator(9999), MinValueValidator(2017)])
    fortnight = models.IntegerField(verbose_name="Semana", null=False, blank=False, default=1,
                                    validators=[MaxValueValidator(24), MinValueValidator(1)])
    start_period = models.DateField(verbose_name="Inicio de Periodo", null=False, blank=False)
    end_period = models.DateField(verbose_name="Fin de Periodo", null=False, blank=False)


    exclusions = models.ManyToManyField('Employee', through='EmployeePayrollPeriodExclusion',through_fields=('payroll_period', 'employee',),)


    class Meta:
        verbose_name_plural = "Periodos de Nómina"
        verbose_name = "Periodos de Nómina"

    def __str__(self):
        return self.name + " del " + str(self.start_period) + " al " + str(self.end_period)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + " del " + str(self.start_period) + " al " + str(self.end_period)



class EmployeePayrollPeriodExclusion(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    payroll_period = models.ForeignKey(PayrollPeriod, verbose_name="Periodo de Nómina", null=False, blank=False)

    class Meta:
        unique_together = (("employee", "payroll_period"),)






class EmployeeEarningsDeductionsbyPeriod(models.Model):
    ammount = models.DecimalField(verbose_name="Monto", decimal_places=2, blank=False, null=False,
                                  default=0, max_digits=20,
                                  validators=[MinValueValidator(Decimal('0.0'))])
    date = models.DateField(verbose_name="Fecha", null=False, blank=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    concept = models.ForeignKey(EarningsDeductions, verbose_name="Conceptos", null=False, blank=False, limit_choices_to={
        'category': 'V', 'status':'A',
    })
    payroll_period = models.ForeignKey(PayrollPeriod, verbose_name="Periodo de Nómina", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Deducciones y Percepciones por Periodo"
        verbose_name = "Deducciones y Percepciones por Periodo"

    def deleteFromEmployeeLoanDetail(self, data):
        obj = EmployeeEarningsDeductionsbyPeriod.objects.get(employee_id=data.employeeloan.employee.id,
                                                             payroll_period_id=data.period.id)
        super(EmployeeEarningsDeductionsbyPeriod, obj).delete()

    def create(self, data):
        existe = EmployeeEarningsDeductionsbyPeriod.objects.filter(employee_id=data.employeeloan.employee.id,
                                                                   payroll_period_id=data.period.id)
        if existe.count() > 0:
            obj = EmployeeEarningsDeductionsbyPeriod.objects.get(employee_id=data.employeeloan.employee.id,
                                                                 payroll_period_id=data.period.id)
            if obj.id > 0:
                obj.ammount = data.amount
                obj.payroll_period_id = data.period.id
                obj.save()
                super(EmployeeEarningsDeductionsbyPeriod, obj).save()
        else:
            self.ammount = data.amount
            self.date = now()
            self.employee_id = data.employeeloan.employee.id
            self.concept_id = 1
            self.payroll_period_id = data.period.id

            super(EmployeeEarningsDeductionsbyPeriod, self).save()

    def save(self, *args, **kwargs):
        super(EmployeeEarningsDeductionsbyPeriod, self).save(*args, **kwargs)

    def __str__(self):
        return "Amount: " + str(self.ammount)


class EmployeeLoanDetail(models.Model):
    employeeloan = models.ForeignKey(EmployeeLoan, verbose_name='Préstamo', null=False, blank=False)
    # period = models.IntegerField(verbose_name='Periodo a Cobrar', null=False, default=getParameters.getPeriodNumber())

    # The group is here to use chained keys
    payroll_group = models.ForeignKey(PayrollGroup, verbose_name="Grupo", null=False, blank=False)
    period = ChainedForeignKey(PayrollPeriod,
                               chained_field="payroll_group",
                               chained_model_field="payroll_group",
                               show_all=False,
                               auto_choose=True,
                               sort=True)
    amount = models.FloatField(verbose_name="Cantidad", null=False, blank=False)
    deduction = models.ForeignKey(EmployeeEarningsDeductionsbyPeriod, verbose_name="Deduction", null=True, blank=True)



    class Meta:
        verbose_name_plural = "Préstamos Detalle"
        verbose_name = "Préstamo Detalle"
        unique_together = ('employeeloan', 'period')

    def delete(self):
        payrollExist = PayrollReceiptProcessed.objects.filter(employee_id=self.employeeloan.employee_id,
                                                              payroll_period_id=self.period.id)
        existReceipt = 0
        for pE in payrollExist:
            existReceipt = 1
        if existReceipt == 0:
            delModel = EmployeeEarningsDeductionsbyPeriod()
            delModel.deleteFromEmployeeLoanDetail(self)
            super(EmployeeLoanDetail, self).delete()

    def save(self, *args, **kwargs):
        if self.deduction is None:
            deduction = EmployeeEarningsDeductionsbyPeriod()
            deduction.ammount = self.amount
            deduction.date = now()
            deduction.employee_id = self.employeeloan.employee.id
            deduction.concept_id = 1
            deduction.payroll_period_id = self.period.id
            deduction.save()
            self.deduction_id = deduction.id
            super(EmployeeLoanDetail, self).save(*args, **kwargs)
        else:
            self.deduction.ammount = self.amount
            self.deduction.date = now()
            self.deduction.employee_id = self.employeeloan.employee.id
            self.deduction.concept_id = 1
            self.deduction.payroll_period_id = self.period.id
            self.deduction.save()
            super(EmployeeLoanDetail, self).save(*args, **kwargs)


    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('employeeloan', 'period'):
            return 'la amortización del préstamo para este periodo ya existe'
        else:
            return super(EmployeeLoanDetail, self).unique_error_message(model_class, unique_check)
    
class EarningDeductionPeriod(models.Model):
    '''
        Earnings and deductions to be applied to the employee.
    '''
    # Foreign Keys.
    payroll_period = models.ForeignKey(PayrollPeriod, verbose_name="Periodo de Nómina", null=False, blank=False)
    employee_earnings_deductions = models.ForeignKey(EmployeeEarningsDeductions, verbose_name="Deducción/Percepción",
                                                     null=False, blank=False)

    class Meta:
        verbose_name_plural = "Periodo Percepción / Deducción"
        verbose_name = "Periodo Percepción / Deducción"

    def __str__(self):
        return str(self.payroll_period.name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.payroll_period.name)


class PayrollReceiptProcessed(models.Model):
    SI = 'Y'
    NO = 'N'
    YNTYPE_CHOICES = (
        (SI, 'Si'),
        (NO, 'No'),
    )

    worked_days = models.DecimalField(verbose_name="Días Trabajados", null=False, blank=False, max_digits=20,
                                      decimal_places=2)
    total_perceptions = models.DecimalField(verbose_name="Total de Percepciones", null=False, blank=False,
                                            max_digits=20, decimal_places=2)
    total_deductions = models.DecimalField(verbose_name="Total de Deducciones", null=False, blank=False, max_digits=20,
                                           decimal_places=2)
    total_payroll = models.DecimalField(verbose_name="Total Neto", null=False, blank=False, max_digits=20,
                                        decimal_places=2)
    taxed = models.DecimalField(verbose_name="Grabado", null=True, blank=True, max_digits=20, decimal_places=2)
    exempt = models.DecimalField(verbose_name="Excento", null=True, blank=True, max_digits=20, decimal_places=2)
    daily_salary = models.DecimalField(verbose_name="Salario Diario", null=True, blank=True, max_digits=20,
                                       decimal_places=2)
    total_withholdings = models.DecimalField(verbose_name="Total de Deducciones", null=True, blank=True,
                                             max_digits=20, decimal_places=2)
    total_discounts = models.DecimalField(verbose_name="Total de Descuentos", null=True, blank=True, max_digits=20,
                                          decimal_places=2)
    printed_receipt = models.CharField(max_length=1, choices=YNTYPE_CHOICES, default=SI)
    stamp_version = models.DecimalField(verbose_name="Versión de Timbrado", null=True, blank=True, max_digits=20,
                                        decimal_places=2)
    stamp_UUID = models.CharField(verbose_name="UUID de Timbrado", null=True, blank=True, max_length=500)
    stamp_date = models.DateTimeField(verbose_name="Fecha de Timbrado", null=True, blank=True)
    stamp_CFDI = models.CharField(verbose_name="CFDI Timbrado", null=True, blank=True, max_length=500)
    sat_certificate = models.CharField(verbose_name="Certificado del SAT", null=True, blank=True, max_length=500)
    stamp_sat = models.CharField(verbose_name="Timbrado del SAT", null=True, blank=True, max_length=500)
    stamp_xml = models.CharField(verbose_name="XML del Timbrado", null=True, blank=True, max_length=500)
    stamp_serie_id = models.CharField(verbose_name="Serie ID  de Timbrado", null=True, blank=True, max_length=500)
    payment_date = models.DateField(verbose_name="Fecha de Pago", null=True, blank=True)

    # foreign

    payroll_period = models.ForeignKey(PayrollPeriod, verbose_name="Periodo de Nómina", null=False,
                                       blank=False)
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False,
                                 blank=False)

    class Meta:
        verbose_name_plural = "Recibo de Nómina Procesada"
        verbose_name = "Recibo de Nómina Procesada"
        unique_together = ('payroll_period', 'employee')


class PayrollProcessedDetail(models.Model):
    # Foreign Keys.
    payroll_receip_processed = models.ForeignKey(PayrollReceiptProcessed, verbose_name="Recibo de Nómina Procesado",
                                                 null=False, blank=False)

    name = models.CharField(verbose_name="Nombre", null=True, blank=True, max_length=30, )
    percent_taxable = models.IntegerField("Porcentaje Gravable", blank=True, null=True)
    sat_key = models.CharField(verbose_name="Clave SAT", null=True, blank=True, max_length=30, )
    law_type = models.CharField(verbose_name="Tipo de Ley", null=True, blank=True, max_length=30, )
    status = models.CharField(verbose_name="Estatus", null=True, blank=True, max_length=64)
    accounting_account = models.IntegerField("Cuenta Contable", blank=True, null=True)
    comments = models.CharField(verbose_name="Observaciones", null=True, blank=True, max_length=500, )
    type = models.CharField(verbose_name="Tipo", max_length=64)
    taxable = models.CharField(verbose_name="Gravable", max_length=64)
    category = models.CharField(verbose_name="Categoria", max_length=64)
    amount = models.FloatField(verbose_name="Monto", null=False)

    class Meta:
        verbose_name_plural = "Detalle de Nómina Procesada"
        verbose_name = "Detalle de Nómina Procesada"


class JobInstance(models.Model):
    # Job Description ***
    job_profile = models.ForeignKey(JobProfile, verbose_name='Perfil de Empleo', null=False, blank=False)
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=True, blank=True)
    parent_job_instance = models.ForeignKey('self', verbose_name='Jefe Inmediato', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vacante de Puesto"
        verbose_name = "Vacante de Empleos"

    def __str__(self):
        return str(self.id)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.id)

    def can_be_deleted(self):
        if self.id != 1:
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        if self.can_be_deleted():
            return super(JobInstance, self).delete(using, keep_parents)
        print 'Job Instance can\'t be deleted, it is the root.'
        return False
