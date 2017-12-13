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


class SearchAccounts(ListView):
    def get(self, request):
        number = request.GET.get('number')
        name = request.GET.get('name')
        subsidiary_account = get_array_or_none(request.GET.get('subsidiary_account'))
        nature_account = get_array_or_none(request.GET.get('nature_account'))
        grouping_code = get_array_or_none(request.GET.get('grouping_code'))
        level = get_array_or_none(request.GET.get('level'))
        item = get_array_or_none(request.GET.get('item'))


        return HttpResponse(Utilities.json_to_dumps({}), 'application/json', )