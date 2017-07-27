# coding=utf-8
from django.http import HttpResponse
from django.views.generic.list import ListView
import json

# Custom classes
from ERP.lib.utilities import Utilities
from ERP.forms import ProgressEstimateLogForm

# Model imports.
from ERP.models import *

class SaveProgressEstimateLogFormEndpoint(ListView):
    ''' Endpoit to return the Log Files that belong to a Progress Estimate Log.
    '''
    def get(self, request, *args, **kwargs):
        form = ProgressEstimateLogForm(request.GET)

        return HttpResponse(json.dumps({'Hola':'Test'}), 'application/json',)
