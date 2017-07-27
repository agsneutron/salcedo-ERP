# coding=utf-8
from __future__ import unicode_literals
from ERP.forms import ProgressEstimateLogForm, LogFileForm
from ERP.models import ProgressEstimateLog, LogFile, ProgressEstimate
from django.db.models import Q
import json

from django.shortcuts import render
from ERP.lib.utilities import Utilities

# Create your views here.
def progress_estimate_log_view(request):
    project = request.GET.get('project')
    concept = request.GET.get('concept')
    estimate = request.GET.get('estimate')
    progress_estimate = request.GET.get('progress_estimate')

    # Retrieving data from the model to be rendered.
    if progress_estimate is None:
        logs_queryset = ProgressEstimateLog.objects.all()
    else:
        logs_queryset = ProgressEstimateLog.objects.first(Q(progress_estimate=progress_estimate))



    if logs_queryset:
        # As both cases where treated as querysets, we can retrieve the first id.
        progress_estimate_id = logs_queryset.first().progress_estimate.id
        logs = []
        for log in logs_queryset:
            user_fullname = log.user.user.first_name + " " + log.user.user.last_name
            log = log.to_serializable_dict()
            log['user_fullname'] = user_fullname
            logs.append(log)

        log_files = []
        if logs:
            log_files = LogFile.objects.filter(Q(progress_estimate_log__id=logs[0]['id']))



        params = {
            'logs': Utilities.json_to_safe_string(logs),
            'log_files': Utilities.query_set_to_json_string(log_files),
            'progress_estimate_id': progress_estimate_id
        }

    else:
        params = {
            'logs': [],
            'log_files': [],
            'progress_estimate_id': ProgressEstimate.objects.all().first().id
        }

    return render(request, 'ProgressEstimateLog/progress_estimate_log_form.html', params)
