# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Libraries.
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from decimal import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator

# Third Party Libraries
from smart_selects.db_fields import ChainedForeignKey


# Importing model from other apps.
from ERP.models import Pais, Estado, Municipio, Project

# Create your models here.
from multiselectfield import MultiSelectField



# Employee General Information.
class Employee(models.Model):
    employee_key = models.CharField(verbose_name="Clave del Empleado", max_length=64, null=False, blank=False, unique=False)
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno", max_length=255, null=False, blank=False)

    TYPE_A = 1
    TYPE_B = 2
    EMPLOYEE_TYPE_CHOICES = (
        (TYPE_A, 'Empleado Tipo A'),
        (TYPE_B, 'Empleado Tipo B'),
    )
    type = models.IntegerField(choices=EMPLOYEE_TYPE_CHOICES, default=TYPE_A, verbose_name='Tipo de Empleando')
    registry_date = models.DateField(default=now(), null=False, blank=False, verbose_name="Fecha de Registro")

    STATUS_A = 1
    STATUS_B = 2
    EMPLOYEE_STATUS_CHOICES = (
        (STATUS_A, 'Estatus A del Empleado'),
        (STATUS_B, 'Estatus B del Empleado'),
    )
    status = models.IntegerField(choices=EMPLOYEE_STATUS_CHOICES, default=STATUS_A, verbose_name='Estatus del Empleado')
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
    MARITAL_STATUS_B= 2
    EMPLOYEE_MARITAL_STATUS_CHOICES = (
        (MARITAL_STATUS_A, 'Soltero'),
        (MARITAL_STATUS_B, 'Casado'),
    )
    marital_status = models.IntegerField(choices=EMPLOYEE_MARITAL_STATUS_CHOICES, default=MARITAL_STATUS_A, verbose_name='Estado Civil')
    curp = models.CharField(verbose_name="CURP", max_length=18, null=False, blank=False, unique=True)
    rfc = models.CharField(verbose_name="RFC", max_length=13, null=False, blank=False, unique=True)
    phone_number = models.CharField(verbose_name="Teléfono", max_length=20, null=False, blank=False)
    cellphone_number = models.CharField(verbose_name="Celular", max_length=20, null=False, blank=True)
    office_number = models.CharField(verbose_name="Teléfono de Oficina", max_length=20, null=False, blank=True)
    extension_number = models.CharField(verbose_name="Número de Extensión", max_length=10, null=False, blank=True)
    personal_email = models.CharField(verbose_name="Correo Electrónico Personal", max_length=255, null=True, blank=False)
    work_email = models.CharField(verbose_name="Correo Electrónico Laboral", max_length=255, null=False, blank=False)

    social_security_number = models.CharField(verbose_name="Número de Seguro Social", max_length=20, null=False, blank=False)
    colony = models.CharField(verbose_name="Colonia", max_length=255, null=False, blank=False)
    street = models.CharField(verbose_name="Calle", max_length=255, null=False, blank=False)
    outdoor_number = models.CharField(verbose_name="No. Exterior", max_length=10, null=False, blank=False)
    indoor_number = models.CharField(verbose_name="No. Interior", max_length=10, null=True, blank=True)
    zip_code = models.CharField(verbose_name="Código Postal", max_length=5, null=False, blank=False)

    BLOOD_TYPE_A = 1
    BLOOD_TYPE_B = 2
    BLOOD_TYPE_CHOICES = (
        (BLOOD_TYPE_A, 'O Negativo'),
        (BLOOD_TYPE_B, 'O Positivo'),
    )
    blood_type = models.IntegerField(choices=BLOOD_TYPE_CHOICES, default=BLOOD_TYPE_A,verbose_name='Tipo Sanguíneo')
    driving_license_number = models.CharField(verbose_name="Número de Licencia de Conducir", max_length=20, null=False, blank=True)
    driving_license_expiry_date = models.DateField(null=False, blank=True, verbose_name="Expiración de Licencia para Conducir")

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

    def __str__(self):
        return self.employee_key + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee_key + ": " + self.name + " " + self.first_last_name + " " + self.second_last_name

    class Meta:
        verbose_name_plural = 'Empleados'
        verbose_name = 'Empleado'


# Employee Checker Data.
class CheckerData(models.Model):
    CHECKER_TYPE_A = 1
    CHECKER_TYPE_B = 2
    CHECKER_TYPE_CHOICES = (
        (CHECKER_TYPE_A, 'Automático'),
        (CHECKER_TYPE_B, 'Manual')
    )
    checker_type = models.IntegerField(choices=CHECKER_TYPE_CHOICES, default=CHECKER_TYPE_A, verbose_name='Tipo de Checador')

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
        return self.get_checker_type_display()


    def __unicode__(self):  # __unicode__ on Python 2
        return self.get_checker_type_display()


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
    return '/'.join(['human_resources', 'employee_documents',instance.employee.employee_key, filename])


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
        verbose_name_plural = 'Tipo de Documento'
        verbose_name = 'Etiquetas'


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
        verbose_name = "Etiqueta del Empleado"
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
    EDUCATION_TYPE_CHOICES = (
        (EDUCATION_TYPE_A, 'Licenciatura'),
        (EDUCATION_TYPE_B, 'Maestría'),
        (EDUCATION_TYPE_C, 'Doctorado')
    )
    type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES, default=EDUCATION_TYPE_A, verbose_name='Tipo de Educación')
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
    return '/'.join(['human_resources', 'employee_documents','current_education',instance.current_education.employee.employee_key, filename])


# Employee Current Education Documents.
class CurrentEducationDocument(models.Model):
    file = models.FileField(upload_to=upload_employee_current_education_document, null=True, verbose_name="Archivo", blank=True)
    comments = models.CharField(verbose_name="Comentarios", max_length=2048, null=True, blank=True, unique=False)

    # Foreign Keys.
    current_education = models.ForeignKey(CurrentEducation, verbose_name='Formación Actual del Empleado', null=False, blank=False)

    def __str__(self):
        return self.file.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.file.name

    class Meta:
        verbose_name_plural = 'Documentos de la Formación Actual del Empleado'
        verbose_name = 'Documento de la Formación Actual del Empleado'


# Method to save the employee's current education file.
def upload_employee_education_document(instance, filename):
    return '/'.join(['human_resources', 'employee_documents', 'education',instance.employee.employee_key, filename])


# Employee Education Records.
class Education(models.Model):
    EDUCATION_TYPE_A = 1
    EDUCATION_TYPE_B = 2
    EDUCATION_TYPE_C = 3
    EDUCATION_TYPE_CHOICES = (
        (EDUCATION_TYPE_A, 'Licenciatura'),
        (EDUCATION_TYPE_B, 'Maestría'),
        (EDUCATION_TYPE_C, 'Doctorado')
    )
    type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES, default=EDUCATION_TYPE_A,
                               verbose_name='Tipo de Educación')
    name = models.CharField(verbose_name="Nombre", max_length=2048, null=False, blank=False)
    institution = models.CharField(verbose_name="Institución", max_length=1024, null=False, blank=False)
    license_code = models.CharField(verbose_name="Código o Número de Cédula", max_length=512, null=False, blank=False)
    evidence = models.FileField(verbose_name="Comprobante", upload_to=upload_employee_education_document, null=True, blank=True)

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
    name = models.CharField(verbose_name="Nombre de la Prueba", max_length=512, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Pruebas"
        verbose_name = "Prueba"

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
class EmployeeContract(models.Model):
    contract_key = models.CharField(verbose_name="Clave del Contrato", max_length=128, null=False, blank=False)
    description = models.CharField(verbose_name="Descripción del Contrato", max_length=4096, null=False, blank=False)
    specifications = models.CharField(verbose_name="Especificaciones del Contrato", max_length=4096, null=False, blank=False)
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
        return self.contract_key


# To represent an employee's family member.
class FamilyMember(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno", max_length=255, null=False, blank=False)
    relationship = models.CharField(verbose_name="Parentesco", max_length=128, null=False, blank=True)

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

    # Foreign Keys.
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
    name = models.CharField(verbose_name="Nombre de la Persona que Hace la Referencia", max_length=255, null=False, blank=False, unique=False)
    first_last_name = models.CharField(verbose_name="Apellido Paterno de la Persona que Hace la Referencia", max_length=255, null=False, blank=False)
    second_last_name = models.CharField(verbose_name="Apellido Materno de la Persona que Hace la Referencia", max_length=255, null=False, blank=False)
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
    DROP_TYPE_CHOICES = (
        (DROP_TYPE_A, 'Despido'),
        (DROP_TYPE_B, 'Incapacidad'),
    )
    type = models.IntegerField(choices=DROP_TYPE_CHOICES, default=DROP_TYPE_A,verbose_name='Tipo de Baja')
    reason = models.CharField(verbose_name="Motivo", max_length=4096, null=False, blank=True)
    severance_pay = models.FloatField(verbose_name="Liquidación", null=True, blank=False)
    observations = models.CharField(verbose_name="Observaciones", null=True, blank=False, max_length=4096)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Bajas de Empleado"
        verbose_name = "Baja de Empleado"

    def __str__(self):
        return self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.employee.name + ": " + self.employee.first_last_name + ": " + self.employee.second_last_name


class EmployeeAssistance(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    # Period

    date = models.DateField(default=now(), null=False, blank=False, verbose_name="Fecha")
    entry_time = models.TimeField(default=now(), null=False, blank=False, verbose_name="Hora de Entrada")
    exit_time = models.TimeField(default=now(), null=False, blank=False, verbose_name="Hora de Salida")


    class Meta:
        verbose_name_plural = "Asistencias"
        verbose_name = "Asistencia"



class EmployeeLoan(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Empleado', null=False, blank=False)
    # Period

    # Start_Period ***
    # End_Period   ***

    amount = models.FloatField(verbose_name="Cantidad", null=False, blank=False)


    class Meta:
        verbose_name_plural = "Préstamos"
        verbose_name = "Préstamo"



# To represent a Job Profile.
class JobProfile(models.Model):
    job = models.CharField(verbose_name="Puesto", max_length=2048, null=False, blank=False,
                                   unique=False)
    abilities = models.CharField(verbose_name="Habilidades", max_length=2048, null=False, blank=True,
                                   unique=False)
    aptitudes = models.CharField(verbose_name="Aptitudes", max_length=2048, null=False, blank=True,
                                   unique=False)
    knowledge = models.CharField(verbose_name="Conocimientos", max_length=2048, null=False, blank=True,
                                 unique=False)
    competitions = models.CharField(verbose_name="Competencias", max_length=2048, null=False, blank=True,
                                 unique=False)
    scholarship = models.CharField(verbose_name="Escolaridad ", max_length=2048, null=False, blank=True,
                                 unique=False)
    experience = models.CharField(verbose_name="Experiencia", max_length=2048, null=False, blank=True,
                                 unique=False)
    entry_time = models.TimeField(verbose_name="Horario de Entrada", null=False, blank=False)
    exit_time = models.TimeField(verbose_name="Horario de Salida", null=False, blank=False)
    sunday = models.BooleanField(verbose_name="Domingo", default= False)
    monday = models.BooleanField(verbose_name="Lunes", default= True)
    tuesday = models.BooleanField(verbose_name="Martes", default= True)
    wednesday = models.BooleanField(verbose_name="Miércoles", default= True)
    thursday = models.BooleanField(verbose_name="Jueves", default= True)
    friday = models.BooleanField(verbose_name="Viernes", default= True)
    saturday = models.BooleanField(verbose_name="Sábado", default= True)

    # Foreign Keys.
    direction = models.ForeignKey('Direction', verbose_name='Dirección', null=False, blank=False)
    subdirection = models.ForeignKey('Subdirection', verbose_name='Subdirección', null=False, blank=False)
    area = models.ForeignKey('Area', verbose_name='Área', null=False, blank=False)
    department = models.ForeignKey('Department', verbose_name='Departamento', null=False, blank=False)


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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Model for an specific employee position description.


class EmployeePositionDescription(models.Model):
    CORPORATIVA='C'
    PROYECTO='P'
    PAYROLLCLASSIFICATION_CHOICES = (
        (CORPORATIVA, 'Corporativa'),
        (PROYECTO, 'Proyecto'),
    )

    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    end_date = models.DateField(verbose_name="Fecha de Termino", null=False, blank=False)
    physical_location = models.CharField(verbose_name="Ubicación Física", max_length=250, null=False, blank=True)
    insurance_type = models.CharField(verbose_name="Tipo de Seguro", null=True, blank=False, max_length=100)
    insurance_number = models.CharField(verbose_name="Número de Seguro", null=True, blank=False, max_length=100)
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
    area = models.ForeignKey(Area, verbose_name='Área', null=False, blank=False)
    department = models.ForeignKey(Department, verbose_name='Departamento', null=False, blank=False)
    job_profile = models.ForeignKey(JobProfile, verbose_name='Puesto', null=False, blank=False)
    #contract = models.ForeignKey(Contract, verbose_name="Contrato", null=False, blank=False)
    #immediate_boss = models.ForeignKey(Instance_Position, verbose_name="Jefe Inmediato", null=False, blank=False)
    payroll_classification = models.CharField(max_length=1, choices=PAYROLLCLASSIFICATION_CHOICES, default=CORPORATIVA)
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Descripción de Puesto del Empleado"
        verbose_name = "Descripción de Puesto del Empleado"

    def __str__(self):
        return self.project.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.project.name + ": " + self.employee.name + " " + self.employee.first_last_name + " " + self.employee.second_last_name




class EmployeeFinancialData(models.Model):
    DEPOSITO='D'
    EFECTIVO='E'
    TRANSFERENCIA='T'
    PAYMENT_METHOD_CHOICES = (
        ('D', 'Deposito'),
        ('E', 'Efectivo'),
        ('T', 'Transferencia Interbancaria'),
    )

    BANK_CHOICES = (
        ('1', 'BANCOMER'),
        ('2', 'BANAMEX'),
        ('3', 'BANORTE'),
        ('4', 'SANTANDER'),
        ('5', 'HSBC'),
    )
    bank = models.CharField(max_length=1, choices=BANK_CHOICES)

    account_number = models.IntegerField(verbose_name='Número de Cuenta', null=False, default=0)
    CLABE = models.IntegerField(verbose_name='CLABE', null=False, default=0)
    monthly_salary = models.DecimalField(verbose_name='Salario Mensual', max_digits=20, decimal_places=2, null=True)
    daily_salary = models.DecimalField(verbose_name='Salario Diario', max_digits=20, decimal_places=2, null=True)
    aggregate_daily_salary = models.DecimalField(verbose_name='Salario Diario Acumulado', max_digits=20, decimal_places=2, null=True)
    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default=DEPOSITO,verbose_name='Forma de Pago')
    bank = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default=DEPOSITO,verbose_name='Forma de Pago')

    class Meta:
        verbose_name_plural = "Datos Financieros del Empleado"
        verbose_name = "Datos Financieros del Empleado"


class InfonavitData(models.Model):
    infonavit_credit_number = models.CharField(verbose_name="Número de Crédito", null=False, blank=False, max_length=30,)
    discount_type = models.CharField(verbose_name="Tipo de Descuento", null=False, blank=False, max_length=30,)
    discount_amount = models.CharField(verbose_name="Monto de Descuento", null=False, blank=False, max_length=30,)
    start_date = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    credit_term = models.CharField(verbose_name="Duración de Crédito", null=False, blank=False,max_length=200)
    comments = models.CharField(verbose_name="Observaciones", null=True, blank=True, max_length=500,)

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
    FIJA='F'
    VARIABLE='V'
    EARNINGDEDUCTIONSCATEGORY_CHOICES = (
        ('F', 'Fija'),
        ('V', 'Variable'),
    )

    DEDUCCION='D'
    PERCEPCION='P'
    EARNINGDEDUCTIONTYPE_CHOICES = (
        (DEDUCCION, 'Deducción'),
        (PERCEPCION, 'Percepción'),
    )

    SI='Y'
    NO='N'
    YNTYPE_CHOICES = (
        (SI, 'Si'),
        (NO, 'No'),
    )

    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30,)
    percent_taxable = models.IntegerField("Porcentaje Grabable", blank=False, null=False)
    sat_key = models.CharField(verbose_name="Clave SAT", null=False, blank=False, max_length=30,)
    law_type = models.CharField(verbose_name="Tipo de Ley", null=False, blank=False, max_length=30,)
    status = models.CharField(verbose_name="Estatus", null=False, blank=False, max_length=1,)
    accounting_account  = models.IntegerField("Cuenta Contable", blank=False, null=False)
    comments = models.CharField(verbose_name="Observaciones", null=False, blank=False, max_length=500,)
    type = models.CharField(max_length=1, choices=EARNINGDEDUCTIONTYPE_CHOICES,default=DEDUCCION)
    taxable = models.CharField(max_length=1, choices=YNTYPE_CHOICES,default=NO)
    category = models.CharField(max_length=1, choices=EARNINGDEDUCTIONSCATEGORY_CHOICES,default=FIJA)

    class Meta:
        verbose_name_plural = "Percepciones y Deducciones"
        verbose_name = "Percepciones y Deducciones"


    def __str__(self):
        return self.type + "-" + self.name


    def __unicode__(self):  # __unicode__ on Python 2
        return self.type + "-" + self.name


class EmployeeEarningsDeductions(models.Model):

    ammount = models.DecimalField(verbose_name="Monto", decimal_places=2, blank=False, null=False,
                                                   default=0, max_digits=20,
                                                   validators=[MinValueValidator(Decimal('0.0'))])
    date = models.DateField(verbose_name="Fecha", null=False,blank=False)

    # Foreign Keys.
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False, blank=False)
    concept = models.ForeignKey(EarningsDeductions, verbose_name="Concepto", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Deducciones y Percepciones por Empleado"
        verbose_name = "Deducciones y Percepciones por Empleado"




class PayrollType(models.Model):
    name = models.CharField(verbose_name="Tipo de Nómina", null=False, blank=False, max_length=30,)

    class Meta:
        verbose_name_plural = "Tipo de Nómina"
        verbose_name = "Tipos de Nómina"

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
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30,)
    month = models.IntegerField(verbose_name="Mes", max_length=2, choices=MONTH_CHOICES, default=JANUARY)
    year = models.IntegerField(verbose_name="Año", null=False, blank=False,default=2017,
        validators=[MaxValueValidator(9999), MinValueValidator(2017)])
    week = models.IntegerField(verbose_name="Semana", null=False, blank=False,default=1,
        validators=[MaxValueValidator(53), MinValueValidator(1)])
    start_period = models.DateField(verbose_name="Inicio de Periodo", null=False,blank=False)
    end_period = models.DateField(verbose_name="Fin de Periodo", null=False,blank=False)

    class Meta:
        verbose_name_plural = "Periodos de Nómina"
        verbose_name = "Periodos de Nómina"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name



class PayrollToProcess(models.Model):
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=30,)
    # Foreign Keys.
    payroll_type = models.ForeignKey(PayrollType, verbose_name="Tipo de Nómina", null=False, blank=False)

    class Meta:
        verbose_name_plural = "Nómina a Procesar"
        verbose_name = "Nómina a Procesar"

    def __str__(self):
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

class PayrollProcessed(models.Model):
    CORPORATIVA = 'C'
    PROYECTO = 'P'
    PAYROLLCLASSIFICATION_CHOICES = (
        (CORPORATIVA, 'Corporativa'),
        (PROYECTO, 'Proyecto'),
    )
    # Foreign Keys.
    payroll_period = models.ForeignKey(PayrollPeriod, verbose_name="Periodo", null=False, blank=False)
    payroll_to_process = models.ForeignKey(PayrollToProcess, verbose_name="Nómina a Procesar", null=False, blank=False)
    payroll_classification = models.CharField(max_length=1, choices=PAYROLLCLASSIFICATION_CHOICES, default=CORPORATIVA)

    class Meta:
        verbose_name_plural = "Nómina Procesada"
        verbose_name = "Nómina Procesada"


class PayrollReceiptProcessed(models.Model):
    SI = 'Y'
    NO = 'N'
    YNTYPE_CHOICES = (
        (SI, 'Si'),
        (NO, 'No'),
    )

    worked_days = models.DecimalField(verbose_name="Días Trabajados", null=False, blank=False, max_digits=20, decimal_places=2)
    total_perceptions = models.DecimalField(verbose_name="Total de Percepciones", null=False, blank=False, max_digits=20, decimal_places=2)
    total_deductions = models.DecimalField(verbose_name="Total de Deducciones", null=False, blank=False, max_digits=20, decimal_places=2)
    total_payroll = models.DecimalField(verbose_name="Total Neto", null=False, blank=False, max_digits=20, decimal_places=2)
    taxed = models.DecimalField(verbose_name="Grabado", null=False, blank=False, max_digits=20, decimal_places=2)
    exempt = models.DecimalField(verbose_name="Excento", null=False, blank=False, max_digits=20, decimal_places=2)
    daily_salry = models.DecimalField(verbose_name="Salario Diario", null=False, blank=False, max_digits=20, decimal_places=2)
    total_withholdings = models.DecimalField(verbose_name="Total de Deducciones", null=False, blank=False, max_digits=20, decimal_places=2)
    total_discounts = models.DecimalField(verbose_name="Total de Descuentos", null=False, blank=False, max_digits=20, decimal_places=2)
    printed_receipt = models.CharField(max_length=1, choices=YNTYPE_CHOICES,default=SI)
    stamp_version = models.DecimalField(verbose_name="Versión de Timbrado", null=False, blank=False, max_digits=20, decimal_places=2)
    stamp_UUID =  models.CharField(verbose_name="UUID de Timbrado", null=False, blank=False, max_length=500)
    stamp_date = models.DateTimeField(verbose_name="Fecha de Timbrado")
    stamp_CFDI =  models.CharField(verbose_name="CFDI Timbrado", null=False, blank=False, max_length=500)
    sat_certificate =  models.CharField(verbose_name="Certificado del SAT", null=False, blank=False, max_length=500)
    stamp_sat =  models.CharField(verbose_name="Timbrado del SAT", null=False, blank=False, max_length=500)
    stamp_xml =  models.CharField(verbose_name="XML del Timbrado", null=False, blank=False, max_length=500)
    stamp_serie_id = models.CharField(verbose_name="Serie ID  de Timbrado", null=False, blank=False, max_length=500)
    payment_date = models.DateField(verbose_name="Fecha de Pago")

    #foreign

    payroll_processed = models.ForeignKey(PayrollProcessed, verbose_name="Nómina Procesada", null=False,
                                              blank=False)
    employee = models.ForeignKey(Employee, verbose_name="Empleado", null=False,
                       blank=False)

    class Meta:
       verbose_name_plural = "Recibo de Nómina Procesada"
       verbose_name = "Recibo de Nómina Procesada"


class PayrollProcessedDetail(models.Model):
   # Foreign Keys.
   payroll_receip_processed = models.ForeignKey(PayrollReceiptProcessed, verbose_name="Recibo de Nómina Procesado", null=False, blank=False)
   earnings_deductions = models.ForeignKey(EarningsDeductions, verbose_name="Concepto", null=False, blank=False)
   total = models.DecimalField( verbose_name="Total", null=False, blank=False, max_digits=20, decimal_places=2)
   taxed = models.DecimalField(verbose_name="Grabable", null=False, blank=False, max_digits=20, decimal_places=2)
   exempt = models.DecimalField(verbose_name="Excento", null=False, blank=False, max_digits=20, decimal_places=2)

   class Meta:
       verbose_name_plural = "Detalle de Nómina Procesada"
       verbose_name = "Detalle de Nómina Procesada"


class PayrollGroup(models.Model):
    name = models.CharField(verbose_name="Nombre", null=False, blank=False, max_length=100, )

    class Meta:
        verbose_name_plural = "Grupo de Nómina"
        verbose_name = "Grupo de Nómina"

    def __str__(self):
        return str(self.name)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.name)

class JobInstance(models.Model):
    # Job Description ***
    job_profile = models.ForeignKey(JobProfile, verbose_name='Perfil de Empleado', null=False, blank=False)
    parent_job_instance = models.ForeignKey('self', verbose_name='Jefe Inmediato', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vacante de Puesto"
        verbose_name = "Vacante de Empleos"

    def __str__(self):
        return str(self.id)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.id)