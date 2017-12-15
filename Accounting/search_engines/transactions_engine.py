# coding=utf-8
import StringIO
import os
from rexec import FileWrapper

import time
import xlsxwriter
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http import StreamingHttpResponse

from Accounting.models import AccountingPolicyDetail, AccountingPolicy


class TransactionsEngine():
    def __init__(self,
                 lower_fiscal_period_year=None,
                 upper_fiscal_period_year=None,
                 lower_fiscal_period_month=None,
                 upper_fiscal_period_month=None,
                 type_policy_array=None,
                 lower_folio=None,
                 upper_folio=None,
                 lower_registry_date=None,
                 upper_registry_date=None,
                 description=None,
                 lower_account_number=None,
                 upper_account_number=None,
                 lower_debit=None,
                 upper_debit=None,
                 lower_credit=None,
                 upper_credit=None,
                 reference=None,
                 only_with_transactions=None,
                 account_array=None
                 ):

        self.lower_fiscal_period_year = lower_fiscal_period_year
        self.upper_fiscal_period_year = upper_fiscal_period_year

        self.lower_fiscal_period_month = lower_fiscal_period_month
        self.upper_fiscal_period_month = upper_fiscal_period_month

        self.type_policy_array = type_policy_array

        self.lower_folio = lower_folio
        self.upper_folio = upper_folio

        self.lower_registry_date = lower_registry_date
        self.upper_registry_date = upper_registry_date

        self.description = description

        self.lower_account_number = lower_account_number
        self.upper_account_number = upper_account_number

        self.lower_debit = lower_debit
        self.upper_debit = upper_debit

        self.lower_credit = lower_credit
        self.upper_credit = upper_credit

        self.reference = reference

        self.only_with_transactions = only_with_transactions

        self.account_array = account_array

    def search_transactions(self):
        query = Q()

        if self.lower_fiscal_period_year is not None:
            query &= Q(accounting_policy__fiscal_period__accounting_year__gte=self.lower_fiscal_period_year)

        if self.upper_fiscal_period_year is not None:
            query &= Q(accounting_policy__fiscal_period__accounting_year__lte=self.upper_fiscal_period_year)

        if self.lower_fiscal_period_month is not None:
            query &= Q(accounting_policy__fiscal_period__account_period__gte=self.lower_fiscal_period_month)

        if self.upper_fiscal_period_month is not None:
            query &= Q(accounting_policy__fiscal_period__account_period__lte=self.upper_fiscal_period_month)

        if self.type_policy_array is not None:
            query &= Q(accounting_policy__type_policy__id__in=self.type_policy_array)

        if self.lower_folio is not None:
            query &= Q(accounting_policy__folio__gte=self.lower_folio)

        if self.upper_folio is not None:
            query &= Q(accounting_policy__folio__lte=self.upper_folio)

        if self.lower_registry_date is not None:
            query &= Q(accounting_policy__registry_date__gte=self.lower_registry_date)

        if self.upper_registry_date is not None:
            query &= Q(accounting_policy__registry_date__lte=self.upper_registry_date)

        if self.description is not None:
            query &= Q(accounting_policy__description__icontains=self.description)

        if self.lower_account_number is not None and self.account_array is None:
            query &= Q(account__number__gte=self.lower_account_number)

        if self.upper_account_number is not None and self.account_array is None:
            query &= Q(account__number__lte=self.lower_account_number)

        if self.lower_debit is not None:
            query &= Q(debit__gte=self.lower_debit)

        if self.upper_debit is not None:
            query &= Q(debit__lte=self.upper_debit)

        if self.lower_credit is not None:
            query &= Q(credit__gte=self.lower_credit)

        if self.upper_credit is not None:
            query &= Q(credit__lte=self.upper_credit)

        if self.reference is not None:
            query &= Q(accounting_policy__reference__icontains=self.reference)

        if self.account_array is not None:
            query &= Q(account__number__in=self.account_array)

        results = AccountingPolicyDetail.objects.filter(query)

        return results

    def get_test_data(self):
        response = {"fiscal_period_year": 2017, "fiscal_period_month": "Septiembre", "account_number": 1231238,
                    "account_id": 132, "account_name": "Cool Account", "parent_account_name": "Super Parent",
                    "parent_account_number": "666", "grouping_code": 119.01,
                    "grouping_code_name": "Gastos Innecesarios"}

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

    def generate_report(self):
        data = self.get_test_data()

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
        current_row += 4
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

        response['Content-Disposition'] = 'attachment; filename=Balanza_de_Comprobación.xlsx'
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

        formats['report_header'] = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'color': colors['white'],
            'fg_color': colors['blue-1']})

        return formats
