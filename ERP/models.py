# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.forms.models import model_to_dict
from users.models import ERPUser

from django.db import models
from Logs.controller import Logs
from smart_selects.db_fields import ChainedManyToManyField



# Create your models here.

# *********************************************************************
#                                Estado                               *
# *********************************************************************

class Pais(models.Model):
    nombrePais = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['pais'] = self.estado.nombrePais
        return ans

    def __str__(self):
        return self.nombrePais

    def __unicode__(self):
        return self.nombrePais


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    pais = models.ForeignKey(Pais, null=False, blank=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class Municipio(models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['estado'] = self.estado.nombreEstado
        return ans

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio


class TipoConstruccion(models.Model):
    nombreTipoConstruccion = models.CharField(max_length=200)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['tipoconstruccion'] = self.nombreTipoConstruccion
        return ans

    def __str__(self):
        return self.nombreTipoConstruccion

    def __unicode__(self):
        return self.nombreTipoConstruccion

class Departamento(models.Model):
        nombreDepartamento = models.TextField(verbose_name='Departamento', max_length=120, null=False, blank=False,
                                              editable=True)
        descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                       editable=True)

        class Meta:
            verbose_name_plural = 'Departamento'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['nombreDepartamento'] = str(self.nombreDepartamento)
            return ans

        def __str__(self):
            return self.nombreDepartamento

        def save(self, *args, **kwargs):
            canSave = True

            if canSave:
                Logs.log("Saving new project", "Te")
                super(Departamento, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class Area(models.Model):
        nombreArea = models.TextField(verbose_name='Área', max_length=120, null=False, blank=False, editable=True)
        descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                       editable=True)
        departamento = models.ForeignKey(Departamento, verbose_name="Departamento", null=False, blank=False)

        class Meta:
            verbose_name_plural = 'Area'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['nombreArea'] = str(self.nombreArea)
            ans['departamento'] = str(self.departamento.nombreDepartamento)
            return ans

        def __str__(self):
            return self.nombreArea

        def save(self, *args, **kwargs):
            canSave = True

            if canSave:
                Logs.log("Saving new Area", "Te")
                super(Area, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class Puesto(models.Model):
        nombrePuesto = models.TextField(verbose_name='Puesto', max_length=120, null=False, blank=False, editable=True)
        descripcion = models.TextField(verbose_name='Descripción', max_length=250, null=False, blank=False,
                                       editable=True)
        area = models.ForeignKey(Area, verbose_name='Área', null=False, blank=False)

        class Meta:
            verbose_name_plural = 'Puesto'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['nombrePuesto'] = str(self.nombrePuesto)
            ans['area'] = str(self.area.nombreArea)
            return ans

        def __str__(self):
            return self.nombre_puesto

        def save(self, *args, **kwargs):
            canSave = True

            if canSave:
                Logs.log("Saving new Puesto", "Te")
                super(Puesto, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class ModalidadContrato(models.Model):
        modalidadContrato = models.CharField(verbose_name='Contrato', max_length=250, null=False, blank=False,
                                             editable=True)
        duracionContrato = models.CharField(verbose_name='Duración de Contrato', max_length=20, null=False, blank=False,
                                            editable=True)

        class Meta:
            verbose_name_plural = 'ModalidadContrato'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['modalidadContrato'] = str(self.modalidadContrato)
            ans['duracionContrato'] = str(self.duracionContrato)
            return ans

        def __str__(self):
            return self.modalidadContrato

        def save(self, *args, **kwargs):
            canSave = True

            if canSave:
                Logs.log("Saving new ModalidadContrato", "Te")
                super(ModalidadContrato, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class Empleado(models.Model):
    nombreEmpleado = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
    calle = models.TextField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
    numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
    colonia = models.TextField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
    municipio = models.ForeignKey(Municipio, verbose_name='Municipio', null=False, blank=False)
    estado = models.ForeignKey(Estado,verbose_name='Estado', null=False, blank=False)
    pais = models.ForeignKey(Pais, verbose_name="pais", null=False, blank=False)
    cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
    rfc = models.TextField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)
    fecha_contrato = models.DateTimeField(verbose_name='Fecha de Contrato', auto_now_add=True)
    modalidad_contrato = models.ForeignKey(ModalidadContrato, verbose_name='Contrato', null=False, blank=False)
    puesto = models.ForeignKey(Puesto, verbose_name='Puesto', null=False, blank=False)
    sueldo_inicial = models.DecimalField (verbose_name='sueldo_inicial', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    sueldo_actual = models.DecimalField(verbose_name='sueldo_actual', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    antiguedad = models.CharField(verbose_name='Antiguedad', max_length=50, null=False, blank=False, editable=True)

    class Meta:
        verbose_name_plural = 'Empleado'


    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombreEmpleado'] = str(self.nombreEmpleado)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombre_estado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['rfc'] = str(self.rfc)
        ans['fecha_contrato'] = str(self.fecha_contrato)
        ans['modalidad_contrato'] = str(self.modalidad_contrato.modalidadContrato)
        ans['puesto'] = str(self.puesto.nombrePuesto)
        ans['sueldo_inicial'] = str(self.sueldo_inicial)
        ans['sueldo_actual'] = str(self.sueldo_actual)
        ans['antiguedad'] = str(self.antiguedad)
        return ans


    def __str__(self):
        return self.nombreEmpleado


    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Empleado", "Te")
            super(Empleado, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

class Contratista(models.Model):
        nombreContratista = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
        calle = models.CharField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
        numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
        colonia = models.CharField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
        municipio = models.ForeignKey(Municipio, verbose_name='Municipio', null=False, blank=False)
        estado = models.ForeignKey(Estado,verbose_name='Estado', null=False, blank=False)
        pais = models.ForeignKey(Pais, verbose_name="pais", null=False, blank=False)
        cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
        rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)

        class Meta:
            verbose_name_plural = 'Contratista'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['nombreContratista'] = str(self.nombreContratista)
            ans['calle'] = str(self.calle)
            ans['numero'] = str(self.numero)
            ans['colonia'] = str(self.colonia)
            ans['municipio'] = str(self.municipio.nombreMunicipio)
            ans['estado'] = str(self.estado.nombre_estado)
            ans['pais'] = str(self.pais.nombrePais)
            ans['cp'] = str(self.cp)
            ans['rfc'] = str(self.rfc)

            return ans


        def __str__(self):
            return self.nombreContratista

            def save(self, *args, **kwargs):
                canSave = True

            if canSave:
                Logs.log("Saving new Contratista", "Te")
                super(Contratista, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class Empresa(models.Model):
        nombreEmpresa = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False, editable=True)
        calle = models.CharField(verbose_name='Calle', max_length=50, null=False, blank=False, editable=True)
        numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False, editable=True)
        colonia = models.CharField(verbose_name='Colonia', max_length=50, null=False, blank=False, editable=True)
        municipio = models.ForeignKey(Municipio, verbose_name='Municipio', null=False, blank=False)
        estado = models.ForeignKey(Estado, verbose_name='Estado', null=False, blank=False)
        pais = models.ForeignKey(Pais, verbose_name='Pais', null=False, blank=False)
        cp = models.CharField(verbose_name='C.P.', max_length=20, null=False, blank=False, editable=True)
        telefono = models.CharField(verbose_name='Teléfono', max_length=30, null=True, blank=True, editable=True)
        rfc = models.CharField(verbose_name='RFC', max_length=20, null=False, blank=False, editable=True)

        class Meta:
            verbose_name_plural = 'Empresa'

        def to_serializable_dict(self):
            ans = model_to_dict(self)
            ans['id'] = str(self.id)
            ans['nombreEmpresa'] = str(self.nombreEmpresa)
            ans['calle'] = str(self.calle)
            ans['numero'] = str(self.numero)
            ans['colonia'] = str(self.colonia)
            ans['municipio'] = str(self.municipio.nombreMunicipio)
            ans['estado'] = str(self.estado.nombre_estado)
            ans['pais'] = str(self.pais.nombrePais)
            ans['cp'] = str(self.cp)
            ans['telefono'] = str(self.telefono)
            ans['rfc'] = str(self.rfc)

            return ans

        def __str__(self):
            return self.nombreEmpresa

        def save(self, *args, **kwargs):
            canSave = True

            if canSave:
                Logs.log("Saving new Empresa", "Te")
                super(Empresa, self).save(*args, **kwargs)
            else:
                Logs.log("Couldn't save")

class Contrato(models.Model):
    no_licitacion = models.CharField(verbose_name='Número de Licitación', max_length=50, null=False, blank=False, editable=True)
    modalidad_contrato = models.ForeignKey(ModalidadContrato, verbose_name='Modalidad Contrato', null=False, blank=False)
    dependencia = models.CharField(verbose_name='dependencia', max_length=50, null=False, blank=False, editable=True)
    codigo_obra = models.CharField(verbose_name='Código de Obra', max_length=50, null=False, blank=False, editable=True)
    contratista = models.ForeignKey(Contratista, verbose_name='Contratista', null=False, blank=False)
    objeto_contrato = models.TextField(verbose_name='Objeto de Contrato', max_length=250, null=False, blank=False, editable=True)
    fecha_firma = models.DateTimeField(verbose_name='Fecha de Firma', editable=True)
    dias_pactados = models.CharField(verbose_name='Días Pactados', max_length=50, null=False, blank=False, editable=True)
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio', editable=True)
    fecha_termino = models.DateTimeField(verbose_name='Fecha de Termino', editable=True)
    lugar_ejecucion = models.TextField(verbose_name='Lugar de Ejecución', max_length=250, null=False, blank=False, editable=True)
    monto_contrato = models.DecimalField(verbose_name='Monto de Contrato', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    monto_contrato_iva = models.DecimalField(verbose_name='Monto de Contrato con IVA', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    pago_inicial = models.DecimalField(verbose_name='Pago Inicial', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    pago_final = models.DecimalField(verbose_name='Pago Final', decimal_places=2, blank=False, null=False, default=0, max_digits=20)
    observaciones = models.TextField(verbose_name='Observaciones', max_length=500, null=False, blank=False, editable=True)

    #class Meta:
    #    verbose_name_plural = 'Contrato'


    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['no_licitacion'] = str(self.nombreContratista)
        ans['modalidad_contrato'] = str(self.modalidad_contrato.modalidadContrato)
        ans['dependencia'] = str(self.dependencia)
        ans['codigo_obra'] = str(self.codigo_obra)
        ans['contratista'] = str(self.contratista.nombreContratista)
        ans['objeto_contrato'] = str(self.objeto_contrato)
        ans['fecha_firma'] = str(self.fecha_firma)
        ans['dias_pactados'] = str(self.dias_pactados)
        ans['fecha_inicio'] = str(self.fecha_inicio)
        ans['fecha_termino'] = str(self.fecha_termino)
        ans['lugar_ejecucion'] = str(self.lugar_ejecucion)
        ans['monto_contrato'] = str(self.monto_contrato)
        ans['monto_contrato_iva'] = str(self.monto_contrato_iva)
        ans['pago_inicial'] = str(self.pago_inicial)
        ans['pago_final'] = str(self.pago_final)
        ans['observaciones'] = str(self.observaciones)

        return ans

        def __str__(self):
            return self.observaciones

        #def save(self, *args, **kwargs):
            #    canSave = True

            #if canSave:
            #    Logs.log("Saving new Contrato", "Te")
            #    super(Contrato, self).save(*args, **kwargs)
            #else:
            #    Logs.log("Couldn't save")


# Propietario
class Propietario(models.Model):
    nombrePropietario = models.CharField(verbose_name="propietario", max_length=200, null=False, blank=False)
    calle = models.CharField(verbose_name="calle", max_length=200, null=False, blank=False)
    numero = models.CharField(verbose_name="numero", max_length=8, null=False, blank=False)
    colonia = models.CharField(verbose_name="Colonia", max_length=200, null=False, blank=False)
    municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    pais = models.ForeignKey(Pais, verbose_name="pais", null=False, blank=False)
    cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    telefono1 = models.CharField(verbose_name="Telefono 1", max_length=20, null=True, blank=True)
    telefono2 = models.CharField(verbose_name="Telefono 2", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="e mail", max_length=100, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name="empresa", null=False, blank=False)


    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombrePropietario'] = str(self.nombrePropietario)
        ans['calle'] = str(self.calle)
        ans['numero'] = str(self.numero)
        ans['colonia'] = str(self.colonia)
        ans['municipio'] = str(self.municipio.nombreMunicipio)
        ans['estado'] = str(self.estado.nombre_estado)
        ans['pais'] = str(self.pais.nombrePais)
        ans['cp'] = str(self.cp)
        ans['telefono1'] = str(self.telefono1)
        ans['telefono_2'] = str(self.telefono2)
        ans['email'] = str(self.email)
        ans['empresa'] = str(self.empresa.nombreEmpresa)
        return ans

    def __str__(self):
        return self.nombrePropietario

    def save(self, *args, **kwargs):
        canSave = True

        if canSave:
            Logs.log("Saving new Propietario", "Te")
            super(Propietario, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

def content_file_documento_fuente(instance, filename):
    return '/'.join(['documentosFuente', instance.proyecto.key, filename])


class DocumentoFuente(models.Model):
    descripcion = models.CharField(max_length=50, )
    documento = models.FileField(upload_to=content_file_documento_fuente, )
    tipoProyectoDetalle = models.ForeignKey('TipoProyectoDetalle', )

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion

    def delete(self, using=None):
        self.documento.delete()
        super(DocumentoFuente, self).delete(using)

# ProgramaVivienda
class TipoProyectoDetalle(models.Model):
    proyecto = models.ForeignKey('Project', verbose_name="proyecto", null=True, blank=True)
    #programaVivienda = models.ForeignKey(ProgramaVivienda, related_name="proyecto_programaVivienda",
    #                                      null=True,
    #                                      blank=True)
    NombreTipoProyecto = models.CharField(verbose_name="tipo Proyecto", max_length=8, null=False, blank=False)
    numero = models.DecimalField(verbose_name='número', decimal_places=2, blank=False,
                                          null=False,
                                          default=0, max_digits=20)
    m2terreno = models.DecimalField(verbose_name='terreno (m2)', decimal_places=2, blank=False, null=False,
                                    default=0,
                                    max_digits=20)
    documento = models.FileField(blank=True, null=True,upload_to=content_file_documento_fuente, )

    class Meta:
        unique_together = [("proyecto","NombreTipoProyecto")]

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans




# proyectos
class Project(models.Model):
    key = models.CharField(verbose_name="Clave del Proyecto", max_length=255, null=False, blank=False, unique=True)
    contrato = models.ForeignKey(Contrato, verbose_name="contrato", null=False, blank=False)
    propietario = models.ForeignKey(Propietario, verbose_name="propietario", null=False, blank=False)
    nombreProyecto = models.CharField(verbose_name="nombre del proyecto", max_length=100, null=False, blank=False)
    fecha_inicial = models.DateTimeField(default=None, null=False)
    fecha_final = models.DateTimeField(default=None, null=False)
    tipo_construccion = models.ForeignKey(TipoConstruccion, verbose_name="tipo de construcción", null=False,
                                          blank=False)
    ubicacion_calle = models.CharField(verbose_name="calle", max_length=200, null=False, blank=False)
    ubicacion_numero = models.CharField(verbose_name="numero", max_length=8, null=False, blank=False)
    ubicacion_colonia = models.CharField(verbose_name="numero", max_length=200, null=False, blank=False)
    ubicacion_municipio = models.ForeignKey(Municipio, verbose_name="municipio", null=False, blank=False)
    ubicacion_estado = models.ForeignKey(Estado, verbose_name="estado", null=False, blank=False)
    ubicacion_cp = models.IntegerField(verbose_name="C.P.", null=False, blank=False)
    ubicacion_pais = models.ForeignKey(Pais, verbose_name="país", null=False, blank=False)
    area_superficie_escritura = models.DecimalField(verbose_name='superficie escritura', decimal_places=2, blank=False,
                                                    null=False, default=0, max_digits=20)
    area_superficie_levantamiento = models.DecimalField(verbose_name='superficie levantamiento', decimal_places=2,
                                                        blank=False, null=False, default=0, max_digits=20)
    
    estadolegal_documento_propiedad = models.CharField(verbose_name="Documento de propiedad", max_length=200, null=True, blank=True)
    documento_propiedad = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    estadolegal_gravamen = models.CharField(verbose_name="gravamen", max_length=200, null=True, blank=True)
    documento_gravamen = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    estadolegal_predial = models.CharField(verbose_name="predial", max_length=200, null=True, blank=True)
    documento_predial = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    estadolegal_agua = models.CharField(verbose_name="agua", max_length=200, null=True, blank=True)
    documento_agua = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    restrccion_vial = models.CharField(verbose_name="vial", max_length=200, null=True, blank=True)
    restrccion_cna = models.CharField(verbose_name="cna", max_length=200, null=True, blank=True)
    restrccion_cfe = models.CharField(verbose_name="cfe", max_length=200, null=True, blank=True)
    restrccion_pemex = models.CharField(verbose_name="pemex", max_length=200, null=True, blank=True)
    restrccion_inha = models.CharField(verbose_name="inha", max_length=200, null=True, blank=True)
    restrccion_otros = models.CharField(verbose_name="otros", max_length=200, null=True, blank=True)
    restrccion_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    usosuelo_pmdu = models.CharField(verbose_name="pmdu", max_length=200, null=True, blank=True)
    usosuelo_densidad = models.CharField(verbose_name="densidad", max_length=200, null=True, blank=True)
    usosuelo_loteminimo = models.DecimalField(verbose_name='lote mínimo', decimal_places=2, blank=True, null=True,
                                              default=0, max_digits=20)
    usosuelo_m2construccion = models.DecimalField(verbose_name='m2 de construcción', decimal_places=2, blank=True,
                                                  null=True, default=0, max_digits=20)
    usosuelo_arealibre = models.CharField(verbose_name="area libre", max_length=200, null=True, blank=True)
    usosuelo_altura = models.CharField(verbose_name="altura", max_length=200, null=True, blank=True)
    usosuelo_densidadrequerida = models.CharField(verbose_name="densidad requerida", max_length=200, null=True,
                                                  blank=True)
    hidraulica_fuente = models.CharField(verbose_name="fuente", max_length=200, null=True, blank=True)
    hidraulica_distancia = models.CharField(verbose_name="distacia", max_length=200, null=True, blank=True)
    hidraulica_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    hidraulica_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    sanitaria_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    sanitaria_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    sanitaria_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    sanitaria_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    pluvial_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    pluvial_responsable = models.CharField(verbose_name="responsable", max_length=200, null=True, blank=True)
    pluvial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    pluvial_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    vial_viaacceso = models.CharField(verbose_name="vias de acceso", max_length=200, null=True, blank=True)
    vial_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    vial_carriles = models.CharField(verbose_name="carriles", max_length=200, null=True, blank=True)
    vial_seccion = models.CharField(verbose_name="seccion", max_length=200, null=True, blank=True)
    vial_tipopavimento = models.CharField(verbose_name="tipo de pavimento", max_length=200, null=True, blank=True)
    vial_estadoconstruccion = models.CharField(verbose_name="estado de construcción", max_length=200, null=True,
                                               blank=True)
    vial_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    vial_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    electricidad_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    electricidad_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    electricidad_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    electricidad_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    alumbradopublico_tipo = models.CharField(verbose_name="tipo", max_length=200, null=True, blank=True)
    alumbradopublico_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    alumbradopublico_observaciones = models.CharField(verbose_name="dobservaciones", max_length=200, null=True,
                                                      blank=True)
    alumbradopublico_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    telefonia_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    telefonia_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    telefonia_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    tvcable_distancia = models.CharField(verbose_name="distancia", max_length=200, null=True, blank=True)
    tvcable_observaciones = models.CharField(verbose_name="observaciones", max_length=200, null=True, blank=True)
    equipamiento_a100 = models.CharField(verbose_name="a 100", max_length=200, null=True, blank=True)
    equipamiento_a200 = models.CharField(verbose_name="a 200", max_length=200, null=True, blank=True)
    equipamiento_a500 = models.CharField(verbose_name="da 500", max_length=200, null=True, blank=True)
    equipamiento_regional = models.CharField(verbose_name="regional", max_length=200, null=True, blank=True)
    costo_predio = models.DecimalField(verbose_name='costo del predio', decimal_places=2, blank=True, null=True,
                                       default=0, max_digits=20)
    costo_m2 = models.DecimalField(verbose_name='m2', decimal_places=2, blank=True, null=True, default=0,
                                   max_digits=20)
    costo_escrituras = models.DecimalField(verbose_name='escrituras m2', decimal_places=2, blank=True, null=True,
                                           default=0, max_digits=20)
    costo_levantamiento = models.DecimalField(verbose_name='levantamiento m2', decimal_places=2, blank=True,
                                              null=True, default=0, max_digits=20)
    estudiomercado_demanda = models.CharField(verbose_name="Demanda", max_length=200, null=True, blank=True)
    estudiomercado_oferta = models.CharField(verbose_name="Oferta", max_length=200, null=True, blank=True)
    estudiomercado_conclusiones = models.CharField(verbose_name="Conlusiones", max_length=200, null=True, blank=True)
    estudiomercado_recomendaciones = models.CharField(verbose_name="Recomendaciones", max_length=200, null=True, blank=True)
    definicionproyecto_alternativa = models.CharField(verbose_name="Alernativa", max_length=200, null=True, blank=True)
    definicionproyecto_tamano = models.CharField(verbose_name="Tamaño", max_length=200, null=True, blank=True)
    definicionproyecto_programa = models.CharField(verbose_name="Programa", max_length=200, null=True, blank=True)

    programayarea_areaprivativa = models.DecimalField(verbose_name='area privada', decimal_places=2, blank=True,
                                                      null=True, default=0, max_digits=20)
    programayarea_caseta = models.DecimalField(verbose_name='caseta', decimal_places=2, blank=True, null=True,
                                               default=0, max_digits=20)
    programayarea_jardin = models.DecimalField(verbose_name='jardín', decimal_places=2, blank=True, null=True,
                                               default=0, max_digits=20)
    programayarea_vialidad = models.DecimalField(verbose_name='vialidad', decimal_places=2, blank=True, null=True,
                                                 default=0, max_digits=20)
    programayarea_areaverde = models.DecimalField(verbose_name='área verde', decimal_places=2, blank=True, null=True,
                                                  default=0, max_digits=20)
    programayarea_estacionamientovisita = models.DecimalField(verbose_name='estacionamiento visita', decimal_places=2,
                                                              blank=True, null=True, default=0, max_digits=20)
    programayarea_afectacion = models.DecimalField(verbose_name='afectación', decimal_places=2, blank=True, null=True,
                                                   default=0, max_digits=20)
    programayarea_documento = models.FileField(blank=True, null=True, upload_to=content_file_documento_fuente, )
    #tipoProyectoDetalle = models.ManyToManyField(TipoProyectoDetalle,null=True,blank=True, )

    class Meta:
        verbose_name_plural = 'Proyectos'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['key'] = str(self.key)
        ans['contrato'] = str(self.contrato.objeto_contrato)
        ans['nombreProyecto'] = str(self.nombreProyecto)
        ans['propietario'] = str(self.propietario.nombrePropietario)

        return ans

    def __str__(self):
        return self.nombreProyecto

    def save(self, *args, **kwargs):
        canSave = True

        if self.fecha_final is not None and self.fecha_inicial >= self.fecha_final:
            Logs.log("The start date is greater than the end date")
            canSave = False

        if canSave:
            Logs.log("Saving new project", "Te")
            super(Project, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")

'''
    Model for the Line Items.
'''


class LineItem(models.Model):
    project = models.ForeignKey(Project, verbose_name="Proyecto", null=False, blank=False)
    parent_line_item = models.ForeignKey('self', verbose_name="Partida Padre", null=False, blank=True)
    description = models.CharField(verbose_name="Descripción", max_length=255, null=False, blank=False, unique=True)
    key = models.CharField(verbose_name="Clave", max_length=8, null=False, blank=True, unique=True, default="")

    class Meta:
        verbose_name_plural = 'Partidas'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['project'] = str(self.project.name)
        ans['parentLineItem'] = str(self.parent_line_item)
        ans['description'] = str(self.description)
        return ans

    def __str__(self):
        return self.description

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description



'''
    Model for the units.
'''


class Unit(models.Model):
    name = models.CharField(verbose_name="Nombre de la Unidad", max_length=255, null=False, blank=False, unique=True)
    abbreviation = models.CharField(verbose_name="Abreviación", max_length=16, null=False, blank=False, unique=True)

    CONTINUOUS = "C"
    DISCRETE = "D"
    QUANTIFICATION_CHOICES = (
        (CONTINUOUS, 'Continuous'),
        (DISCRETE, 'Discrete'),
    )
    quantification = models.CharField(max_length=1, choices=QUANTIFICATION_CHOICES, default=CONTINUOUS)

    class Meta:
        verbose_name_plural = 'Unidades'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['name'] = str(self.name)
        ans['abbreviation'] = str(self.abbreviation)
        return ans

    def __str__(self):
        return self.abbreviation + self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


'''
    Model for the concepts.
'''


class Concept_Input(models.Model):
    ARCHIVED = "A"
    CURRENT = "C"
    STATUS_CHOICES = (
        (ARCHIVED, 'Archivado'),
        (CURRENT, 'Actual'),
    )

    CONCEPT = "C"
    INPUT = "I"
    TYPE_CHOICES = (
        (CONCEPT, 'Concepto'),
        (INPUT, 'Insumo'),
    )

    line_item = models.ForeignKey(LineItem, verbose_name="Partida", null=False, blank=False)
    unit = models.ForeignKey(Unit, verbose_name="Unidad", null=False, blank=False)
    key = models.CharField(verbose_name="Clave", max_length=32, null=False, blank=False, unique=True, editable=True)
    description = models.TextField(verbose_name="Descripción", max_length=4096, null=False, blank=False, editable=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ARCHIVED)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=CONCEPT)
    quantity = models.DecimalField(verbose_name='Cantidad', decimal_places=2, blank=False, null=False, default=0,
                                   max_digits=20)
    unit_price = models.DecimalField(verbose_name='Precio Unitario', decimal_places=2, blank=False, null=False,
                                     default=0, max_digits=20)

    class Meta:
        verbose_name_plural = 'Conceptos'
        verbose_name = 'Concepto'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['unit'] = str(self.unit.name)
        ans['status'] = str(self.status)
        ans['quantity'] = str(self.quantity)
        ans['unitPrice'] = str(self.unitPrice)
        return ans

    def __str__(self):
        return self.master.description

    def save(self, *args, **kwargs):
        canSave = True

        if self.end_date is not None and self.start_date >= self.end_date:
            Logs.log("The start date is greater than the end date")
            canSave = False

        if canSave:
            Logs.log("Saving new concept", "Te")
            super(Concept_Input, self).save(*args, **kwargs)
        else:
            Logs.log("Couldn't save")


'''
    Model for the Estimates.
'''


class Estimate(models.Model):
    concept_input = models.ForeignKey(Concept_Input, verbose_name="Concepto", null=True, blank=False, default=None)
    start_date = models.DateTimeField(default=None, null=True, verbose_name="Fecha de inicio")
    end_date = models.DateTimeField(default=None, null=True , verbose_name="Fecha de fin")
    period = models.DateTimeField(default=None, null=True, verbose_name="Periodo")

    class Meta:
        verbose_name_plural = 'Estimaciones'


'''
    Model for the Progress Estimates.
'''


def generator_file_storage(instance, filename):
    project_key = instance.proyecto.key
    line_item_key = instance.estimate.concept_input.line_item.key
    concept_key = instance.estimate.concept_input.key
    estimate_id = instance.estimate.id
    progress_estimate_key = instance.key

    return '/'.join(['documentosFuente',project_key, line_item_key, concept_key, estimate_id, progress_estimate_key, filename])

class ProgressEstimate(models.Model):
    estimate = models.ForeignKey(Estimate, verbose_name="Estimación", null=False, blank=False)
    key = models.CharField(verbose_name="Clave de la Estimación", max_length=8, null=False, blank=False)
    progress = models.DecimalField(verbose_name='Progreso', decimal_places=2, blank=False, null=False, default=0,
                                   max_digits=5)
    amount = models.DecimalField(verbose_name='Cantidad', decimal_places=1, blank=False, null=False, default=0,
                                 max_digits=4)
    generator_amount = models.DecimalField(verbose_name='Cantidad del Generador', decimal_places=2, blank=False, null=False, default=0,
                                   max_digits=20)
    generator_file = models.FileField(unique=True, upload_to=content_file_documento_fuente, null=True, default=None)
    RETAINER = "R"
    PROGRESS = "P"
    ESTIMATE = "E"
    TYPE_CHOICES = (
        (RETAINER, 'Adelanto'),
        (PROGRESS, 'Avance'),
        (ESTIMATE, 'Estimado'),
    )


    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=PROGRESS)

    class Meta:
        verbose_name_plural = 'Avances'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['key'] = str(self.key)
        ans['progress'] = str(self.progress)
        ans['amount'] = str(self.amount)
        ans['type'] = str(self.type)
        return ans

    def __str__(self):
        return self.estimate.concept_master.description + " - " + str(self.estimate.period) + " - " + self.key


'''
    Model for handling the progress estimate log.
'''

class ProgressEstimateLog(models.Model):
    progress_estimate = models.ForeignKey(ProgressEstimate, verbose_name="Estimación", null=False, blank=False)
    user = models.ForeignKey(ERPUser, verbose_name="Usuario", null=False, blank=False)
    description = models.CharField(verbose_name="Descripción", max_length=512, null=False, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=None, null=True, verbose_name="Fecha")

    class Meta:
        verbose_name_plural = 'Bitácoras de Estimaciones'


    def to_serializable_dict(self):
        answer = model_to_dict(self)
        answer['date'] = str(self.date)
        answer['register_date'] = str(self.register_date)
        return answer


    def __unicode__(self):  # __unicode__ on Python 2
        return self.description



'''
    Model for the Log File.
'''


class LogFile(models.Model):
    progress_estimate_log = models.ForeignKey(ProgressEstimateLog, verbose_name="Bitácora de Estimación", null=False,
                                              blank=False)
    file = models.FileField(verbose_name="Archivo", max_length=1024, null=True, blank=True)
    mime = models.CharField(verbose_name="MIME", max_length=128, null=False, blank=False)

    def to_serializable_dict(self):
        answer = model_to_dict(self)
        answer['file'] = str(self.file)
        return answer


