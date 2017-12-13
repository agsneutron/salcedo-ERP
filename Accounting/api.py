from django.http.response import HttpResponse
from django.views.generic.list import ListView

from Accounting.search_engines.account_engine import AccountSearchEngine
from Accounting.search_engines.provider_engine import ProviderSearchEngine
from ERP.lib.utilities import Utilities
from datetime import datetime


def get_array_or_none(the_string):
    if the_string is None or the_string == "":
        return None
    return map(int, the_string.split(','))


def string_to_date(str):
    if str is None:
        return None
    return datetime.strptime(str, '%m/%d/%Y')


class SearchPolicies(ListView):
    def get(self, request):
        return HttpResponse(Utilities.json_to_dumps({}), 'application/json', )


class SearchAccounts(ListView):
    def get(self, request):
        number = request.GET.get('number')
        name = request.GET.get('name')
        subsidiary_account_array = get_array_or_none(request.GET.get('subsidiary_account_array'))
        nature_account_array = get_array_or_none(request.GET.get('nature_account_array'))
        grouping_code_array = get_array_or_none(request.GET.get('grouping_code_array'))
        level = request.GET.get('level')
        item = request.GET.get('item')

        engine = AccountSearchEngine(number, name, subsidiary_account_array, nature_account_array, grouping_code_array,
                                     level, item)

        results = engine.search()

        return HttpResponse(Utilities.query_set_to_dumps(results), 'application/json', )


class SearchProviders(ListView):
    def get(self, request):
        name = request.GET.get('name')
        rfc = request.GET.get('rfc')
        email = request.GET.get('email')
        phone_number = request.GET.get('phone_number')
        accounting_account_number = request.GET.get('accounting_account_number')
        register_date = request.GET.get('register_date')

        nature_account_array = get_array_or_none(request.GET.get('nature_account_array'))

        # engine = ProviderSearchEngine(number, name, subsidiary_account_array, nature_account_array, grouping_code_array,
        #                               level, item)
        #
        # results = engine.search()

        return HttpResponse(Utilities.query_set_to_dumps({}), 'application/json', )
