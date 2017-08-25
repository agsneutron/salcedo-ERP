
from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from ERP.lib import utilities
from ERP.models import Project

class ProjectEndpoint(View):
    def get(self):
        qry=Project.objects.values('id','key','nombreProyecto').order_by('key')
        return HttpResponse(utilities.query_set_to_dumps(qry), 'application/json')