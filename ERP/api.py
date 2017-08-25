
from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from ERP.lib import utilities
from ERP.models import Project
import json

class ProjectEndpoint(View):
    def get(self,request):
        qry=Project.objects.values('id','key','nombreProyecto').order_by('key')
        the_list = []
        for register in qry:
            the_list.append(register)

        return HttpResponse(
            json.dumps(the_list, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ),
            'application/json', )