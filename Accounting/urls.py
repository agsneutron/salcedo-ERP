from django.conf.urls import url

from Accounting import api
from Accounting import views

app_name = 'DataUpload'

urlpatterns = [

    url(r'^search_policies', api.SearchPolicies.as_view(), name='policy-engine'),
    url(r'^search_accounts', api.SearchAccounts.as_view(), name='account-engine'),
    url(r'^search_commercial_allies', api.SearchProviders.as_view(), name='commercial-allies-engine'),
    url(r'^search_transactions_by_account', api.SearchTransactionsByAccount.as_view(), name='search-transactions'),

    # Reports.
    url(r'^generate_trial_balance', api.GenerateTrialBalance.as_view(), name='trial-balance'),
    url(r'^generate_general_balance', api.GenerateBalance.as_view(), name='general-balance'),

    # F/E
    url(r'^searchaccount', views.SearchAccount, name='searchaccount'),
    url(r'^searchprovider', views.SearchProvider, name='searchprovider'),
    url(r'^searchcreditors', views.SearchCreditors, name='searchcreditors'),
    url(r'^searchthird', views.SearchThird, name='searchthird'),




]