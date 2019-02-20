# coding=utf-8
from __future__ import unicode_literals

from decimal import Decimal
from django.db.models import F
from django.db.models import Q, Count, Sum
from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from ERP.lib import utilities
from ERP.lib.utilities import Utilities
from ERP.models import Project, LineItem, Estimate, Concept_Input, ProgressEstimate, ProjectSections, Section, \
    AccessToProject, ContratoContratista
from ERP.models import ContractConcepts
import json


def get_array_or_none(the_string):
    if the_string is None or the_string == "":
        return None
    else:
        return map(int, the_string.split(','))


class ProjectEndpoint(View):
    def get(self, request):
        qry = Project.objects.values('id', 'key', 'nombreProyecto').order_by('key')
        the_list = []
        for register in qry:
            the_list.append(register)

        return HttpResponse(
            Utilities.json_to_dumps(the_list),
            'application/json', )

class ContractorByProject(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        contractors = ContratoContratista.objects.filter(project_id=project_id).values('contratista_id','contratista__nombreContratista')\
            .annotate(Count('contratista_id'), Count('contratista__nombreContratista'))

        the_list = []

        for contractor in contractors:
            new_item = {
                'id': contractor['contratista_id'],
                'nombreContratista': unicode(contractor['contratista__nombreContratista'])
            }
            the_list.append(new_item)

        return HttpResponse(
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json; charset=utf-8')


class LineItemsByProject(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        line_items = LineItem.objects.filter(project_id=project_id)

        the_list = []

        for line_item in line_items:
            new_item = {
                'id': line_item.id,
                'description': unicode(line_item.description)
            }
            the_list.append(new_item)

        return HttpResponse(
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json; charset=utf-8')


class SectionsByProjectEndpoint(View):
    def get(self, request):
        project_id = request.GET.get('project_id')

        response = []
        sections = ProjectSections.objects.filter(Q(project_id=project_id) & Q(section__parent_section=None))
        for section in sections:

            temp_json = {
                "project_section_id": section.id,
                "project_section_name": section.section.section_name,
                "project_section_status": section.status,
                "inner_sections": []

            }
            inner_sections = ProjectSections.objects.filter(
                Q(project_id=project_id) & Q(section__parent_section__id=section.section.id))
            for inner_section in inner_sections:
                temp_json["inner_sections"].append({
                    "project_section_id": inner_section.id,
                    "project_section_name": inner_section.section.section_name,
                    "project_section_status": inner_section.status,
                })
            response.append(temp_json)

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8')


class CleanProject(View):
    def get(self, request):
        project_id = request.GET.get('project_id')


        items = LineItem.objects.filter(project_id=project_id)

        for item in items:
            item.delete()



        return HttpResponse('ok cleaning project', 'application/json; charset=utf-8')


class CleanEstimate(View):
    def get(self, request):
        estimate_id = request.GET.get('id')


        items = ProgressEstimate.objects.filter(estimate_id=estimate_id)

        for item in items:
            item.delete()


        estimate = Estimate.objects.get(pk=estimate_id)
        estimate.lock_status = 'L'
        estimate.save()



        return HttpResponse('ok', 'application/json; charset=utf-8')


class Saveamountofestimate(View):
    def get(self, request):
        ID_Estimate = request.GET.get('ID')

        if ID_Estimate is not None:
            Hasta_Estimacion = request.GET.get('AEstaEstimacion')
            De_Estimacion = request.GET.get('DeEstaEstimacion')

            Concept = ContractConcepts.objects.filter(id=ID_Estimate)


            if Concept:
                Concept.OfThisEstimate = De_Estimacion
                Concept.ThisEstimate = Hasta_Estimacion
                Concept.save()

                return HttpResponse('ok', 'application/json; charset=utf-8')
            else:
                new_it = {
                    'mensaje': 'No Se guardó correctamente la información'
                }
                return HttpResponse('ok', 'application/json; charset=utf-8')
        else:
            New_it = {
                'mensaje': 'El ID no es correcto'
            }
            return HttpResponse('ok', 'application/json; charset=utf-8')




class SectionsByProjectSave(View):
    def get(self, request):
        secciones_id = get_array_or_none(request.GET.get('secciones'))
        no_seleccionados = get_array_or_none(request.GET.get('noseleccionados'))

        if secciones_id is not None:
            projectid = request.GET.get('project_id')
            sections = ProjectSections.objects.filter(project_id=projectid, id__in=secciones_id)
            if sections.count() == 0:
                for section in secciones_id:
                    addPS = ProjectSections.objects.create(project_id=projectid, id=section, status=1)
            else:
                for section in secciones_id:
                    addPS = ProjectSections.objects.filter(project_id=projectid, id=section)
                    if addPS.count() == 0:
                        addPSN = ProjectSections.objects.create(project_id=projectid, id=section, status=1)
                    else:
                        addPSS = ProjectSections.objects.filter(project_id=projectid, id=section).get(id=section)
                        if addPSS:
                            addPSS.status = 1
                            addPSS.save()
                        else:
                            addPSN = ProjectSections.objects.create(project_id=projectid, id=section, status=1)

        # no seleccionados
        if no_seleccionados is not None:
            sections = ProjectSections.objects.filter(project_id=projectid, id__in=no_seleccionados)

            if sections.count() == 0:
                for section in no_seleccionados:
                    addPS = ProjectSections.objects.create(project_id=projectid, id=section, status=0)
            else:
                for section in no_seleccionados:
                    addPS = ProjectSections.objects.filter(project_id=projectid, id=section)
                    if addPS.count() == 0:
                        addPSN = ProjectSections.objects.create(project_id=projectid, id=section, status=0)
                    else:
                        addPSS = ProjectSections.objects.filter(project_id=projectid, id=section).get(
                            id=section)
                        if addPSS:
                            addPSS.status = 0
                            addPSS.save()
                        else:
                            addPSN = ProjectSections.objects.create(project_id=projectid, id=section, status=0)

        the_list = []
        new_item = {
            'codigo_respuesta': 0,
            'mensaje': 'Se guardó correctamente la información'
        }

        the_list.append(new_item)

        return HttpResponse(
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json; charset=utf-8')


class EstimatesByLineItems(View):
    def get(self, request):
        line_item_id = request.GET.get('line_item_id')
        estimates = Estimate.objects.filter(line_item_id=line_item_id)

        description_qs = LineItem.objects.filter(id=line_item_id)
        if len(description_qs) == 0:
            the_list = {'error': 'There is no line_item with id = ' + line_item_id}
            return HttpResponse(
                json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
                'application/json; charset=utf-8')

        the_list = {'line_item': {
            'id': line_item_id,
            'description': 'desc'
        }, 'estimates': []}

        for estimate in estimates:
            new_item = {
                'id': estimate.id,
                'start_date': estimate.start_date,
                'end_date': estimate.end_date,
                'period': estimate.period,
            }
            the_list['estimates'].append(new_item)

        return HttpResponse(
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json; charset=utf-8')



class AccessToProjectByUser(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        accesses = AccessToProject.objects.filter(user_id=user_id)

        return HttpResponse(Utilities.query_set_to_dumps(accesses), 'application/json; charset=utf-8')


