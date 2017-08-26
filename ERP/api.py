from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from ERP.lib import utilities
from ERP.lib.utilities import Utilities
from ERP.models import Project, LineItem, Estimate
import json


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
