# coding=utf-8

import json
import django
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from ERP.lib.utilities import Utilities
from HumanResources.models import EmployeeAssistance, PayrollPeriod, Employee, EmployeePositionDescription, \
    EmployeeFinancialData, PayrollProcessedDetail, PayrollReceiptProcessed, ISRTable, EarningsDeductions, \
    EmployeeEarningsDeductionsbyPeriod, EmployeeEarningsDeductions, Tag, EmployeePayrollPeriodExclusion
from SalcedoERP.lib.SystemLog import LoggingConstants, SystemException
from reporting.lib.employee_payment_receipt import EmployeePaymentReceipt
from django.db import transaction
from django.views.generic.list import ListView


# Convierte a un string separado por comas en un arreglo o None
def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(str, the_string.split(','))


class ChangeAbsenceJustifiedStatus(View):
    def post(self, request):
        employee_assitance_id = request.POST.get('employee_assistance')
        new_status = request.POST.get('status')

        employee_assistance = EmployeeAssistance.objects.get(pk=employee_assitance_id)

        employee_assistance.justified = new_status
        employee_assistance.save()

        redirect_url = request.POST.get('redirect_url')

        return HttpResponseRedirect(redirect_url)




class DeleteAssistances(View):
    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period')
        assistances_to_delete = EmployeeAssistance.objects.filter(payroll_period=payroll_period_id)

        for assistance in assistances_to_delete:
            assistance.delete()


        return HttpResponseRedirect('/humanresources/employeebyperiod/?payrollperiod='+str(payroll_period_id))

class GeneratePayrollReceipt(View):
    def get_ISR_from_taxable(self, earnings):

        isr_rules = ISRTable.objects.all()
        for rule in isr_rules:
            # Finding the range the earnings belong to.
            if (earnings >= rule.lower_limit and earnings <= rule.upper_limit) or (
                            earnings >= rule.lower_limit and rule.upper_limit == 0):
                # Subtracting the lower limit to the earnings.
                tax_minus_lower_limit = earnings - rule.lower_limit

                # Multiplying by the rate.
                value_per_rate = tax_minus_lower_limit * rule.rate

                # Adding the fixed fee to the result.
                result = value_per_rate + rule.fixed_fee

                # Rounding the result to two decimals.
                result = round(result, 2)

                return result

        return 0

    def create_earnings_deductions_historic(self, payroll_receipt_processed, concept_json):

        try:
            if concept_json["id"] != "":
                concept_id = int(concept_json["id"])
            else:
                concept_id = None

            concept = EarningsDeductions.objects.get(pk=concept_id)

            new_obj = PayrollProcessedDetail(
                name=concept.name,
                percent_taxable=concept.percent_taxable,
                sat_key=concept.sat_key,
                law_type=concept.law_type,
                status=concept.status,
                accounting_account=concept.account.id,
                comments=concept.comments,
                type=concept.type,
                taxable=concept.get_taxable_display(),
                category=concept.get_category_display(),
                payroll_receip_processed=payroll_receipt_processed,
                amount=concept_json['amount']
            )

        except EarningsDeductions.DoesNotExist as e:

            new_obj = PayrollProcessedDetail(
                name=concept_json["name"],
                percent_taxable=100,
                sat_key=0,
                law_type="-",
                status="Activa",
                accounting_account=0,
                comments="-",
                type=EarningsDeductions.DEDUCCION,
                taxable="Sí",
                category="Variable",
                payroll_receip_processed=payroll_receipt_processed,
                amount=float(concept_json['amount'])
            )

        new_obj.save()

    def create_receipt_historic_record(self, payroll_period, receipts):

        for receipt in receipts:

            employee = Employee.objects.get(pk=receipt['employee_id'])
            employee_total_earnings = float(receipt['total_earnings'])
            employee_total_deductions = float(receipt['total_deductions'])
            employee_total_taxed = float(receipt['total_taxable'])
            employee_isr = float(receipt['isr'])

            employee_financial_data = EmployeeFinancialData.objects.get(employee_id=employee.id)

            payroll_receipt_processed = PayrollReceiptProcessed(
                employee=employee,
                payroll_period=payroll_period,
                worked_days=0,
                total_perceptions=employee_total_earnings,
                total_deductions=employee_total_deductions,
                total_payroll=employee_total_earnings - employee_total_deductions,
                taxed=employee_total_taxed,
                exempt=employee_total_earnings - employee_total_taxed,
                daily_salary=employee_financial_data.daily_salary,
                total_withholdings=employee_isr,
                total_discounts=employee_total_deductions
            )

            payroll_receipt_processed.save()

            for deduction in receipt['deductions']:
                self.create_earnings_deductions_historic(payroll_receipt_processed, deduction)

            for earning in receipt['earnings']:
                self.create_earnings_deductions_historic(payroll_receipt_processed, earning)

        return True

    def validate_employee_financial_data(self, employee):
        try:
            employee_financial_data = EmployeeFinancialData.objects.get(employee__id=employee.id)
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
                "id": str(fixed_earning.concept.id),
                "name": fixed_earning.concept.name,
                "amount": str(fixed_earning.ammount)
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
            total_taxable += variable_earning.ammount * variable_earning.concept.percent_taxable / 100

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
                "id": absence.id,
                "name": "Falta del " + str(absence.record_date),
                "amount": str(employee_financial_data.daily_salary)
            }
            absences_array.append(absence_json)
            deductions_array.append(absence_json)
            total_deductions += employee_financial_data.daily_salary

        receipt['absences'] = absences_array

        # ISR.
        isr = self.get_ISR_from_taxable(float(total_taxable))
        deductions_array.append({
            "id": "",
            "name": "ISR",
            "amount": isr
        })
        total_deductions = float(total_deductions) + isr

        # General array.
        receipt['earnings'] = earnings_array
        receipt['deductions'] = deductions_array
        receipt['total_taxable'] = float(total_taxable)
        receipt['isr'] = isr

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

        excluded_employees_csv = request.GET.get('employeesSelected')
        if excluded_employees_csv == "":
            excluded_employees = []
        else:
            excluded_employees = get_array_or_none(excluded_employees_csv)

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
            employee_set = Employee.objects.filter(Q(id__in=employee_array)).exclude(id__in=excluded_employees)

        # Generating the payroll for every single employee.
        receipts_array = []

        try:
            with transaction.atomic():
                for employee in employee_set:
                    financial_data_exists = self.validate_employee_financial_data(employee)

                    # If any of the employees lacks of financial data, return an error.
                    if not financial_data_exists:
                        raise Exception(
                            'Ha habido un problema generando los recibos de nómina. El empleado ' + employee.employee_key +
                            " no cuenta con datos financieros cargados en el sistema")

                    receipt = self.generate_single_payroll(employee, payroll_period)
                    receipts_array.append(receipt)

                result = self.create_receipt_historic_record(payroll_period, receipts_array)
                response = EmployeePaymentReceipt.generate_employee_payment_receipts(receipts_array)
                return response




        except Exception as e:
            print "Exception was: " + str(e)
            django.contrib.messages.error(request, "Ya se han generado los recibos de nómina anteriormente.")
            return HttpResponseRedirect(
                "/humanresources/employeebyperiod?payrollperiod=" + str(payroll_period.id) + "&payrollgroup=" + str(
                    payroll_period.payroll_group.id))


class GeneratePayrollReceiptForEmployee(View):
    def get_historic_deductions(self, payroll_receipt_processed, employee):
        deductions_array = []
        details = PayrollProcessedDetail.objects.filter(
            Q(payroll_receip_processed=payroll_receipt_processed) & Q(payroll_receip_processed__employee=employee) & Q(
                type=EarningsDeductions.DEDUCCION))
        for record in details:
            deductions_array.append({
                "name": record.name,
                "amount": record.amount
            })

        return deductions_array

    def get_historic_earnings(self, payroll_receipt_processed, employee):
        earnings_array = []
        details = PayrollProcessedDetail.objects.filter(
            Q(payroll_receip_processed=payroll_receipt_processed) & Q(payroll_receip_processed__employee=employee) & Q(
                type=EarningsDeductions.PERCEPCION))
        for record in details:
            earnings_array.append({
                "name": record.name,
                "amount": record.amount
            })

        return earnings_array

    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period')
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        employee_id = request.GET.get('employee')
        employee = Employee.objects.get(pk=employee_id)

        payroll_receipt_processed = PayrollReceiptProcessed.objects.get(
            Q(payroll_period__id=payroll_period.id) & Q(employee_id=employee.id))

        receipts_array = []
        receipt = {}
        deductions_array = self.get_historic_deductions(payroll_receipt_processed, employee)
        earnings_array = self.get_historic_earnings(payroll_receipt_processed, employee)

        receipt['earnings'] = earnings_array
        receipt['deductions'] = deductions_array

        # General array.
        receipt['total_taxable'] = payroll_receipt_processed.taxed
        receipt['isr'] = payroll_receipt_processed.total_withholdings

        # Adding the general data to the receipt (employee and totals).
        receipt["employee_id"] = str(employee.id)
        receipt["employee_key"] = str(employee.employee_key)
        receipt["rfc"] = str(employee.rfc)
        receipt["ssn"] = str(employee.social_security_number)
        receipt["employee_fullname"] = employee.get_full_name()
        receipt["total_earnings"] = str(payroll_receipt_processed.total_perceptions)
        receipt["total_deductions"] = str(payroll_receipt_processed.total_deductions)

        receipts_array.append(receipt)
        response = EmployeePaymentReceipt.generate_employee_payment_receipts(receipts_array)

        # return HttpResponse(Utilities.json_to_dumps({}),'application/json; charset=utf-8')
        return response


class DeletePayrollReceiptsForPeriod(View):
    def get(selfself, request):
        payroll_period_id = request.GET.get('payroll_period')
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payroll_receipt_processed = PayrollReceiptProcessed.objects.filter(payroll_period_id=payroll_period_id)
        '''
        if len(payroll_receipt_processed) > 0:
            payroll_processed_detail = PayrollProcessedDetail.objects.filter(payroll_receip_processed = payroll_receipt_processed)
            print payroll_processed_detail

            for record in payroll_processed_detail:
                record.delete()
        '''
        payroll_receipt_processed.delete()

        django.contrib.messages.success(request, "Se han borrado exitosamente los recibos de nómina.")

        return HttpResponseRedirect(
            "/humanresources/employeebyperiod?payrollperiod=" + str(payroll_period.id) + "&payrollgroup=" + str(
                payroll_period.payroll_group.id))


class ErrorDataUpload(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.OPERATION_LOGIC, priority, user_id)


class Get_Tags(ListView):
    def get(self, request, *args, **kwargs):
        consulta_tags = Tag.objects.all()

        json_response = []
        for tag in consulta_tags:
            json_tags = {}
            json_tags['id'] = tag.id
            json_tags['nombre'] = tag.name
            json_response.append(json_tags)

        return HttpResponse(
            json.dumps(json_response, indent=4, separators=(',', ': '), sort_keys=False,
                       ensure_ascii=False),
            'application/json; charset=utf-8')


class SaveExcludedEmployeesForPeriod(View):
    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period_id')
        data = request.GET.get('data')
        data = json.loads(data)

        for record in data:
            employee_id = record["employee"]
            is_excluded = record["excluded"]
            previous_record = EmployeePayrollPeriodExclusion.objects.filter(
                Q(payroll_period_id=payroll_period_id) & Q(employee_id=employee_id))

            if len(previous_record) > 0 and not is_excluded:
                # If the employee was excluded and is not any more...
                previous_record.delete()
            elif len(previous_record) == 0 and is_excluded:
                # If the employee was no excluded but it is now...
                new_record = EmployeePayrollPeriodExclusion(employee_id=employee_id,
                                                            payroll_period_id=payroll_period_id)
                new_record.save()

        response = {"status": "ok"}

        return HttpResponse(json.dumps(response, indent=4, separators=(',', ': '), sort_keys=False,
                                       ensure_ascii=False), 'application/json; charset=utf-8')
