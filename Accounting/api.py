from django.http.response import HttpResponse
from django.views.generic.list import ListView
from ERP.lib.utilities import Utilities


class SearchPolicies(ListView):
    def get(self, request):

        
        return HttpResponse(Utilities.json_to_dumps({}),'application/json', )