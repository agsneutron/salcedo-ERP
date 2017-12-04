"""SalcedoERP URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import api
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect
from django.conf import settings



import reporting
from users import urls
import users
from ERP import urls
import ERP

import HumanResources
from HumanResources import views

from reporting import urls

from users import views
from HumanResources import views


from django.conf.urls.static import static

urlpatterns = [


    url(r'^employeehome$', views.employeehome, name='employeehome'),
    url(r'^payrollhome$', views.payrollhome, name='payrollhome'),
    url(r'^employeebyperiod', views.EmployeeByPeriod, name='employeebyperiod'),

    # Calls to API

    url(r'^api/change_justified_status', api.ChangeAbsenceJustifiedStatus.as_view(), name='change_justified_status'),
    url(r'^api/generate_payroll_receipt$', api.GeneratePayrollReceipt.as_view(), name='generate_payroll_receipt'),
    url(r'^api/generate_payroll_receipt_for_employee$', api.GeneratePayrollReceiptForEmployee.as_view(), name='generate_payroll_receipt_for_employee'),


]