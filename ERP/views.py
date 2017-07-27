# coding=utf-8
from __future__ import unicode_literals
from ERP.forms import ProgressEstimateLogForm, LogFileForm
from ERP.models import ProgressEstimateLog, LogFile
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

    # Getting the forms to add to the specific models.
    progress_estimate_log_form = ProgressEstimateLogForm()
    log_file_form = LogFileForm()

    # Retrieving data from the model to be rendered.
    logs_queryset = ProgressEstimateLog.objects.all()

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
        'pel_form': progress_estimate_log_form,
        'files_form': log_file_form,
        'logs': Utilities.json_to_safe_string(logs),
        'log_files': Utilities.query_set_to_json_string(log_files)
    }

    return render(request, 'ProgressEstimateLog/progress_estimate_log_form.html', params)
