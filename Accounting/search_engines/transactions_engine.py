# coding=utf-8

from django.db.models.aggregates import Count
from django.db.models.query_utils import Q

from Accounting.models import AccountingPolicyDetail, AccountingPolicy


class TransactionsEngine():


    def __init__(self,
                 lower_fiscal_period_year=None,
                 upper_fiscal_period_year=None,
                 lower_fiscal_period_month=None,
                 upper_fiscal_period_month=None,
                 type_policy_array=None,
                 lower_folio=None,
                 upper_folio=None,
                 lower_registry_date=None,
                 upper_registry_date=None,
                 description=None,
                 lower_account_number=None,
                 upper_account_number=None,
                 lower_debit=None,
                 upper_debit=None,
                 lower_credit=None,
                 upper_credit=None,
                 reference=None,
                 only_with_transactions=None,
                 account_array = None
                 ):

        self.lower_fiscal_period_year = lower_fiscal_period_year
        self.upper_fiscal_period_year = upper_fiscal_period_year

        self.lower_fiscal_period_month = lower_fiscal_period_month
        self.upper_fiscal_period_month = upper_fiscal_period_month

        self.type_policy_array = type_policy_array

        self.lower_folio = lower_folio
        self.upper_folio = upper_folio

        self.lower_registry_date = lower_registry_date
        self.upper_registry_date = upper_registry_date

        self.description = description

        self.lower_account_number = lower_account_number
        self.upper_account_number = upper_account_number

        self.lower_debit = lower_debit
        self.upper_debit = upper_debit

        self.lower_credit = lower_credit
        self.upper_credit = upper_credit

        self.reference = reference

        self.only_with_transactions = only_with_transactions

        self.account_array = account_array

    def search_transactions(self):
        query = Q()

        if self.lower_fiscal_period_year is not None:
            query &= Q(accounting_policy__fiscal_period__accounting_year__gte=self.lower_fiscal_period_year)


        if self.upper_fiscal_period_year is not None:
            query &= Q(accounting_policy__fiscal_period__accounting_year__lte=self.upper_fiscal_period_year)

        if self.lower_fiscal_period_month is not None:
            query &= Q(accounting_policy__fiscal_period__account_period__gte=self.lower_fiscal_period_month)

        if self.upper_fiscal_period_month is not None:
            query &= Q(accounting_policy__fiscal_period__account_period__lte=self.upper_fiscal_period_month)

        if self.type_policy_array is not None:
            query &= Q(accounting_policy__type_policy__id__in=self.type_policy_array)

        if self.lower_folio is not None:
            query &= Q(accounting_policy__folio__gte=self.lower_folio)

        if self.upper_folio is not None:
            query &= Q(accounting_policy__folio__lte=self.upper_folio)

        if self.lower_registry_date is not None:
            query &= Q(accounting_policy__registry_date__gte=self.lower_registry_date)


        if self.upper_registry_date is not None:
            query &= Q(accounting_policy__registry_date__lte=self.upper_registry_date)

        if self.description is not None:
            query &= Q(accounting_policy__description__icontains=self.description)

        if self.lower_account_number is not None and self.account_array is None:
            query &= Q(account__number__gte=self.lower_account_number)

        if self.upper_account_number is not None and self.account_array is None:
            query &= Q(account__number__lte=self.lower_account_number)

        if self.lower_debit is not None:
            query &= Q(debit__gte=self.lower_debit)

        if self.upper_debit is not None:
            query &= Q(debit__lte=self.upper_debit)

        if self.lower_credit is not None:
            query &= Q(credit__gte=self.lower_credit)

        if self.upper_credit is not None:
            query &= Q(credit__lte=self.upper_credit)


        if self.reference is not None:
            query &= Q(accounting_policy__reference__icontains=self.reference)


        if self.account_array is not None:
            query &= Q(account__number__in=self.account_array)




        results = AccountingPolicyDetail.objects.filter(query)



        return results





