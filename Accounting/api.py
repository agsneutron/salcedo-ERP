from django.http.response import HttpResponse
from django.views.generic.list import ListView
from ERP.lib.utilities import Utilities


def get_array_or_none(the_string):
    if the_string is None or the_string == "":
        return None
    else:
        return map(int, the_string.split(','))


class SearchPolicies(ListView):
    def get(self, request):


        return HttpResponse(Utilities.json_to_dumps({}),'application/json', )