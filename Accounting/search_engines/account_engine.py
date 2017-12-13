from django.db.models import Q

from Accounting.models import Account


class AccountSearchEngine():
    def __init__(self, number, name, subsidiary_account_array, nature_account_array, grouping_code_array, level,
                 item_array):
        self.number = number
        self.name = name
        self.subsidiary_account_array = subsidiary_account_array
        self.nature_account_array = nature_account_array
        self.grouping_code_array = grouping_code_array
        self.level = level
        self.item_array = item_array

    def search(self):
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

        return Account.objects.filter(q)
