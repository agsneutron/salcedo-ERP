# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports.
from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView


# Model Imports.
from HumanResources.models import *



class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = "HumanResources/employee-detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)

        #progressestimatelog = context['progressestimatelog']
        #context['logfiles'] = LogFile.objects.filter(Q(progress_estimate_log_id=progressestimatelog.id))

        return context