# coding=utf-8
from _mysql import IntegrityError
from datetime import timedelta
from django.contrib import messages

import datetime

from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

from ERP.lib.utilities import Utilities
from HumanResources.models import PayrollPeriod, EmployeePositionDescription, Employee, EmployeeAssistance


class AutomaticAbsences(ListView):

    def get_assistance_days_for_employee(self, employee):

        poistion_description = EmployeePositionDescription.objects.get(employee_id=employee.id)
        assistance_days_array = []

        monday = poistion_description.monday
        tuesday = poistion_description.tuesday
        wednesday = poistion_description.wednesday
        thursday = poistion_description.thursday
        friday = poistion_description.friday
        saturday = poistion_description.saturday
        sunday = poistion_description.sunday

        if monday:
            assistance_days_array.append(0)

        if tuesday:
            assistance_days_array.append(1)

        if wednesday:
            assistance_days_array.append(2)

        if thursday:
            assistance_days_array.append(3)

        if friday:
            assistance_days_array.append(4)

        if saturday:
            assistance_days_array.append(5)

        if sunday:
            assistance_days_array.append(6)


        return assistance_days_array



    def generate_automatic_absecences_for_employee(self, payroll_period, employee):
        assistance_days = self.get_assistance_days_for_employee(employee)
        start_date = payroll_period.start_period
        end_date = payroll_period.end_period

        control_date = start_date
        while control_date <= end_date:

            control_date = control_date + timedelta(days=1)
            day_of_the_week = control_date.weekday()


            if day_of_the_week in assistance_days:

                control_assistance = EmployeeAssistance.objects.filter(
                    Q(employee=employee) &
                    Q(payroll_period=payroll_period) &
                    Q(record_date=control_date))

                if len(control_assistance) < 0:

                    employee_assistance = EmployeeAssistance(
                        employee = employee,
                        payroll_period=payroll_period,
                        record_date=control_date,
                        entry_time=datetime.time(00,00),
                        exit_time=datetime.time(00,00),
                        absence=True,
                        justified=False
                    )


                    employee_assistance.save()



    def get(self, request):
        payroll_period_id = int(request.GET.get('payroll_period'))
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        # Getting the employee object for batch generation.
        payroll_group = payroll_period.payroll_group

        # Getting all the position descriptions related to the payroll group.
        position_description_set = EmployeePositionDescription.objects.filter(payroll_group_id=payroll_group.id)
        employee_array = []

        for position_description in position_description_set:
            employee_array.append(position_description.employee.id)

        # Getting all the employees realted to the found payroll groups.
        employee_set = Employee.objects.filter(id__in=employee_array)


        for employee in employee_set:
            self.generate_automatic_absecences_for_employee(payroll_period, employee)

        messages.success(request, "Se crearon exitosamente las faltas para el periodo correspondiente")

        return HttpResponseRedirect("http://localhost:8000/admin")