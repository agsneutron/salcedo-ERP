from Accounting.models import AccountingPolicyDetail


class TrialBalanceReport():

    @staticmethod
    def generate_report(queryset):
        for record in queryset:
            accounting_policy_detail_set = AccountingPolicyDetail.objects.filter(Q(accounting_policy__id=record.id))
            pass