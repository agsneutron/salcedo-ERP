# coding=utf-8

import json
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum, Count
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from ERP.lib.utilities import Utilities
from HumanResources.models import EmployeeAssistance, PayrollPeriod, Employee, EmployeePositionDescription, \
    EmployeeFinancialData, PayrollProcessedDetail, PayrollReceiptProcessed, ISRTable, EarningsDeductions, \
    EmployeeEarningsDeductionsbyPeriod, EmployeeEarningsDeductions, Tag, EmployeePayrollPeriodExclusion, JobInstance, \
    PayrollGroup, EmployeeLoan, EmployeeLoanDetail
from SalcedoERP.lib.SystemLog import LoggingConstants, SystemException
from reporting.lib.employee_payment_receipt import EmployeePaymentReceipt
from reporting.lib.payroll_list import PayrollListFile
from reporting.lib.earnings_deductions_totals_report import EarningsDeductionsTotalEarnings
from django.db import transaction
from django.views.generic.list import ListView

from HumanResources.search_engines.transactions_engine import TransactionsEngine


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



class GenerateEarningsDeductionsReport(View):
    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period_id')

        #Check that the parameter is provided
        if payroll_period_id is None:
            raise Exception('Se necesita enviar el parámetro payroll_period_id')

        try:
            payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)
        except ValueError as e:
            # The parameter is not an integer
            raise Exception('El parámetro payroll_period_id debe de ser de tipo entero.')
        except ObjectDoesNotExist as e:
            # The specified Payroll Group does not exist.
            raise Exception('No existe un periodo de nómina con el id ' + str(payroll_period_id))

        response = {
            'payroll_period_name': payroll_period.name,
            'payroll_group_name': payroll_period.payroll_group.name,

        }

        perception_total_fixed = 0
        perception_total_variable = 0
        # Get all the perceptions
        perceptions = EarningsDeductions.objects.filter(type=EarningsDeductions.PERCEPCION)
        perceptions_array = []
        for perception in perceptions:
            total_fixed, total_variable = perception.get_accumulated_for_period(payroll_period_id)
            total = total_fixed + total_variable
            perception_total_fixed += total_fixed
            perception_total_variable += total_variable
            total_fixed
            perception_dict = {
                "name": perception.name,
                "sat_key": perception.sat_key,
                "total_fixed": str(total_fixed),
                "total_variable": str(total_variable),
                "total": str(total),
            }
            perceptions_array.append(perception_dict)
        response['perceptions'] = perceptions_array

        # Get all the deductions
        deduction_total_fixed = 0
        deduction_total_variable = 0

        deductions = EarningsDeductions.objects.filter(type=EarningsDeductions.DEDUCCION)
        deductions_array = []
        for deduction in deductions:
            total_fixed, total_variable = deduction.get_accumulated_for_period(payroll_period_id)
            total = total_fixed + total_variable
            deduction_total_fixed += total_fixed
            deduction_total_variable += total_variable
            deduction_dict = {
                "name": deduction.name,
                "sat_key": deduction.sat_key,
                "total_fixed": str(total_fixed),
                "total_variable": str(total_variable),
                "total": str(total),
            }
            deductions_array.append(deduction_dict)
        response['deductions'] = deductions_array


        # Overall totals
        response['perception_total_fixed'] = str(perception_total_fixed)
        response['perception_total_variable'] = str(perception_total_variable)
        response['deduction_total_fixed'] = str(deduction_total_fixed)
        response['deduction_total_variable'] = str(deduction_total_variable)

        report = EarningsDeductionsTotalEarnings.generate_report(response)
        #return HttpResponse(Utilities.json_to_dumps(response),'application/json; charset=utf-8')
        return report



class DeleteAssistances(View):
    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period')
        assistances_to_delete = EmployeeAssistance.objects.filter(payroll_period=payroll_period_id)

        for assistance in assistances_to_delete:
            assistance.delete()


        return HttpResponseRedirect('/humanresources/employeebyperiod/?payrollperiod='+str(payroll_period_id))


class PayrollUtilities:

    @staticmethod
    def get_ISR_from_taxable(earnings):
        """
        Takes the total for the employee earnings and calculates its ISR taxes using the formula that SAT provides.
        :param earnings: total of earnings
        :return: total of taxes
        """

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

    @staticmethod
    def validate_employee_financial_data(employee):
        """
            Validates that the employee has Financial Data created in the system.
            :param employee: employee whose financial data we will look for.
            :return:
        """

        employee_financial_data = EmployeeFinancialData.objects.get(employee__id=employee.id)
        return True

    @staticmethod
    def generate_single_payroll(employee, payroll_period):
        """
        Generates the payroll (total earnings, total deductions, etc) for the given employee.
        :param employee: employee to work with.
        :param payroll_period: specific payroll to look for.
        :return:
        """
        total_earnings = 0
        total_deductions = 0
        total_taxable = 0
        earnings_array = []
        deductions_array = []

        receipt = {}

        receipt['base_salary'] = 0.0

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

            if(fixed_earning.concept.name == "Salario"):
                receipt['base_salary'] = float(fixed_earning.ammount)

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

        # before process the variable earnings go to search if exists pendind payments for loans
        # employee_loan_charge = EmployeeLoanDetail.objects.filter(employeeloan__employee_id=employee).filter(pay_status=False).order_by('pay_number')[:1]

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
        isr = PayrollUtilities.get_ISR_from_taxable(float(total_taxable))
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

        # Getting the info. for the employee position.
        position_array = []
        job_instance_set = JobInstance.objects.filter(employee_id=employee.id)
        for each in job_instance_set:
            position_array.append(each.job_profile.job)

        if len(position_array) > 0:
            position_string = ', '.join(position_array)
        else:
            position_string = 'Sin asignar'
        receipt['position'] = position_string


        # Adding the general data to the receipt (employee and totals).
        receipt["employee_id"] = str(employee.id)
        receipt["employee_key"] = str(employee.employee_key)
        receipt["rfc"] = str(employee.rfc)
        receipt["ssn"] = str(employee.social_security_number)
        receipt["employee_fullname"] = employee.get_full_name()
        receipt["total_earnings"] = str(total_earnings)
        receipt["total_deductions"] = str(total_deductions)

        return receipt


class GeneratePayrollReceipt(View):
    def create_earnings_deductions_historic(self, payroll_receipt_processed, concept_json):

        try:
            if concept_json["id"] != "":
                concept_id = int(concept_json["id"])
            else:
                concept_id = None

            concept = EarningsDeductions.objects.get(pk=concept_id)
            print "Concept:"
            print concept

            new_obj = PayrollProcessedDetail(
                name=concept.name,
                percent_taxable=concept.percent_taxable,
                sat_key=concept.sat_key,
                #law_type=concept.law_type,
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
            PayrollUtilities.generate_single_payroll(employee_set[0], payroll_period)

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
                    financial_data_exists = PayrollUtilities.validate_employee_financial_data(employee)

                    # If any of the employees lacks of financial data, return an error.
                    if not financial_data_exists:
                        raise Exception(
                            'Ha habido un problema generando los recibos de nómina. El empleado ' + employee.employee_key +
                            " no cuenta con datos financieros cargados en el sistema")

                    receipt = PayrollUtilities.generate_single_payroll(employee, payroll_period)
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
    def get(self, request):
        payroll_period_id = request.GET.get('payroll_period')
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payroll_receipt_processed = PayrollReceiptProcessed.objects.filter(payroll_period_id=payroll_period_id)
        print "Length " + str(len(payroll_receipt_processed))
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


class ExportPayrollList(View):
    """
        Exports the payroll list as an excel file for a given payroll group. This method does not save data
        in a historic way as the GeneratePayrollReceipt methods do. This means that the user will be able to
        export the list to see the information, before creating the final receipts.
    """
    def get(self, request):

        payroll_period_id = request.GET.get('payroll_period')

        '''
        excluded_employees_csv = request.GET.get('employeesSelected')
        if excluded_employees_csv == "":
            excluded_employees = []
        else:
            excluded_employees = get_array_or_none(excluded_employees_csv)
        '''


        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)



        # Getting the employee object for batch generation.
        payroll_group = payroll_period.payroll_group

        # Getting all the position descriptions related to the payroll group.
        position_description_set = EmployeePositionDescription.objects.filter(payroll_group_id=payroll_group.id)


        # Employees to be excluded.
        excluded_employees = []
        exclusion_set = EmployeePayrollPeriodExclusion.objects.filter(payroll_period=payroll_period)
        for exclusion in exclusion_set:
            excluded_employees.append(exclusion.employee.id)

        # Array to control employees data set.
        employee_array = []

        for position_description in position_description_set:
            employee_array.append(position_description.employee.id)

        # Getting all the employees realted to the found payroll groups.
        employee_set = Employee.objects.filter(Q(id__in=employee_array)).exclude(id__in=excluded_employees)

        # Generating the payroll for every single employee.
        payroll_array = []

        try:

            for employee in employee_set:
                financial_data_exists = PayrollUtilities.validate_employee_financial_data(employee)

                # If any of the employees lacks of financial data, return an error.
                if not financial_data_exists:
                    raise Exception(
                        'Ha habido un problema exportando el listado nominal. El empleado ' + employee.employee_key +
                        " no cuenta con datos financieros cargados en el sistema")

                single_payroll = PayrollUtilities.generate_single_payroll(employee, payroll_period)
                payroll_array.append(single_payroll)

            payroll_list_file = PayrollListFile.generate_payroll_list(payroll_array)

            '''
            return HttpResponse(
                json.dumps(payroll_array, indent=4, separators=(',', ': '), sort_keys=False,
                           ensure_ascii=False),
                'application/json; charset=utf-8')
            '''
            return payroll_list_file


        except Exception as e:
            print "Exception was: " + str(e)
            django.contrib.messages.error(request, "Hubo un error al exportar la Lista Nominal.")
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


class SearchTransactionsByEmployee(ListView):
    def get_values_PayrollProcessedDetail(self, transactions):
        grouped = transactions.values('payroll_receip_processed__payroll_period__year', 'payroll_receip_processed__payroll_period__month', 'payroll_receip_processed__payroll_period__name',
                                      'payroll_receip_processed__employee__employee_key','payroll_receip_processed__employee__name','payroll_receip_processed__employee__rfc',
                                      'name','amount','type')

        return grouped

    def exclude_debit_limits(self, lower_debit, upper_debit, grouped_transactions):
        if lower_debit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_debit__lt=lower_debit))

        if upper_debit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_debit__gt=upper_debit))

        return grouped_transactions

    def exclude_credit_limits(self, lower_credit, upper_credit, grouped_transactions):
        if lower_credit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_credit__lt=lower_credit))

        if upper_credit is not None:
            grouped_transactions = grouped_transactions.exclude(Q(total_credit__gt=upper_credit))

        return grouped_transactions

    def get(self, request, *args, **kwargs):
        fiscal_period_year = request.GET.get('fiscal_period_year')

        fiscal_period_month = request.GET.get('fiscal_period_month')

        employee_key = request.GET.get('employee_key')
        name = request.GET.get('name')
        rfc = request.GET.get('rfc')

        # If the account number is set, the range is ignored.
        account_number_array = get_array_or_none(request.GET.get('account'))

        engine = TransactionsEngine(
            fiscal_period_year=fiscal_period_year,
            fiscal_period_month=fiscal_period_month,
            employee_key=employee_key,
            name=name,
            rfc=rfc,
            only_with_transactions=False,

        )

        transactions = engine.search_transactions()

        # Grouping all the transactions by accounts.
        grouped_transactions = self.get_values_PayrollProcessedDetail(transactions)

        response = {
            'accounts': []
        }

        'payroll_receip_processed__payroll_period__year', 'payroll_receip_processed__payroll_period__month', 'payroll_receip_processed__payroll_period__name',
        'payroll_receip_processed__employee__employee_key', 'payroll_receip_processed__employee__name', 'payroll_receip_processed__employee__rfc',
        'name', 'amount', 'type'

        for account in grouped_transactions:
            response['accounts'].append({
                'payroll_period_year': account['payroll_receip_processed__payroll_period__year'],
                'payroll_period_month': account['payroll_receip_processed__payroll_period__month'],
                'payroll_period_name': str(account['payroll_receip_processed__payroll_period__name']),
                'employee_key': account['payroll_receip_processed__employee__employee_key'],
                'employee_name': account['payroll_receip_processed__employee__name'],
                'employee_rfc': account['payroll_receip_processed__employee__rfc'],
                'payrollprocesseddetail_name': account['name'],
                'amount': account['amount'],
                'type': account['type'],
            })

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8', )

class GenerateTransactionsByAccountReport(ListView):
    def create_general_structure(self, report_title, year, month, employee):


        if report_title is None or report_title is "":
            title = "Transacciones del empleado " + str(employee.employee_key) + " " + employee.name
        else:
            title = report_title

        general_structure = {
            'report_title': title,
            'fiscal_period_year': year,
            'fiscal_period_month': month,
            'employee_key': str(employee.employee_key),
            'account_name': employee.name,
            'rfc': employee.rfc,
            'transactions': []
        }

        return general_structure

    def create_transaction_structure(self, transaction_info):

        account_structure = {
            'name': transaction_info.name,
            'amount': transaction_info.amount,
            'type': transaction_info.type
        }

        return account_structure

    def get(self, request, *args, **kwargs):
        fiscal_period_year = request.GET.get('fiscal_period_year')
        fiscal_period_month = request.GET.get('fiscal_period_month')
        employee_key = request.GET.get('employee_key')
        name = request.GET.get('name')
        rfc = request.GET.get('rfc')
        report_title = request.GET.get('report_title')

        # If the account number is set, the range is ignored.
        employee_key_array = get_array_or_none(request.GET.get('employee_key'))

        engine = TransactionsEngine(
            fiscal_period_year=fiscal_period_year,
            fiscal_period_month=fiscal_period_month,
            employee_key=employee_key,
            name = name,
            rfc = rfc,
            only_with_transactions=False,
            employee_array=employee_key_array
        )

        transactions_set = engine.search_transactions()

        # Getting the account number.
        employee = employee_key_array[0]

        # Getting the account object.
        employee_object = Employee.objects.get(employee_key=employee)

        # Creating the general structure for the response.
        general_structure = self.create_general_structure(
            report_title,
            fiscal_period_year,
            fiscal_period_month,
            employee_object
        )

        # Accumulated amounts.
        total_amount = 0

        # Creating the structure for each of the accounts.
        for transaction in transactions_set:
            total_amount += transaction.amount
            transaction_structure = self.create_transaction_structure(transaction)
            general_structure['transactions'].append(transaction_structure)

        # Assigning the accumulated amounts.
        general_structure['total_amount'] = total_amount


        return engine.generate_report(general_structure)

        # return HttpResponse(Utilities.json_to_dumps(general_structure) , 'application/json; charset=utf-8', )