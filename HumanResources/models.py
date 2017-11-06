# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Libraries.
from django.db import models
from django.utils.timezone import now

# Third Party Libraries
from smart_selects.db_fields import ChainedForeignKey

# Importing model from other apps.
from ERP.models import Pais, Estado, Municipio

# Create your models here.




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
    driving_license_expiry_date = models.DateField(null=False, blank=True, verbose_name="Fecha de Expiración de la Licencia de Conducir")

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
    return '/'.join(['human_resources', 'employee_documents', 'education',instance.current_education.employee.employee_key, filename])


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
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description



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

