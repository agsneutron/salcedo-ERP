from django.http.response import HttpResponse
from django.views.generic.list import ListView

from Accounting.search_engines.account_engine import AccountSearchEngine
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
        subsidiary_account_array = get_array_or_none(request.GET.get('subsidiary_account'))
        nature_account_array = get_array_or_none(request.GET.get('nature_account'))
        grouping_code_array = get_array_or_none(request.GET.get('grouping_code'))
        level_array = get_array_or_none(request.GET.get('level'))
        item_array = get_array_or_none(request.GET.get('item'))


        engine = AccountSearchEngine(number,name,subsidiary_account_array,nature_account_array,grouping_code_array,level_array,item_array)


        return HttpResponse(Utilities.json_to_dumps({}), 'application/json', )