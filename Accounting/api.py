# coding=utf-8
import csv

from django.db.models.aggregates import Sum, Count
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.generic.list import ListView

from Accounting.models import AccountingPolicyDetail
from Accounting.reports.general_balance import GeneralBalanceEngine
from Accounting.reports.trial_balance import TrialBalanceReport
from Accounting.search_engines.account_engine import AccountSearchEngine
from Accounting.search_engines.policy_engine import PolicySearchEngine
from Accounting.search_engines.transactions_engine import TransactionsEngine
from Accounting.search_engines.provider_engine import ProviderSearchEngine

from ERP.lib.utilities import Utilities
from SharedCatalogs.models import Account
from datetime import datetime
from django.shortcuts import redirect, render
import requests

from reporting.api import createCSVResponseFromQueryset


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

        # If the account number is set, the range is ignored.
        account_number_array = get_array_or_none(request.GET.get('account'))

        internal_company = request.GET.get('internal_company')

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
            reference=reference,
            only_with_transactions=False,
            account_array=account_number_array,
            internal_company=internal_company
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
        #item = request.GET.get('item')
        item_account_array = get_array_or_none(request.GET.get('item_account_array'))
        internal_company = request.GET.get('internal_company')

        engine = AccountSearchEngine(number, name, subsidiary_account_array, nature_account_array, grouping_code_array,
                                     level, item_account_array, internal_company)

        results = engine.search()

        response = {
            'accounts': []
        }

        for account in results:
            response['accounts'].append({
                'id': account.id,
                'number': str(account.number),
                'name': account.name,
                'status': account.status,
                'nature_account': account.nature_account,
                'item_id': account.item_id,
                'item': str(account.item.name),
                'internal_company_id': account.internal_company_id,
                'internal_company': str(account.internal_company),
                'grouping_code_id': account.grouping_code_id,
                'grouping_code': str(account.grouping_code),
                'subsidiary_account_id': account.subsidiary_account_id,
                'subsidiary_account': str(account.subsidiary_account),
                'type_account': account.type_account
            })

        return HttpResponse(Utilities.json_to_dumps(response['accounts']), 'application/json; charset=utf-8', )
        # return HttpResponse(Utilities.query_set_to_dumps(results), 'application/json; charset=utf-8', )


class SearchProviders(ListView):
    def get(self, request):

        if request.GET.get('export_excel') is not None:
            export_excel = True
        else:
            print(' not excel');
            export_excel = False

        type = request.GET.get('type')

        if type is None:
            return HttpResponse(Utilities.json_to_dumps({"error": {"message": "The parameter 'type' is required."}}),
                                'application/json; charset=utf-8', )

        # Make it uppercase so that it's easier to compare.
        type = type.upper()

        if type not in ('PROVIDER', 'CREDITOR', 'THIRD_PARTY'):
            return HttpResponse(Utilities.json_to_dumps(
                {"error": {"message": "The parameter 'type' must be PROVIDER, CREDITOR or THIRD_PARTY."}}),
                'application/json; charset=utf-8', )

        name = request.GET.get('name')
        rfc = request.GET.get('rfc')
        email = request.GET.get('email')
        phone_number = request.GET.get('phone_number')
        accounting_account_number = request.GET.get('accounting_account_number')
        bank_account = request.GET.get('bank_account')
        register_date_lower = Utilities.string_to_date(request.GET.get('register_date_lower'))
        register_date_upper = Utilities.string_to_date(request.GET.get('register_date_upper'))
        services = request.GET.get('services')

        engine = ProviderSearchEngine(type, name, rfc, email, phone_number, accounting_account_number, bank_account,
                                      register_date_lower, register_date_upper, services)

        results = engine.search()

        if export_excel:
            values = ['name', 'country', 'colony', 'street', 'outdoor_number', 'indoor_number', 'zip_code',
                      'rfc', 'curp',
                      'phone_number', 'phone_number_2', 'email', 'cellphone_number', 'office_number',
                      'extension_number']
            return createCSVResponseFromQueryset(results, values)
        else:
            return HttpResponse(Utilities.query_set_to_dumps(results), 'application/json; charset=utf-8', )


class SearchTransactionsByAccount(ListView):
    def group_transactions_by_account(self, transactions):
        grouped = transactions.values('account__id', 'account__name', 'account__number') \
            .annotate(Count('account__id'), Count('account__name'), Count('account__number'),
                      total_credit=Sum('credit'), total_debit=Sum('debit'))

        return grouped

    def exclude_debit_limits(self, lower_debit, upper_debit, grouped_transactions):
        if lower_debit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_debit__lt=lower_debit))

        if upper_debit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_debit__gt=upper_debit))

        return grouped_transactions

    def exclude_credit_limits(self, lower_credit, upper_credit, grouped_transactions):
        if lower_credit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_credit__lt=lower_credit))

        if upper_credit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_credit__gt=upper_credit))

        return grouped_transactions

    def get(self, request, *args, **kwargs):
        fiscal_period_year = request.GET.get('fiscal_period_year')

        fiscal_period_month = request.GET.get('fiscal_period_month')

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

        internal_company = request.GET.get('internal_company')

        # If the account number is set, the range is ignored.
        account_number_array = get_array_or_none(request.GET.get('account'))

        engine = TransactionsEngine(
            fiscal_period_year=fiscal_period_year,
            fiscal_period_month=fiscal_period_month,
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
            reference=reference,
            only_with_transactions=False,
            account_array=account_number_array,
            internal_company=internal_company
        )

        transactions = engine.search_transactions()

        # Grouping all the transactions by accounts.
        grouped_transactions = self.group_transactions_by_account(transactions)

        # Excluding the accounts that overpass the debit limits.
        grouped_transactions = self.exclude_debit_limits(lower_debit, upper_debit, grouped_transactions)

        # Excluding the accounts that overpass the credit limits.
        grouped_transactions = self.exclude_credit_limits(lower_credit, upper_credit, grouped_transactions)

        response = {
            'accounts': []
        }

        for account in grouped_transactions:
            response['accounts'].append({
                'account_id': account['account__id'],
                'account_name': account['account__name'],
                'account_number': str(account['account__number']),
                'total_credit': account['total_credit'],
                'total_debit': account['total_debit']
            })

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8', )


#
#   Reports.
#

class GenerateTrialBalance(ListView):
    def get_details_for_policies(self, policies_set):
        policies_id_array = []
        for policiy in policies_set:
            policies_id_array.append(policiy.id)

        policy_details_set = AccountingPolicyDetail.objects.filter(Q(accounting_policy__id__in=policies_id_array))

        return policy_details_set

    def get(self, request):
        lower_account_number = request.GET.get('lower_account_number')
        upper_account_number = request.GET.get('upper_account_number')

        fiscal_period_year = request.GET.get('fiscal_period_year')
        fiscal_period_month = request.GET.get('fiscal_period_month')

        title = request.GET.get('title')

        internal_company = request.GET.get('internal_company')

        only_with_transactions = request.GET.get('only_with_transactions')

        engine = PolicySearchEngine(
            lower_fiscal_period_year=fiscal_period_year,
            upper_fiscal_period_year=fiscal_period_year,
            lower_fiscal_period_month=fiscal_period_month,
            upper_fiscal_period_month=fiscal_period_month,
            lower_account_number=lower_account_number,
            upper_account_number=upper_account_number,
            only_with_transactions=only_with_transactions,
            internal_company=internal_company
        )

        result = engine.search_policies()

        policies_details_set = self.get_details_for_policies(result)

        # General data to send to the report maker.
        general_data = {
            "title": title,
            "year": fiscal_period_year,
            "month": fiscal_period_month
        }

        report_result = TrialBalanceReport.generate_report(general_data, policies_details_set)

        # return HttpResponse(Utilities.query_set_to_dumps(result), 'application/json; charset=utf-8', )
        return report_result


class GenerateBalance(ListView):
    def get(self, request):
        lower_account_number = request.GET.get('lower_account_number')
        upper_account_number = request.GET.get('upper_account_number')

        fiscal_period_year = request.GET.get('fiscal_period_year')
        fiscal_period_month = request.GET.get('fiscal_period_month')

        title = request.GET.get('title')

        internal_company = request.GET.get('internal_company')

        only_with_transactions = request.GET.get('only_with_transactions')
        only_with_balance = request.GET.get('only_with_balance')

        engine = GeneralBalanceEngine(
            title=title,
            lower_account_number=lower_account_number,
            upper_account_number=upper_account_number,
            fiscal_period_year=fiscal_period_year,
            fiscal_period_month=fiscal_period_month,
            only_with_transactions=only_with_transactions,
            only_with_balance=only_with_balance,
            internal_company=internal_company)

        result = engine.generate()

        return result

        # return HttpResponse(Utilities.json_to_dumps({}), 'application/json; charset=utf-8', )


class GenerateTransactionsByAccountReport(ListView):
    def create_general_structure(self, report_title, year, month, account):

        parent_account = account.subsidiary_account
        if parent_account is None:
            parent_account_name = '-'
            parent_account_number = '-'
        else:
            parent_account_name = parent_account.name
            parent_account_number = parent_account.number

        if report_title is None or report_title is "":
            title = "Transacciones de la cuenta " + str(account.number) + " " + account.name
        else:
            title = report_title

        general_structure = {
            'report_title': title,
            'fiscal_period_year': year,
            'fiscal_period_month': month,
            'account_number': str(account.number),
            'account_name': account.name,
            'parent_account_name': parent_account_name,
            'parent_account_number': parent_account_number,
            'grouping_code': float(account.grouping_code.grouping_code),
            'grouping_code_name': account.grouping_code.account_name,
            'transactions': []
        }

        return general_structure

    def create_transaction_structure(self, transaction_info):

        account_structure = {
            'description': transaction_info.description,
            'debit': transaction_info.debit,
            'credit': transaction_info.credit,
            'policy_folio': transaction_info.accounting_policy.folio,
            'policy_type': transaction_info.accounting_policy.type_policy.name
        }

        return account_structure

    def get(self, request, *args, **kwargs):
        fiscal_period_year = request.GET.get('fiscal_period_year')

        fiscal_period_month = request.GET.get('fiscal_period_month')

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

        internal_company = request.GET.get('internal_company')

        report_title = request.GET.get('report_title')

        # If the account number is set, the range is ignored.
        account_number_array = get_array_or_none(request.GET.get('account'))

        engine = TransactionsEngine(
            fiscal_period_year=fiscal_period_year,
            fiscal_period_month=fiscal_period_month,
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
            reference=reference,
            only_with_transactions=False,
            account_array=account_number_array,
            internal_company=internal_company
        )

        transactions_set = engine.search_transactions()

        # Getting the account number.
        account_number = account_number_array[0]

        # Getting the account object.
        account_object = Account.objects.get(number=account_number)

        # Creating the general structure for the response.
        general_structure = self.create_general_structure(
            report_title,
            fiscal_period_year,
            fiscal_period_month,
            account_object
        )

        # Accumulated amounts.
        total_debit = 0
        total_credit = 0

        # Creating the structure for each of the accounts.
        for transaction in transactions_set:
            total_debit += transaction.debit
            total_credit += transaction.credit
            transaction_structure = self.create_transaction_structure(transaction)
            general_structure['transactions'].append(transaction_structure)

        # Assigning the accumulated amounts.
        general_structure['total_debit'] = total_debit
        general_structure['total_credit'] = total_credit

        return engine.generate_report(general_structure)

        # return HttpResponse(Utilities.json_to_dumps(general_structure) , 'application/json; charset=utf-8', )


class CommercialAllyEndpoint(ListView):
    def get(self, request, name):
        r = requests.post('http://127.0.0.1:8000/admin/Accounting/commercialally/add', data={'name': 'alex'})
        # r=redirect('/admin/Accounting/commercialally/add',params={'name':'alex'})

        return r
        # return render(request,'/admin/Accounting/commercialally/add/',{'name':'alex'})
        # return redirect('/admin/Accounting/commercialally/add',id=name)
