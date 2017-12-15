# coding=utf-8

from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q

from Accounting.models import AccountingPolicyDetail, AccountingPolicy


class PolicySearchEngine():


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

        if self.lower_account_number is not None and self.account_array is None:

            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects\
                .filter(Q(account__number__gte=self.lower_account_number))\
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)

        if self.upper_account_number is not None and self.account_array is None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(account__number__lte=self.upper_account_number)) \
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


        if self.account_array is not None:
            policy_detail_array = []
            accounting_policy_detail_set = AccountingPolicyDetail.objects \
                .filter(Q(account__number__in=self.account_array)) \
                .values('accounting_policy__id').annotate(Count('accounting_policy__id'))

            for record in accounting_policy_detail_set:
                policy_detail_array.append(record['accounting_policy__id'])

            query &= Q(id__in=policy_detail_array)




        results = AccountingPolicy.objects.filter(query)


        if self.only_with_transactions is not None:
            if bool(int(self.only_with_transactions)) == True:
                exclude_array = []
                for record in results:
                    accounting_policy_detail_set = AccountingPolicyDetail.objects.filter(Q(accounting_policy__id=record.id))
                    if len(accounting_policy_detail_set) <= 0:
                        exclude_array.append(record.id)

                results = results.exclude(Q(id__in=exclude_array))


        # Excluding the policies that overpass the debit and credit limits.
        exclude_array = []
        for policy in results:
            policy_details = AccountingPolicyDetail.objects.filter(accounting_policy__id=policy.id).values('accounting_policy__id')\
                .annotate(Count('accounting_policy__id'), total_debit=Sum('debit'), total_credit=Sum('credit'))[0]


            if self.lower_debit is not None:
                if policy_details['total_debit'] < float(self.lower_debit):
                    exclude_array.append(policy.id)

            if self.upper_debit is not None:
                if policy_details['total_debit'] > float(self.upper_debit):
                    print "Excluding: " + str(policy.id)
                    exclude_array.append(policy.id)

            if self.lower_credit is not None:
                if policy_details['total_credit'] < float(self.lower_credit):
                    exclude_array.append(policy.id)

            if self.upper_credit is not None:
                if policy_details['total_credit'] > float(self.upper_credit):
                    exclude_array.append(policy.id)


        results= results.exclude(Q(id__in=exclude_array))

        return results





