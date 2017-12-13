from django.http.response import HttpResponse
from django.views.generic.list import ListView

from Accounting.search_engines.account_engine import AccountSearchEngine
from Accounting.search_engines.policy_engine import PolicySearchEngine
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

        type_policy_array = get_array_or_none(request.GET.get('type_policy_array'))

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

        reference = request.GET.get('reference')

        engine = PolicySearchEngine(
            lower_fiscal_period=lower_fiscal_period,
            upper_fiscal_period=upper_fiscal_period,
            type_policy_array=type_policy_array,
            lower_folio=lower_folio,
            upper_folio=upper_folio,
            lower_registry_date=lower_registry_date,
            upper_registry_date=upper_registry_date,
            description=description,
            lower_account_number=lower_account_number,
            upper_account_number=upper_account_number,
            lower_debit=lower_debit,
            upper_debit=upper_debit,
            lower_credit=lower_credit,
            upper_credit=upper_credit,
            reference=reference
        )

        result = engine.search_policies()


        return HttpResponse(Utilities.json_to_dumps(result),'application/json', )


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