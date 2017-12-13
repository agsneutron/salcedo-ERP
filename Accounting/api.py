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
        lower_fiscal_period = request.GET.get('lower_fiscal_period')
        upper_fiscal_period = request.GET.get('upper_fiscal_period')

        type_policy = get_array_or_none(request.GET.get('type_policy'))

        lower_folio = request.GET.get('lower_folio')
        upper_folio = request.GET.get('upper_folio')

        lower_registry_date = request.GET.get('upper_folio')
        upper_registry_date = request.GET.get('upper_registry_date')

        description = request.GET.get('description')


        lower_account_number = request.GET.get('lower_account_number')
        upper_account_number = request.GET.get('upper_account_number')

        lower_debit = request.GET.get('lower_debit')
        upper_debit = request.GET.get('upper_debit')

        lower_credit = request.GET.get('lower_credit')
        upper_credit = request.GET.get('upper_credit')


        return HttpResponse(Utilities.json_to_dumps({}),'application/json', )