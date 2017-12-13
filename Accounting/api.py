from django.http.response import HttpResponse
from django.views.generic.list import ListView
from ERP.lib.utilities import Utilities


class SearchPolicies(ListView):
    def get(self, request):

        
        return HttpResponse(Utilities.json_to_dumps({}),'application/json', )


class SearchAccounts(ListView):
    def get(self, request):
        number = request.GET.get('number')
        name = request.GET.get('name')
        subsidiary_account = request.GET.get('subsidiary_account')
        nature_account = request.GET.get('nature_account')
        grouping_code = request.GET.get('grouping_code')
        level = request.GET.get('level')
        item = request.GET.get('item')


        return HttpResponse(Utilities.json_to_dumps({}), 'application/json', )