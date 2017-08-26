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
    def post(self, request, *args, **kwargs):

        pel_id = request.POST.get('pel_id')         # Reading the Progress Estimate Log Id to filter by.
        print "Received Id: " + str(pel_id)
        log_files = LogFile.objects.filter(Q(progress_estimate_log__id=pel_id))    # Filtering the log files.

        json_files = Utilities.query_set_to_json_string(log_files)
        return HttpResponse(json_files,'application/json',)



class ConceptInputsForLineItemAndType(ListView):
    '''
        Endpoint to return the concepts or inputs filtered by a line_item and a type [concept|input]
    '''
    def get(self, request, *args, **kwargs):

        line_item_id = request.GET.get('line_item')         # Getting the type fpr the request.
        type = request.GET.get('type')                      # Getting the type fpr the request.

        qs = Concept_Input.objects.filter(Q(type=type) & Q(line_item=line_item_id)).values('id', 'description')
        cleaned_qs = Utilities.clean_generic_queryset(qs)

        return HttpResponse(cleaned_qs,'application/json',)
