from django import template
from django.db import models
from django.db.models import Q

from HumanResources.models import EmployeePayrollPeriodExclusion

register = template.Library()


@register.filter(name='employee_is_active')
def employee_is_active(employee_data, payrollperiod):

    exclusions = EmployeePayrollPeriodExclusion.objects.filter(Q(employee__id=employee_data['employee_id']) & Q(payroll_period=payrollperiod))

    if (len(exclusions) > 0):
        return 'checked="checked"'

    return ""


@register.filter(name='subtract')
def subtract(value, arg):
    return float(value) - float(arg)