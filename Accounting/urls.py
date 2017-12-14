from django.conf.urls import url

from Accounting import api

app_name = 'DataUpload'

urlpatterns = [

    url(r'^search_policies', api.SearchPolicies.as_view(), name='policy-engine'),
    url(r'^search_accounts', api.SearchAccounts.as_view(), name='account-engine'),
    url(r'^search_providers', api.SearchProviders.as_view(), name='provider-engine'),

    # Reports.
    url(r'^generate_trial_balance', api.GenerateTrialBalance.as_view(), name='trial-balance'),
]