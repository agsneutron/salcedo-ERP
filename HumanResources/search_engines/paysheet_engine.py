# coding=utf-8

from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q

from HumanResources.models import PayrollReceiptProcessed, PayrollProcessedDetail


class PaySheetSearchEngine():


    def __init__(self,payroll_period):


        '''self.lower_debit = lower_debit
        self.upper_debit = upper_debit
        self.account_array = account_array'''

        self.payroll_period = payroll_period

    def search_paysheet(self):
        query = Q()

        if self.payroll_period is not None:
            query &= Q(payroll_receip_processed__payroll_period_id=self.payroll_period)

        results = PayrollProcessedDetail.objects.filter(query)


        return results





