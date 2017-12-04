# coding=utf-8

from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from ERP.lib.utilities import Utilities
from HumanResources.models import EmployeeAssistance, PayrollPeriod, Employee, EmployeePositionDescription, \
    EmployeeFinancialData, PayrollProcessedDetail, PayrollReceiptProcessed
from SalcedoERP.lib.SystemLog import LoggingConstants, SystemException
from reporting.lib.employee_payment_receipt import EmployeePaymentReceipt
from django.db import transaction


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

    def create_historic_record(self, payroll_period, receipts):

        for receipt in receipts:

            employee = Employee.objects.get(pk=receipt['employee_id'])
            employee_total_earnings = float(receipt['total_earnings'])
            employee_total_deductions = float(receipt['total_deductions'])
            employee_total_taxed = float(receipt['total_taxed'])


            payroll_receipt_processed = PayrollReceiptProcessed(
                employee=employee,
                payroll_period=payroll_period,
                worked_days=0,
                total_perceptions=employee_total_earnings,
                total_deductions=employee_total_deductions,
                total_payroll=employee_total_earnings - employee_total_deductions,
                taxed=0,
                exempt=0,
                daily_salry=0,
                total_withholdings=0,
                total_discounts=0
            )

            payroll_receipt_processed.save()


        return True

    def validate_employee_financial_data(self, employee):
        try:
            employee_financial_data = EmployeeFinancialData.objects.get(employee__id = employee.id)
            return True

        except EmployeeFinancialData.DoesNotExist as e:
            return False



    def generate_single_payroll(self, employee, payroll_period):

        total_earnings = 0
        total_deductions = 0
        total_taxable = 0
        earnings_array = []
        deductions_array = []

        receipt = {}

        # Fixed earnings.
        fixed_earnigs = employee.get_fixed_earnings()
        fixed_earnings_array = []
        for fixed_earning in fixed_earnigs:
            fixed_earning_json = {
                "id" : str(fixed_earning.concept.id),
                "name" : fixed_earning.concept.name,
                "amount" : str(fixed_earning.ammount)
            }
            fixed_earnings_array.append(fixed_earning_json)
            earnings_array.append(fixed_earning_json)
            total_earnings += fixed_earning.ammount
            total_taxable += fixed_earning.ammount * fixed_earning.concept.percent_taxable / 100

        receipt['fixed_earnings'] = fixed_earnings_array


        # Fixed deductions.
        fixed_deductions = employee.get_fixed_deductions()
        fixed_deductions_array = []
        for fixed_deduction in fixed_deductions:
            fixed_deduction_json = {
                "id": str(fixed_deduction.concept.id),
                "name": fixed_deduction.concept.name,
                "amount": str(fixed_deduction.ammount)
            }
            fixed_deductions_array.append(fixed_deduction_json)
            deductions_array.append(fixed_deduction_json)
            total_deductions += fixed_deduction.ammount

        receipt['fixed_deductions'] = fixed_deductions_array



        # Variable Earnings.
        variable_earnings = employee.get_variable_earnings_for_period(payroll_period)
        variable_earnings_array = []
        for variable_earning in variable_earnings:
            variable_earning_json = {
                "id": str(variable_earning.concept.id),
                "name": variable_earning.concept.name,
                "amount": str(variable_earning.ammount)
            }
            variable_earnings_array.append(variable_earning_json)
            earnings_array.append(variable_earning_json)
            total_earnings += variable_earning.ammount
            total_taxable += fixed_earning.ammount * fixed_earning.concept.percent_taxable / 100

        receipt['variable_earnings'] = variable_earnings_array



        # Variable Deductions.
        variable_deductions = employee.get_variable_deductions_for_period(payroll_period)
        variable_deductions_array = []
        for variable_deduction in variable_deductions:
            variable_deduction_json = {
                "id": str(variable_deduction.concept.id),
                "name": variable_deduction.concept.name,
                "amount": str(variable_deduction.ammount)
            }
            variable_deductions_array.append(variable_deduction_json)
            deductions_array.append(variable_deduction_json)
            total_deductions += variable_deduction.ammount

        receipt['variable_deductions'] = variable_deductions_array





        # Absences.
        employee_financial_data = EmployeeFinancialData.objects.get(employee_id=employee.id)
        absences = employee.get_unjustified_employee_absences_for_period(payroll_period)
        absences_array = []
        for absence in absences:
            absence_json = {
                "id" : absence.id,
                "name": "Falta del " + str(absence.record_date),
                "amount" : str(employee_financial_data.daily_salary)
            }
            absences_array.append(absence_json)
            deductions_array.append(absence_json)
            total_deductions += employee_financial_data.daily_salary

        receipt['absences'] = absences_array


        # General array.
        receipt['earnings'] = earnings_array
        receipt['deductions'] = deductions_array
        receipt['total_taxable'] = float(total_taxable)


        # Adding the general data to the receipt (employee and totals).
        receipt["employee_id"] = str(employee.id)
        receipt["employee_key"] = str(employee.employee_key)
        receipt["rfc"] = str(employee.rfc)
        receipt["ssn"] = str(employee.social_security_number)
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
        try:
            with transaction.atomic():
                for employee in employee_set:
                    financial_data_exists = self.validate_employee_financial_data(employee)

                    # If any of the employees lacks of financial data, return an error.
                    if not financial_data_exists:
                        raise ErrorDataUpload('Ha habido un problema generando los recibos de nómina. El empleado '+employee.employee_key+
                                              " no cuenta con datos financieros cargados en el sistema", LoggingConstants.ERROR, request.user.id)


                    receipt = self.generate_single_payroll(employee, payroll_period)
                    receipts_array.append(receipt)



                #return HttpResponse(Utilities.json_to_dumps(receipts_array),'application/json; charset=utf-8')


                result = self.create_historic_record(payroll_period, receipts_array)
                # response = EmployeePaymentReceipt.generate_employee_payment_receipts(receipts_array)
                # return response

                return HttpResponse(Utilities.json_to_dumps(receipts_array),'application/json; charset=utf-8')


        except ErrorDataUpload as e:
            e.save()
            raise e



class ErrorDataUpload(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.OPERATION_LOGIC, priority, user_id)