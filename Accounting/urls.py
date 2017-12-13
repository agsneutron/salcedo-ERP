from django.conf.urls import url

from Accounting import api

app_name = 'DataUpload'

urlpatterns = [

    url(r'^search_policies', api.SearchPolicies.as_view(), name='policy-engine')

]