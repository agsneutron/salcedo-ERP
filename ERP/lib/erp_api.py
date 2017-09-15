# coding=utf-8
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.db.models import Q

# Custom classes
from ERP.lib.utilities import Utilities

# Model imports.
from ERP.models import *


#
class LogFilesForProgressEstimateLogEndpoint(ListView):
    ''' Endpoit to return the Log Files that belong to a Progress Estimate Log.
    '''

    def post(self, request, *args, **kwargs):
        pel_id = request.POST.get('pel_id')  # Reading the Progress Estimate Log Id to filter by.
        print "Received Id: " + str(pel_id)
        log_files = LogFile.objects.filter(Q(progress_estimate_log__id=pel_id))  # Filtering the log files.

        json_files = Utilities.query_set_to_json_string(log_files)
        return HttpResponse(json_files, 'application/json', )


class ConceptInputsForLineItemAndType(ListView):
    '''
        Endpoint to return the concepts or inputs filtered by a line_item and a type [concept|input]
    '''

    def get(self, request, *args, **kwargs):
        line_item_id = request.GET.get('line_item')  # Getting the type fpr the request.
        type = request.GET.get('type')  # Getting the type fpr the request.

        qs = Concept_Input.objects.filter(Q(type=type) & Q(line_item=line_item_id)).values('id', 'description')
        cleaned_qs = Utilities.clean_generic_queryset(qs)

        return HttpResponse(cleaned_qs, 'application/json', )


class GetProjectInfo(ListView):
    '''
      Endpoint to return a certain project information.
    '''

    def get(self, request, *args, **kwargs):
        project_id = request.GET.get('project')  # Getting the type fpr the request.

        project = Project.objects.filter(id=project_id)[0]
        response = {
            "id": project.id,
            "key": project.key,
            "propietario": project.propietario.nombrePropietario,
            "nombreProyecto": project.nombreProyecto,
            "fecha_inicial": str(project.fecha_inicial),
            "fecha_final": str(project.fecha_final),
            "tipo_construccion": project.tipo_construccion.nombreTipoConstruccion,
            "ubicacion_calle": project.ubicacion_calle,
            "ubicacion_numero": project.ubicacion_numero,
            "ubicacion_colonia": project.ubicacion_colonia,
            "ubicacion_pais": project.ubicacion_pais.nombrePais,
            "ubicacion_estado": project.ubicacion_estado.nombreEstado,
            "ubicacion_municipio": project.ubicacion_municipio.nombreMunicipio,
            "ubicacion_cp": project.ubicacion_cp,
            "area_superficie_escritura": project.area_superficie_escritura,
            "area_superficie_levantamiento": project.area_superficie_levantamiento,
            "estadolegal_documento_propiedad": project.estadolegal_documento_propiedad,
            "estadolegal_gravamen": project.estadolegal_gravamen,
            "estadolegal_predial": project.estadolegal_predial,
            "estadolegal_agua": project.estadolegal_agua,
            #"documento_propiedad": project.documento_propiedad,
            #"documento_gravamen": project.documento_gravamen,
            #"documento_agua": project.documento_agua,
            #"documento_predial": project.documento_predial,
            "restriccion_vial": project.restriccion_vial,
            "restriccion_cna": project.restriccion_cna,
            "restriccion_cfe": project.restriccion_cfe,
            "restriccion_pemex": project.restriccion_pemex,
            "restriccion_inha": project.restriccion_inha,
            "restriccion_otros": project.restriccion_otros,
            "restriccion_observaciones": project.restriccion_observaciones,
            "usosuelo_pmdu": project.usosuelo_pmdu,
            "usosuelo_densidad": project.usosuelo_densidad,
            "usosuelo_loteminimo": project.usosuelo_loteminimo,
            "usosuelo_m2construccion": project.usosuelo_m2construccion,
            "usosuelo_arealibre": project.usosuelo_arealibre,
            "usosuelo_altura": project.usosuelo_altura,
            "usosuelo_densidadrequerida": project.usosuelo_densidadrequerida,
            "hidraulica_fuente": project.hidraulica_fuente,
            "hidraulica_distancia": project.hidraulica_distancia,
            "hidraulica_observaciones": project.hidraulica_observaciones,
            #hidraulica_documento": project.hidraulica_documento,
            "sanitaria_tipo": project.sanitaria_tipo,
            "sanitaria_responsable": project.sanitaria_responsable,
            "sanitaria_observaciones": project.sanitaria_observaciones,
            #"sanitaria_documento": project.sanitaria_documento,
            "pluvial_tipo": project.pluvial_tipo,
            "pluvial_responsable": project.pluvial_responsable,
            "pluvial_observaciones": project.pluvial_observaciones,
            #"pluvial_documento": project.pluvial_documento.name,
            "vial_viaacceso": project.vial_viaacceso,
            "vial_distancia": project.vial_distancia,
            "vial_carriles": project.vial_carriles,
            "vial_seccion": project.vial_seccion,
            "vial_tipopavimento": project.vial_tipopavimento,
            "vial_estadoconstruccion": project.vial_estadoconstruccion,
            "vial_observaciones": project.vial_observaciones,
            #"vial_documento": project.vial_documento,
            "electricidad_tipo": project.electricidad_tipo,
            "electricidad_distancia": project.electricidad_distancia,
            "electricidad_observaciones": project.electricidad_observaciones,
            #"electricidad_documento": project.electricidad_documento,
            "alumbradopublico_tipo": project.alumbradopublico_tipo,
            "alumbradopublico_distancia": project.alumbradopublico_distancia,
            "alumbradopublico_observaciones": project.alumbradopublico_observaciones,
            #"alumbradopublico_documento": project.alumbradopublico_documento,
            "telefonia_distancia": project.telefonia_distancia,
            "telefonia_observaciones": project.telefonia_observaciones,
            #"telefonia_documento": project.telefonia_documento.name,
            "tvcable_distancia": project.tvcable_distancia,
            "tvcable_observaciones": project.tvcable_observaciones,
            "equipamiento_a100": project.equipamiento_a100,
            "equipamiento_a200": project.equipamiento_a200,
            "equipamiento_a500": project.equipamiento_a500,
            "equipamiento_regional": project.equipamiento_regional,
            "costo_predio": project.costo_predio,
            "costo_m2": project.costo_m2,
            "costo_escrituras": project.costo_escrituras,
            "costo_levantamiento": project.costo_levantamiento,
            "estudiomercado_demanda": project.estudiomercado_demanda,
            "estudiomercado_oferta": project.estudiomercado_oferta,
            "estudiomercado_conclusiones": project.estudiomercado_conclusiones,
            "estudiomercado_recomendaciones": project.estudiomercado_recomendaciones,
            "definicionproyecto_alternativa": project.definicionproyecto_alternativa,
            "definicionproyecto_tamano": project.definicionproyecto_tamano,
            "definicionproyecto_programa": project.definicionproyecto_programa,
            #"programayarea_areaprivativa": project.programayarea_areaprivativa,
            #"programayarea_caseta": project.programayarea_caseta,
            #"programayarea_jardin": project.programayarea_jardin,
            #"programayarea_vialidad": project.programayarea_vialidad,
            #"programayarea_areaverde": project.programayarea_areaverde,
            #"programayarea_estacionamientovisita": project.programayarea_estacionamientovisita,
            #"programayarea_afectacion": project.programayarea_afectacion,
            #"programayarea_documento": project.programayarea_documento,
            "latitud": project.latitud,
            "longitud": project.longitud

        }


        response = Utilities.clean_generic_queryset_from_nones(response)
        response = Utilities.clean_generic_queryset(response)

        print "Cleaned:"
        print response

        return HttpResponse(Utilities.json_to_dumps(response[0]), 'application/json', )
