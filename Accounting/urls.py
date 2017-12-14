from django.conf.urls import url

from Accounting import api
from Accounting import views

app_name = 'DataUpload'

urlpatterns = [

    url(r'^search_policies', api.SearchPolicies.as_view(), name='policy-engine'),
    url(r'^search_accounts', api.SearchAccounts.as_view(), name='account-engine'),
    url(r'^search_commercial_allies', api.SearchProviders.as_view(), name='commercial-allies-engine'),
    url(r'^searchaccount', views.SearchAccount, name='searchaccount'),
    url(r'^searchcomercialallie', views.SearchComercialAllie, name='searchcomercialallie')
]