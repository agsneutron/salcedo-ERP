# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ERP.forms import ProgressEstimateLogForm, LogFileForm
from ERP.models import ProgressEstimateLog, LogFile
from django.db.models import Q

from django.shortcuts import render


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
    logs = ProgressEstimateLog.objects.all()
    files = []
    if logs:
        print logs.first().id
        files = LogFile.objects.filter(Q(progress_estimate_log__id=logs.first().id))

    for file in files:
        print file.file

    params = {
        'pel_form': progress_estimate_log_form,
        'files_form': log_file_form
    }
    return render(request, 'ProgressEstimateLog/progress_estimate_log_form.html', params)
