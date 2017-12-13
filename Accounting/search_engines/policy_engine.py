# coding=utf-8

from django.db.models.aggregates import Count
from django.db.models.query_utils import Q

from Accounting.models import AccountingPolicyDetail, AccountingPolicy


class PolicySearchEngine():


    def __init__(self,
                 lower_fiscal_period_year,
                 upper_fiscal_period_year,
                 lower_fiscal_period_month,
                 upper_fiscal_period_month,
                 type_policy_array,
                 lower_folio,
                 upper_folio,
                 lower_registry_date,
                 upper_registry_date,
                 description,
                 lower_account_number,
                 upper_account_number,
                 lower_debit,
                 upper_debit,
                 lower_credit,
                 upper_credit,
                 reference):

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


    def search_policies(self):
        query = Q()

        if self.lower_fiscal_period_year is not None:
            query &= Q(fiscal_period__accounting_year__gte=self.lower_fiscal_period_year)


        if self.upper_fiscal_period_year is not None:
            query &= Q(fiscal_period__accounting_year__lte=self.upper_fiscal_period_year)

        if self.lower_fiscal_period_month is not None:
            query &= Q(fiscal_period__account_period__gte=self.lower_fiscal_period_month)

        if self.upper_fiscal_period_month is not None:
            query &= Q(fiscal_period__account_period__lte=self.upper_fiscal_period_month)

        if self.type_policy_array is not None:
            query &= Q(type_policy__id__in=self.type_policy_array)

        if self.lower_folio is not None:
            query &= Q(folio__gte=self.lower_folio)

        if self.upper_folio is not None:
            query &= Q(folio__lte=self.upper_folio)

        if self.lower_registry_date is not None:
            query &= Q(registry_date__gte=self.lower_registry_date)


        if self.upper_registry_date is not None:
            query &= Q(registry_date__lte=self.upper_registry_date)

        if self.description is not None:
            query &= Q(description__icontains=self.description)

        if self.lower_account_number is not None:

            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects\
                .filter(Q(account__number__gte=self.lower_account_number))\
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.upper_account_number is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(account__number__lte=self.upper_account_number)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.lower_debit is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(debit__gte=self.lower_debit)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.upper_debit is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(debit__lte=self.upper_debit)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.lower_credit is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(credit__gte=self.lower_credit)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.upper_credit is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(credit__lte=self.upper_credit)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.reference is not None:
            query &= Q(reference__icontains=self.reference)




        return AccountingPolicy.objects.filter(query)