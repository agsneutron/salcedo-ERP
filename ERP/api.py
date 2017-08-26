from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from ERP.lib import utilities
from ERP.lib.utilities import Utilities
from ERP.models import Project, LineItem
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
