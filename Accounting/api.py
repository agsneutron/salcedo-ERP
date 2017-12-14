# coding=utf-8

from django.http.response import HttpResponse
from django.views.generic.list import ListView

from Accounting.reports.trial_balance import TrialBalanceReport
from Accounting.search_engines.account_engine import AccountSearchEngine
from Accounting.search_engines.provider_engine import ProviderSearchEngine
from Accounting.search_engines.policy_engine import PolicySearchEngine
from ERP.lib.utilities import Utilities
from datetime import datetime


def get_array_or_none(the_string):
    if the_string is None or the_string == "":
        return None
    return map(int, the_string.split(','))


class SearchPolicies(ListView):

    def get(self, request):
        lower_fiscal_period_year = request.GET.get('lower_fiscal_period_year')
        upper_fiscal_period_year = request.GET.get('upper_fiscal_period_year')

        lower_fiscal_period_month = request.GET.get('lower_fiscal_period_month')
        upper_fiscal_period_month = request.GET.get('upper_fiscal_period_month')

        type_policy_array = get_array_or_none(request.GET.get('type_policy_array'))

        lower_folio = request.GET.get('lower_folio')
        upper_folio = request.GET.get('upper_folio')

        lower_registry_date = Utilities.string_to_date(request.GET.get('lower_registry_date'))
        upper_registry_date = Utilities.string_to_date(request.GET.get('upper_registry_date'))

        description = request.GET.get('description')

        lower_account_number = request.GET.get('lower_account_number')
        upper_account_number = request.GET.get('upper_account_number')

        lower_debit = request.GET.get('lower_debit')
        upper_debit = request.GET.get('upper_debit')

        lower_credit = request.GET.get('lower_credit')
        upper_credit = request.GET.get('upper_credit')

        reference = request.GET.get('reference')

        engine = PolicySearchEngine(
            lower_fiscal_period_year=lower_fiscal_period_year,
            upper_fiscal_period_year=upper_fiscal_period_year,
            lower_fiscal_period_month=lower_fiscal_period_month,
            upper_fiscal_period_month=upper_fiscal_period_month,
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


        return HttpResponse(Utilities.query_set_to_dumps(result), 'application/json; charset=utf-8', )


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

        return HttpResponse(Utilities.query_set_to_dumps(results), 'application/json; charset=utf-8', )


class SearchProviders(ListView):
    def get(self, request):
        name = request.GET.get('name')
        rfc = request.GET.get('rfc')
        email = request.GET.get('email')
        phone_number = request.GET.get('phone_number')
        accounting_account_number = request.GET.get('accounting_account_number')
        bank_account = request.GET.get('bank_account')
        register_date_lower = Utilities.string_to_date(request.GET.get('register_date_lower'))
        register_date_upper = Utilities.string_to_date(request.GET.get('register_date_upper'))
        services = request.GET.get('services')

        engine = ProviderSearchEngine(name, rfc, email, phone_number, accounting_account_number, bank_account,
                                      register_date_lower, register_date_upper, services)

        results = engine.search()

        return HttpResponse(Utilities.query_set_to_dumps(results), 'application/json; charset=utf-8', )


#
#   Reports.
#

class GenerateTrialBalance(ListView):
    def get(self, request):
        lower_account_number = request.GET.get('lower_account_number')
        upper_account_number = request.GET.get('upper_account_number')

        fiscal_period_year = request.GET.get('fiscal_period_year')
        fiscal_period_month = request.GET.get('fiscal_period_month')

        only_with_transactions = request.GET.get('only_with_transactions')

        engine = PolicySearchEngine(
            lower_fiscal_period_year=fiscal_period_year,
            upper_fiscal_period_year=fiscal_period_year,
            lower_fiscal_period_month=fiscal_period_month,
            upper_fiscal_period_month=fiscal_period_month,
            lower_account_number=lower_account_number,
            upper_account_number=upper_account_number,
            only_with_transactions=only_with_transactions
        )

        result = engine.search_policies()

        report_result = TrialBalanceReport.generate_report(result)

        return HttpResponse(Utilities.query_set_to_dumps(result), 'application/json; charset=utf-8', )