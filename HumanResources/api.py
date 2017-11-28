from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from ERP.lib.utilities import Utilities
from HumanResources.models import EmployeeAssistance, PayrollPeriod, Employee, EmployeePositionDescription, \
    EmployeeFinancialData


class ChangeAbsenceJustifiedStatus(View):
    def post(self, request):

        employee_assitance_id = request.POST.get('employee_assistance')
        new_status = request.POST.get('status')

        employee_assistance = EmployeeAssistance.objects.get(pk=employee_assitance_id)

        employee_assistance.justified = new_status
        employee_assistance.save()

        redirect_url = request.POST.get('redirect_url')

        return HttpResponseRedirect(redirect_url)



class GeneratePayrollReceipt(View):



    def generate_single_payroll(self, employee, payroll_period):

        total_earnings = 0
        total_deductions = 0

        receipt = {}

        # Fixed earnings.
        fixed_earnigs = employee.get_fixed_earnings()
        fixed_earnings_array = []
        for fixed_earning in fixed_earnigs:
            fixed_earnings_array.append({
                "id" : str(fixed_earning.concept.id),
                "name" : fixed_earning.concept.name,
                "amount" : str(fixed_earning.ammount)
            })
            total_earnings += fixed_earning.ammount

        receipt['fixed_earnings'] = fixed_earnings_array


        # Fixed deductions.
        fixed_deductions = employee.get_fixed_deductions()
        fixed_deductions_array = []
        for fixed_deduction in fixed_deductions:
            fixed_deductions_array.append({
                "id": str(fixed_deduction.concept.id),
                "name": fixed_deduction.concept.name,
                "amount": str(fixed_deduction.ammount)
            })
            total_deductions += fixed_deduction.ammount

        receipt['fixed_deductions'] = fixed_deductions_array


        # Variable Earnings.
        variable_earnings = employee.get_variable_earnings_for_period(payroll_period)
        variable_earnings_array = []
        for variable_earning in variable_earnings:
            variable_earnings_array.append({
                "id": str(variable_earning.concept.id),
                "name": variable_earning.concept.name,
                "amount": str(variable_earning.ammount)
            })
            total_earnings += variable_earning.ammount

        receipt['variable_earnings'] = variable_earnings_array


        # Variable Deductions.
        variable_deductions = employee.get_variable_deductions_for_period(payroll_period)
        variable_deductions_array = []
        for variable_deduction in variable_deductions:
            variable_deductions_array.append({
                "id": str(variable_deduction.concept.id),
                "name": variable_deduction.concept.name,
                "amount": str(variable_deduction.ammount)
            })
            total_deductions += variable_deduction.ammount

        receipt['variable_deductions'] = variable_deductions_array


        # Absences.
        employee_financial_data = EmployeeFinancialData.objects.get(employee_id=employee.id)
        absences = employee.get_employee_absences_for_period(payroll_period)
        absences_array = []
        for absence in absences:
            absences_array.append({
                "id" : absence.id,
                "date": str(absence.record_date),
                "amount" : str(employee_financial_data.daily_salary)
            })
            total_deductions += employee_financial_data.daily_salary

        receipt['absences'] = absences_array

        # Adding the general data to the receipt (employee and totals).
        receipt["employee_id"] = str(employee.id)
        receipt["employee_key"] = str(employee.employee_key)
        receipt["employee_fullname"] = employee.get_full_name()
        receipt["total_earnings"] = str(total_earnings)
        receipt["total_deductions"] = str(total_deductions)

        return receipt


    def get(self, request):

        payroll_period_id = request.GET.get('payroll_period')
        employee_id = request.GET.get('employee')

        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)


        if employee_id is not None:
            # Getting the employee object for a single employee.
            employee_set = Employee.objects.filter(pk=employee_id)
            self.generate_single_payroll(employee_set[0], payroll_period)

        else:

            # Getting the employee object for batch generation.
            payroll_group = payroll_period.payroll_group

            # Getting all the position descriptions related to the payroll group.
            position_description_set = EmployeePositionDescription.objects.filter(payroll_group_id=payroll_group.id)
            employee_array = []

            for position_description in position_description_set:
                employee_array.append(position_description.employee.id)



            # Getting all the employees realted to the found payroll groups.
            employee_set = Employee.objects.filter(id__in=employee_array)


        # Generating the payroll for every single employee.
        receipts_array = []
        for employee in employee_set:
            receipt = self.generate_single_payroll(employee, payroll_period)
            receipts_array.append(receipt)



        return HttpResponse(Utilities.json_to_dumps(receipts_array),'application/json; charset=utf-8')