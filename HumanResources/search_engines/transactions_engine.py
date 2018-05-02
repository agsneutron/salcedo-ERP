# coding=utf-8
import StringIO
import os
from rexec import FileWrapper

import time
import xlsxwriter
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http import StreamingHttpResponse

from HumanResources.models import PayrollProcessedDetail, PayrollReceiptProcessed


class TransactionsEngine():
    def __init__(self,
                 fiscal_period_year=None,
                 fiscal_period_month=None,
                 employee_key=None,
                 name=None,
                 rfc=None,
                 only_with_transactions=None,
                 ):

        self.fiscal_period_year = fiscal_period_year
        self.fiscal_period_month = fiscal_period_month
        self.employee_key = employee_key
        self.name = name
        self.rfc = rfc



        self.only_with_transactions = only_with_transactions


    def search_transactions(self):
        query = Q()

        if self.fiscal_period_year is not None:
            query &= Q(payroll_receip_processed__payroll_period__year=self.fiscal_period_year)

        if self.fiscal_period_month is not None:
            query &= Q(payroll_receip_processed__payroll_period__month=self.fiscal_period_month)


        if self.employee_key is not None:
            query &= Q(payroll_receip_processed__employee__employee_key__icontains=self.employee_key)
        if self.name is not None:
            query &= Q(payroll_receip_processed__employee__name__icontains=self.name)
        if self.rfc is not None:
            query &= Q(payroll_receip_processed__employee__rfc__icontains=self.rfc)

        results = PayrollProcessedDetail.objects.filter(query)

        return results

    def get_test_data(self):
        response = {"fiscal_period_year": 2017, "fiscal_period_month": "Septiembre", "account_number": 1231238,
                    "account_id": 132, "account_name": "Cool Account", "parent_account_name": "Super Parent",
                    "parent_account_number": "666", "grouping_code": 119.01,
                    "grouping_code_name": "Gastos Innecesarios",
                    "total_debit": 10000, "total_credit": 20000, "report_title": "Transacciones_por_cuenta"}

        transactions = []
        transactions += self.get_test_transactions()
        transactions += self.get_test_transactions()
        transactions += self.get_test_transactions()
        transactions += self.get_test_transactions()

        response["transactions"] = transactions

        return response

    def get_test_transactions(self):
        response = [
            {
                "description": "Movimiento a caja chica",
                "debit": 1000,
                "credit": 0,
                "policy_folio": 144,
                "policy_type": "Ingresos",
            },
            {
                "description": "Compra de computadoras",
                "debit": 0,
                "credit": 12000,
                "policy_folio": 145,
                "policy_type": "Egresos",
            }
        ]
        return response

    def generate_report(self, data):
        #data = self.get_test_data()

        output = StringIO.StringIO()

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Get all the formats
        formats = self.get_formats(workbook)

        offset = 0  # Horizontal offset
        header_start_row = 1  # Everything else should be dynamic
        start_row = header_start_row + 6  # Everything else should be dynamic
        current_row = start_row  # Everything else should be dynamic
        active_column_width = 30
        passive_column_width = 30

        '''
            Header section
        '''
        # Insert Logo
        worksheet.insert_image(header_start_row, offset,
                               os.path.dirname(os.path.abspath(__file__)) + '/assets/images/salcedo.png',
                               {
                                   'x_offset': 50,
                                   'y_offset': 0
                               })

        worksheet.merge_range(header_start_row + 2, 2 + offset, header_start_row + 2, 5 + offset,
                              'Salcedo Construcción y Supervision SA de CV', formats['report_header'])
        worksheet.merge_range(header_start_row + 3, 2 + offset, header_start_row + 3, 5 + offset,
                              'Movimientos de Cuenta', formats['report_header'])

        date_label = time.strftime("%d de %B de %Y")

        # Widths
        label_column_width = 30
        value_column_width = 20

        worksheet.set_column(offset + 0, offset + 2, 5)  # Number
        worksheet.set_column(offset + 1, offset + 3, 26)  # Description
        worksheet.set_column(offset + 2, offset + 4, 13)  # Debit
        worksheet.set_column(offset + 3, offset + 5, 13)  # Credit
        worksheet.set_column(offset + 4, offset + 6, 12)  # Policy Folio
        worksheet.set_column(offset + 5, offset + 7, 25)  # Policy Type

        '''
            General info
        '''

        # Account Number
        worksheet.merge_range(current_row, offset, current_row, 1 + offset,
                              "Número de Cuenta", formats['info_label'])

        worksheet.write(current_row, 2 + offset, data['account_number'], formats['number_1'])

        # Account Name
        worksheet.merge_range(current_row, 3 + offset, current_row, 4 + offset,
                              "Nombre de Cuenta", formats['info_label'])
        worksheet.write(current_row, 5 + offset, data['account_name'], formats['number_1'])

        current_row += 1

        # Grouping Code
        worksheet.merge_range(current_row, offset, current_row, 1 + offset,
                              "Código Agrupador", formats['info_label'])
        worksheet.write(current_row, 2 + offset, data['grouping_code'], formats['number_1'])

        # Grouping Code Name
        worksheet.merge_range(current_row, 3 + offset, current_row, 4 + offset,
                              "Tipo de Cuenta", formats['info_label'])

        worksheet.write(current_row, 5 + offset, data['grouping_code_name'], formats['number_1'])

        current_row += 1

        # Parent Account Number
        worksheet.merge_range(current_row, offset, current_row, 1 + offset,
                              "Número de Cuenta Padre", formats['info_label'])
        worksheet.write(current_row, 2 + offset, data['parent_account_number'], formats['number_1'])

        # Parent Account Name
        worksheet.merge_range(current_row, 3 + offset, current_row, 4 + offset,
                              "Nombre de la Cuenta Padre", formats['info_label'])
        worksheet.write(current_row, 5 + offset, data['parent_account_name'], formats['number_1'])

        current_row += 1

        # Fiscal Period Month
        worksheet.merge_range(current_row, offset, current_row, 1 + offset,
                              "Mes Fiscal", formats['info_label'])
        worksheet.write(current_row, 2 + offset, data['fiscal_period_month'], formats['number_1'])
        # Fiscal Period Year
        worksheet.merge_range(current_row, 3 + offset, current_row, 4 + offset,
                              "Año Fiscal", formats['info_label'])

        worksheet.write(current_row, 5 + offset, data['fiscal_period_year'], formats['number_1'])

        '''
            Transactions Section
        '''

        current_row += 2
        worksheet.write(current_row, 4 + offset, "Total Debe", formats['report_header'])
        worksheet.write(current_row, 5 + offset, data['total_debit'], formats['currency_1'])
        current_row += 1
        worksheet.write(current_row, 4 + offset, "Total Haber", formats['report_header'])
        worksheet.write(current_row, 5 + offset, data['total_credit'], formats['currency_1'])

        current_row += 1
        # Headers
        worksheet.write(current_row, offset, '#', formats['info_label'])
        worksheet.write(current_row, 1 + offset, 'Descripción', formats['info_label'])
        worksheet.write(current_row, 2 + offset, 'Debe', formats['info_label'])
        worksheet.write(current_row, 3 + offset, 'Haber', formats['info_label'])
        worksheet.write(current_row, 4 + offset, 'Póliza', formats['info_label'])
        worksheet.write(current_row, 5 + offset, 'Tipo de Póliza', formats['info_label'])

        current_row += 1
        for idx, transaction in enumerate(data['transactions']):
            worksheet.write(current_row, offset, idx + 1, formats['light_label'])
            worksheet.write(current_row, 1 + offset, transaction['description'], formats['data_1'])
            worksheet.write(current_row, 2 + offset, transaction['debit'], formats['currency_1'])
            worksheet.write(current_row, 3 + offset, transaction['credit'], formats['currency_1'])
            worksheet.write(current_row, 4 + offset, transaction['policy_folio'], formats['data_1'])
            worksheet.write(current_row, 5 + offset, transaction['policy_type'], formats['data_1'])

            current_row += 1

        workbook.close()

        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=' + data['report_title'] + '.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    def get_formats(self, workbook):

        colors = {
            'gray-1': '#E7E7E7',
            'gray-2': '#F9F9F9',
            'white': '#FFFFFF',
            'blue-1': '#0E156C',
            'blue-2': '#96C6FF',
            'blue-3': '#00bcd4'
        }
        formats = {}

        formats['info_label'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['gray-1']})

        formats['light_label'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'color': colors['white'],
            'fg_color': colors['blue-3']})

        formats['number_1'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['white']})

        formats['data_1'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['white']})

        formats['currency_1'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'fg_color': colors['white']})

        formats['report_header'] = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'color': colors['white'],
            'fg_color': colors['blue-1']})

        ## old

        formats['level_00_header'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['gray-2']})

        formats['currency_2'] = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'fg_color': colors['white']})

        formats['level_1_label'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'fg_color': colors['white']})

        formats['level_1_total_label'] = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'fg_color': colors['gray-2']})

        formats['level_00_total_label'] = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'color': colors['white'],
            'fg_color': colors['blue-1']})

        return formats
