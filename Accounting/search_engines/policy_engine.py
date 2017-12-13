class PolicySearchEngine():


    def __init__(self,
                  lower_fiscal_period,
                  upper_fiscal_period,
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

        self.lower_fiscal_period = lower_fiscal_period
        self.upper_fiscal_period = upper_fiscal_period
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
        
        return {}