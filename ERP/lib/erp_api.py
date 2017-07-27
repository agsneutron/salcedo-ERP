# coding=utf-8
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.db.models import Q

# Custom classes
from ERP.lib.utilities import Utilities

# Model imports.
from ERP.models import *


#
class LogFilesForProgressEstimateLogEndpoint(ListView):
    ''' Endpoit to return the Log Files that belong to a Progress Estimate Log.
    '''
    def get(self, request, *args, **kwargs):

        pel_id = request.GET.get('pel_id')         # Reading the Progress Estimate Log Id to filter by.
        print "Received Id: " + str(pel_id)
        log_files = LogFile.objects.filter(Q(progress_estimate_log__id=pel_id))    # Filtering the log files.

        json_files = Utilities.query_set_to_json(log_files)
        return HttpResponse(json_files,'application/json',)
