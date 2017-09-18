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
from ERP.models import Project, LineItem, Estimate, Concept_Input, ProgressEstimate, ProjectSections,Section
import json


def get_array_or_none(the_string):
    if the_string is None or the_string=="":
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
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json', )


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
                "project_section_name": section.section.sectionName,
                "project_section_status": section.status,
                "inner_sections": []

            }
            inner_sections = ProjectSections.objects.filter(Q(project_id=project_id) & Q(section__parent_section__id=section.section.id))
            for inner_section in inner_sections:
                temp_json["inner_sections"].append({
                    "project_section_id": inner_section.id,
                    "project_section_name": inner_section.section.sectionName,
                    "project_section_status": inner_section.status,
                })
            response.append(temp_json)

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8')



class SectionsByProjectSave(View):
    def get(self, request):
        secciones_id = get_array_or_none(request.GET.get('secciones'))
        no_seleccionados = get_array_or_none(request.GET.get('noseleccionados'))
        projectid = request.GET.get('project_id')
        sections = ProjectSections.objects.filter(project_id=projectid,section_id__in=secciones_id)

        if sections.count() == 0:
            for section in secciones_id:
                addPS = ProjectSections.objects.create(project_id=projectid, section_id=section, status=1)
        else:
            for section in secciones_id:
                addPS = ProjectSections.objects.filter(project_id=projectid,section_id=section)
                if addPS.count() == 0:
                    addPSN = ProjectSections.objects.create(project_id=projectid, section_id=section, status=1)
                else:
                    addPSS = ProjectSections.objects.filter(project_id=projectid, section_id=section).get(section_id=section)
                    if addPSS:
                        addPSS.status = 1
                        addPSS.save()
                    else:
                        addPSN = ProjectSections.objects.create(project_id=projectid, section_id=section, status=1)

        #no seleccionados
        sections = ProjectSections.objects.filter(project_id=projectid, section_id__in=no_seleccionados)

        if sections.count() == 0:
            for section in no_seleccionados:
                addPS = ProjectSections.objects.create(project_id=projectid, section_id=section, status=0)
        else:
            for section in no_seleccionados:
                addPS = ProjectSections.objects.filter(project_id=projectid, section_id=section)
                if addPS.count() == 0:
                    addPSN = ProjectSections.objects.create(project_id=projectid, section_id=section, status=0)
                else:
                    addPSS = ProjectSections.objects.filter(project_id=projectid, section_id=section).get(
                        section_id=section)
                    if addPSS:
                        addPSS.status = 0
                        addPSS.save()
                    else:
                        addPSN = ProjectSections.objects.create(project_id=projectid, section_id=section, status=0)


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


class FinancialHistoricalProgressReport(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        line_items = LineItem.objects.filter(project_id=project_id)
        type = 'C'

        response = []
        structured_response = []
        parent_keys = {}
        line_item_general_programmed = {}
        line_item_general_estimated = {}

        for line_item in line_items:
            temp_concepts = Concept_Input.objects.filter(Q(type=type) & Q(line_item_id=line_item.id))

            parent_line_item_key = LineItem.objects.filter(pk=line_item.parent_line_item_id)

            tem_obj = {"key": line_item.key, "parent_key": parent_line_item_key}

            if len(parent_line_item_key) > 0:
                tem_obj['parent_key'] = parent_line_item_key[0].key
                parent_keys[str(line_item.key)] = str(parent_line_item_key[0].key)
                is_sub_line_item = True
            else:
                tem_obj['parent_key'] = ''
                parent_keys[str(line_item.key)] = ''
                is_sub_line_item = False

            line_item_concepts = []

            programmed = temp_concepts.values('line_item_id').annotate(Count('line_item_id'),
                                                                       total_programmed=Sum(
                                                                           F('unit_price') * F('quantity')))

            estimated = ProgressEstimate.objects.filter(estimate__concept_input__line_item_id=line_item.id).values(
                'estimate__concept_input__line_item_id').annotate(Count('estimate__concept_input__line_item_id'),
                                                                  total_estimated=Sum('amount'))

            # for concept in temp_concepts:
            #     line_item_concepts.append(concept.to_serializable_dict())

            # tem_obj['concepts'] = line_item_concepts

            if programmed.exists():
                total_programmed = programmed[0]['total_programmed']
                if str(line_item.key) not in line_item_general_programmed.keys():
                    line_item_general_programmed[str(line_item.key)] = 0
                line_item_general_programmed[str(line_item.key)] = line_item_general_programmed[
                                                                       str(line_item.key)] + total_programmed
                tem_obj['total_programmed'] = str(total_programmed)
            else:
                tem_obj['total_programmed'] = '0.00'

            if estimated.exists():
                total_estimated = estimated[0]['total_estimated']
                tem_obj['total_estimated'] = str(total_estimated)
                tem_obj['total_pending'] = str(
                    Decimal(tem_obj['total_programmed']) - Decimal(tem_obj['total_estimated']))

                if str(line_item.key) not in line_item_general_estimated.keys():
                    line_item_general_estimated[str(line_item.key)] = 0
                    line_item_general_estimated[str(line_item.key)] = line_item_general_estimated[
                                                                          str(line_item.key)] + total_estimated
            else:
                tem_obj['total_estimated'] = '0.00'
                tem_obj['total_pending'] = tem_obj['total_programmed']

            response.append(tem_obj)


        for element in response:
            temp_parent_key = element['parent_key']
            temp_current_key = element['key']

            if temp_parent_key == '':
                element['greatest_parent'] = ''
            else:
                while temp_parent_key != "":
                    temp_current_key = temp_parent_key
                    temp_parent_key = parent_keys[temp_parent_key]
                element['greatest_parent'] = temp_current_key

        for element in response:
            key = element['key']
            if parent_keys[key] == '':
                general_programmed_sum = 0
                general_estimated_sum = 0
                for element2 in response:
                    parent_key = element2['greatest_parent']
                    current_key = element2['key']
                    if parent_key == key and current_key in line_item_general_programmed.keys():
                        general_programmed_sum = general_programmed_sum + line_item_general_programmed[str(current_key)]

                    if parent_key == key and current_key in line_item_general_estimated.keys():
                        general_estimated_sum = general_estimated_sum + line_item_general_estimated[str(current_key)]

                element['general_programmed_sum'] = str(general_programmed_sum)
                element['general_estimated_sum'] = str(general_estimated_sum)
                element['general_pending_sum'] = str(general_programmed_sum - general_estimated_sum)

                sub_line_items = []

                for record in response:
                    if record['greatest_parent'] == element['key']:
                        sub_line_items.append(record)

                element['sub_line_items'] = sub_line_items

                structured_response.append(element)

        return HttpResponse(
            Utilities.json_to_dumps(structured_response), 'application/json; charset=utf-8')
