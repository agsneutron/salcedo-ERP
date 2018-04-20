from django.conf.urls import url

from Accounting import api
from Accounting import views
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

app_name = 'Accounting'
reverse_lazy = lazy(reverse,str)

urlpatterns = [

    url(r'^search_policies', api.SearchPolicies.as_view(), name='policy-engine'),
    url(r'^search_accounts', api.SearchAccounts.as_view(), name='account-engine'),
    url(r'^search_commercial_allies', api.SearchProviders.as_view(), name='commercial-allies-engine'),
    url(r'^search_transactions_by_account', api.SearchTransactionsByAccount.as_view(), name='search-transactions'),

    # Reports.
    url(r'^generate_trial_balance', api.GenerateTrialBalance.as_view(), name='trial-balance'),
    url(r'^generate_general_balance', api.GenerateBalance.as_view(), name='general-balance'),
    url(r'^transactions_by_account_report', api.GenerateTransactionsByAccountReport.as_view(), name='general-balance'),

    # F/E
    url(r'^searchaccount', views.SearchAccount, name='searchaccount'),
    url(r'^policiedetail', views.PolicieDetail, name='policiedetail'),
    url(r'^searchprovider', views.SearchProvider, name='searchprovider'),
    url(r'^searchcreditors', views.SearchCreditors, name='searchcreditors'),
    url(r'^searchpolicies', views.SearchPolicies, name='searchpolicies'),
    url(r'^searchthird', views.SearchThird, name='searchthird'),
    url(r'^searchtransactions', views.SearchTransactions, name='searchtransactions'),
    url(r'^policiesbyaccount', views.PoliciesAccountList, name='policiesbyaccount'),
    url(r'^generatetrialbalance', views.GenerateTrialBalance, name='generatetrialbalance'),
    url(r'^generategeneralbalance', views.GenerateGeneralBalance, name='generategeneralbalance'),


    #catalogs
    #url(r'^api/commercialally/$', api.CommercialAllyEndpoint.as_view(),{'name': 'provider'}),




]