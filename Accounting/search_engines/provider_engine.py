from datetime import date

from django.db.models import Q

from Accounting.models import Provider
from ERP.lib.utilities import Utilities


class ProviderSearchEngine(object):
    """
        Search engines for the Provider model
    """

    def __init__(self, name, rfc, email, phone_number, accounting_account_number, bank_account, register_date_lower,
                 register_date_upper, services):
        self.name = name
        self.rfc = rfc
        self.email = email
        self.phone_number = phone_number
        self.accounting_account_number = accounting_account_number
        self.bank_account = bank_account
        self.register_date_lower = register_date_lower
        self.register_date_upper = register_date_upper
        self.services = services

    def search(self):
        """
        Searches for providers according to the parameters set in constructor
        :return: Queryset with the results
        """
        q = Q()

        if self.name is not None:
            q = q & Q(name__icontains=self.name)

        if self.rfc is not None:
            q = q & Q(rfc__icontains=self.rfc)

        if self.email is not None:
            q = q & Q(email__icontains=self.email)

        if self.phone_number is not None:
            q = q & Q(phone_number__icontains=self.phone_number)

        if self.accounting_account_number is not None:
            q = q & Q(accounting_account__number__icontains=self.accounting_account_number)

        if self.bank_account is not None:
            q = q & Q(bank_account__icontains=self.bank_account)

        if self.register_date_lower is not None:
            # dt = date(self.register_date.year, self.register_date.month, self.register_date.day)
            q = q & Q(register_date__gte=self.register_date_lower)

        if self.register_date_upper is not None:
            q = q & Q(register_date__lte=self.register_date_upper)

        if self.services is not None:
            q = q & Q(services__icontains=self.services)

        return Provider.objects.filter(q)
