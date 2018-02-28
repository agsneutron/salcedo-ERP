from django import template
from django.db import models
from django.db.models import Q

from HumanResources.models import EmployeePayrollPeriodExclusion

register = template.Library()


@register.filter(name='employee_is_active')
def employee_is_active(employee_description, payrollperiod):

    exclusions = EmployeePayrollPeriodExclusion.objects.filter(Q(employee=employee_description.employee) & Q(payroll_period=payrollperiod))

    if (len(exclusions) > 0):
        return 'checked="checked"'

    return ""
