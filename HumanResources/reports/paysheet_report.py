# coding=utf-8
from django.db.models.aggregates import Count, Sum

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook

from Accounting.models import FiscalPeriod
from HumanResources.models import EmployeeContract


class PaySheetReport():

    @staticmethod
    def generate_report(general_data, paysheet_details_set):
        """
        Entry point to generate the trial report.

        :param general_data: General Data for the report, such as Fiscal Period, Year, etc.
        :param policies_details_set: Set of policy details to be processed.
        :return: HttpResponse containing the downloadable file.
        """

        output = StringIO.StringIO()
        workbook = Workbook(output)
        worksheet = workbook.add_worksheet('Nómina')


        if len(paysheet_details_set) == 0:
            # Widen the first column to make the text clearer.
            #worksheet.write('A1', 'No se encontraron datos pertenecientes al periodo.')
            pass


        else:
            PaySheetReport.add_headers(workbook, worksheet, general_data)
            PaySheetReport.add_paysheet_details(workbook, worksheet, paysheet_details_set)



        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Datos_para_CFD.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response


    @staticmethod
    def add_headers(workbook, worksheet, general_data):
        """
        Adds the necessary headers to the worksheet.

        :param workbook: Workbook Object.
        :param worksheet: Worksheet Object.
        :param general_data: Data to set info in the headers section.
        """

        formats = PaySheetReport.get_formats(workbook)

        # Formats
        blue_header_format_info = formats['blue_header_format_info']
        white_centered_bold_header = formats['white_centered_bold_header']
        white_bold_header = formats['white_bold_header']


        worksheet.set_column('A:G', 20)


        # Row 1.
        if general_data['title'] is None or general_data['title'] == "":
            title = "Balance de Comprobación de Sumas y Saldos"
        else:
            title = general_data['title']

        worksheet.merge_range('A1:G1', title, white_centered_bold_header)

        # Row 2.
        worksheet.merge_range('A2:C2', "Salcedo Construcción y Supervisión", white_bold_header)
        # Line Commented until definition of CUIT.
        #worksheet.merge_range('D2:F2', "CUIT", white_bold_header)

        # Row 3.
        '''month_number = int(general_data['month'])
        year_number = int(general_data['year'])'''

        worksheet.merge_range('A3:C3', FiscalPeriod.get_month_name_from_number(7) + " " + str(2018), white_bold_header)

        COUNTER_COL = 0
        PAYMENT_DATE_COL = 1
        EMPLOYEE_KEY_COL = 2
        WORKED_DAYS_COL = 3
        DAILY_SALARY_COL = 5
        TOTAL_PAYROLL_COL = 6
        CONTRACT_KEY_COL = 7
        TAX_REGIME_COL = 8


        # Table headers.
        worksheet.write('A5', "No.", blue_header_format_info)
        worksheet.write('B5', "FechaD", blue_header_format_info)
        worksheet.write('C5', "FechaA", blue_header_format_info)
        worksheet.write('D5', "Fecha Pago", blue_header_format_info)
        worksheet.write('E5', "Contacto", blue_header_format_info)
        worksheet.write('F5', "Dias Pagados", blue_header_format_info)
        worksheet.write('G5', "Concepto", blue_header_format_info)
        worksheet.write('H5', "Movimiento", blue_header_format_info)
        worksheet.write('I5', "Gravado", blue_header_format_info)
        worksheet.write('J5', "Exento", blue_header_format_info)
        worksheet.write('K5', "INCAPACIDADDIAS", blue_header_format_info)
        worksheet.write('L5', "INCAPACIDADTIPO", blue_header_format_info)
        worksheet.write('M5', "INCAPACIDADDESCUENTO", blue_header_format_info)
        worksheet.write('N5', "HORASEXTRASDIAS", blue_header_format_info)
        worksheet.write('O5', "HORASEXTRASHORAS", blue_header_format_info)
        worksheet.write('P5', "HORASEXTRASTIPO", blue_header_format_info)
        worksheet.write('Q5', "HORASEXTRASIMPORTE", blue_header_format_info)
        worksheet.write('R5', "Salario Diario", blue_header_format_info)
        worksheet.write('S5', "SDI", blue_header_format_info)
        worksheet.write('T5', "FECHAANTIGUEDAD", blue_header_format_info)
        worksheet.write('U5', "FECHAALTA", blue_header_format_info)
        worksheet.write('V5', "RIMSSPATRON", blue_header_format_info)
        worksheet.write('W5', "CENTROCOSTOS", blue_header_format_info)
        worksheet.write('X5', "PUESTO", blue_header_format_info)
        worksheet.write('Y5', "DEPARTAMENTO", blue_header_format_info)
        worksheet.write('Z5', "GRUPO", blue_header_format_info)
        worksheet.write('AA5', "Contrato", blue_header_format_info)
        worksheet.write('AB5', "Tipo Regimen", blue_header_format_info)
        worksheet.write('AC5', "Jornada", blue_header_format_info)
        worksheet.write('AD5', "Periodicidad Pago", blue_header_format_info)
        worksheet.write('AE5', "Forma Pago", blue_header_format_info)
        worksheet.write('AF5', "Tipo Nómina", blue_header_format_info)
        worksheet.write('AG5', "Riesgo Puesto", blue_header_format_info)
        worksheet.write('AH5', "Subsidio Causado", blue_header_format_info)


    @staticmethod
    def get_formats(workbook):
        formats = {}

        # Format with blue background and white letters.
        blue_header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#3E84CF',
            'border_color': '#000000',
            'font_color': '#FFFFFF'
        }
        formats['blue_header_format_info'] = workbook.add_format(blue_header_format_info)

        # Format with white background and bold centered text.
        white_centered_bold_header_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1
        }
        formats['white_centered_bold_header'] = workbook.add_format(white_centered_bold_header_info)

        # Format with white background and bold text aligned to the left.
        white_bold_header_info = {
            'align': 'left',
            'valign': 'vcenter',
            'bold': 1
        }
        formats['white_bold_header'] = workbook.add_format(white_bold_header_info)

        # Format with white background and bold text aligned to the left with black border.
        white_bold_record_info = {
            'align': 'left',
            'valign': 'vcenter',
            'bold': 1,
            'border': 1,
            'border_color':'#000000'
        }
        formats['white_bold_record'] = workbook.add_format(white_bold_record_info)

        # Format with white background and bold text aligned to the right with black border for currency.
        white_bold_right_currency_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'num_format': '$#,#00.00',
            'bold':1
        }
        formats['white_bold_right_currency'] = workbook.add_format(white_bold_right_currency_info)

        # Format with gray background and bold text aligned to the right with black border for currency.
        gray_bold_right_currency_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'num_format': '$#,#00.00',
            'bold': 1,
            'fg_color':'#E8E8E8'
        }
        formats['gray_bold_right_currency'] = workbook.add_format(gray_bold_right_currency_info)

        gray_bold_right_date_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'num_format': 'dd/mm/yyyy',
            'bold': 1,
            'fg_color': '#E8E8E8'
        }
        formats['gray_bold_right_date'] = workbook.add_format(gray_bold_right_date_info)



        # Format with yellow background and bold text aligned to the right.
        yellow_total_right_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'bold': 1,
            'fg_color': '#FDB709'
        }
        formats['yellow_total_right'] = workbook.add_format(yellow_total_right_info)


        return formats


    @staticmethod
    def add_paysheet_details(workbook, worksheet, paysheet_detail_set):
        """
        Takes a set of policy details and processes it to define the amount of debit and credit related to an
         account.

        :param workbook: Workbook Object.
        :param worksheet: Worksheet Object.
        :param policies_set: Set of policies that were found for the given fiscal period and account ranges.

        """
        START_ROW = 5

        COUNTER_COL = 0
        INICTIAL_DATE_COL = 1
        FINAL_DATE_COL = 2
        PAYMENT_DATE_COL = 3
        EMPLOYEE_KEY_COL = 4
        WORKED_DAYS_COL = 5
        CONCEPT_KEY_COL = 6
        MOVEMENT_COL = 7
        EXEMPT_COL=8
        TAXABLE_COL = 9
        INABILITY_DAYS_COL =10
        INABILITY_TYPE_COL = 11
        INABILITY_DISCOUNT_COL = 12
        EXTRAHOURS_DAY_COL=13
        EXTRAHOURS_HOURS_COL=14
        EXTRAHOURS_TYPE_COL=15
        EXTRAHOURS_AMOUNT_COL=16
        DAILY_SALARY_COL = 17
        TOTAL_PAYROLL_COL = 18
        DATE_ANTIQUETY_COL = 19
        DATE_START_COL = 20
        RIMSSPATRON_COL = 21
        COST_CENTER_COL =22
        PROFILE_COL = 23
        DEPARTMENT_COL = 24
        GROUP_COL = 25
        CONTRACT_KEY_COL = 26
        TAX_REGIME_COL = 27
        WORKINGDAY_COL = 28
        FREQUENCY_COL = 29
        WAYTOAY_COL =30
        PAYROLLTYPE_COL=31
        RISK_TYPE_COL = 32
        SUBSIDY_COL = 33


        # Getting the formats.
        formats = PaySheetReport.get_formats(workbook)
        white_bold_record = formats['white_bold_record']
        white_bold_right_currency = formats['white_bold_right_currency']
        gray_bold_right_currency = formats['gray_bold_right_currency']
        yellow_total_right = formats['yellow_total_right']
        gray_bold_right_date = formats['gray_bold_right_date']


        paysheet_detail_qry_set = paysheet_detail_set.values('payroll_receip_processed__payment_date','payroll_receip_processed__employee__employee_key','payroll_receip_processed__worked_days','payroll_receip_processed__daily_salary','payroll_receip_processed__total_payroll',
                                                                     'payroll_receip_processed__employee__tax_regime__id','payroll_receip_processed__employee__employeecontract__contract_key',
                                                             'earningdeduction_key','type','taxable','amount','payroll_receip_processed__employee__risk_type','payroll_receip_processed__employee__employeedata__aggregate_daily_salary',
                                                             'payroll_receip_processed__employee__employeepositiondescription__job_profile__job','payroll_receip_processed__employee__employeepositiondescription__department__name',
                                                             'payroll_receip_processed__employee__employeepositiondescription__direction__id','payroll_receip_processed__payroll_period__start_period','payroll_receip_processed__payroll_period__end_period',
                                                             'payroll_receip_processed__employee__registry_date')

        row_counter = START_ROW
        counter = 1
        exempt = 0
        taxable = 0
        for record in paysheet_detail_qry_set:

            if record['taxable'] == 'NO':
                exempt = record['amount']
            else:
                taxable = record['amount']
            worksheet.write(row_counter, COUNTER_COL, counter, white_bold_record)
            worksheet.write(row_counter, INICTIAL_DATE_COL, record['payroll_receip_processed__payroll_period__start_period'],gray_bold_right_date)
            worksheet.write(row_counter, FINAL_DATE_COL, record['payroll_receip_processed__payroll_period__end_period'],gray_bold_right_date)
            worksheet.write(row_counter, PAYMENT_DATE_COL, record['payroll_receip_processed__payment_date'], gray_bold_right_date)
            worksheet.write(row_counter, EMPLOYEE_KEY_COL, record['payroll_receip_processed__employee__employee_key'], white_bold_record)
            worksheet.write(row_counter, WORKED_DAYS_COL, record['payroll_receip_processed__worked_days'], white_bold_right_currency)
            worksheet.write(row_counter, CONCEPT_KEY_COL, record['earningdeduction_key'],white_bold_right_currency)
            worksheet.write(row_counter, MOVEMENT_COL, record['type'], white_bold_right_currency)
            worksheet.write(row_counter, TAXABLE_COL, taxable, white_bold_right_currency)
            worksheet.write(row_counter, EXEMPT_COL, exempt, white_bold_right_currency)
            worksheet.write(row_counter, DAILY_SALARY_COL, record['payroll_receip_processed__daily_salary'], white_bold_right_currency)
            worksheet.write(row_counter, TOTAL_PAYROLL_COL, record['payroll_receip_processed__employee__employeedata__aggregate_daily_salary'], gray_bold_right_currency)

            worksheet.write(row_counter, DATE_START_COL, record['payroll_receip_processed__employee__registry_date'],gray_bold_right_date)

            worksheet.write(row_counter, COST_CENTER_COL,record['payroll_receip_processed__employee__employeepositiondescription__direction__id'],white_bold_record)
            worksheet.write(row_counter, PROFILE_COL, record['payroll_receip_processed__employee__employeepositiondescription__job_profile__job'],white_bold_record)
            worksheet.write(row_counter, DEPARTMENT_COL, record['payroll_receip_processed__employee__employeepositiondescription__department__name'],white_bold_record)

            worksheet.write(row_counter, CONTRACT_KEY_COL,record['payroll_receip_processed__employee__employeecontract__contract_key'],gray_bold_right_currency)
            worksheet.write(row_counter, TAX_REGIME_COL, record['payroll_receip_processed__employee__tax_regime__id'], white_bold_record)
            worksheet.write(row_counter, WORKINGDAY_COL, '02', white_bold_record)
            worksheet.write(row_counter, FREQUENCY_COL, '01', white_bold_record)
            worksheet.write(row_counter, WAYTOAY_COL, '01', white_bold_record)
            worksheet.write(row_counter, PAYROLLTYPE_COL, '04', white_bold_record)
            worksheet.write(row_counter, RISK_TYPE_COL, record['payroll_receip_processed__employee__risk_type'],white_bold_record)
            worksheet.write(row_counter, SUBSIDY_COL, '0', white_bold_record)

            row_counter += 1
            counter += 1





