from django.db.models import Q

from Accounting.models import Account


class ProviderSearchEngine(object):
    """
        Search engines for the Account model
    """

    def __init__(self, number, name, subsidiary_account_array, nature_account_array, grouping_code_array, level,
                 item):
        self.number = number
        self.name = name
        self.subsidiary_account_array = subsidiary_account_array
        self.nature_account_array = nature_account_array
        self.grouping_code_array = grouping_code_array
        self.level = level
        self.item = item

    def search(self):
        """
        Searches for accounts according to the parameters set in constructor
        :return: Queryset with the results
        """
        q = Q()

        if self.number is not None:
            q = q & Q(number=self.number)

        if self.name is not None:
            q = q & Q(name=self.name)

        if self.subsidiary_account_array is not None:
            q = q & Q(subsidiary_account__in=self.subsidiary_account_array)

        if self.nature_account_array is not None:
            q = q & Q(nature_account__in=self.nature_account_array)

        if self.grouping_code_array is not None:
            q = q & Q(grouping_code__in=self.grouping_code_array)

        if self.level is not None:
            q = q & Q(level__icontains=str(self.level))

        if self.item is not None:
            q = q & Q(item__icontains=str(self.item))

        return Account.objects.filter(q)
