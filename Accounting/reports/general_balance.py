# coding=utf-8
import StringIO
from rexec import FileWrapper

import time
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
import xlsxwriter
from django.http import StreamingHttpResponse
import os

from Accounting.models import AccountingPolicyDetail, AccountingPolicy, GroupingCode
from SharedCatalogs.models import Account


class GeneralBalanceEngine():
    SHORT_TERM_ACTIVE_LOWER = 101
    SHORT_TERM_ACTIVE_UPPER = 121

    LONG_TERM_ACTIVE_LOWER = 151
    LONG_TERM_ACTIVE_UPPER = 191

    SHORT_TERM_PASSIVE_LOWER = 201
    SHORT_TERM_PASSIVE_UPPER = 218

    LONG_TERM_PASSIVE_LOWER = 251
    LONG_TERM_PASSIVE_UPPER = 260

    ACCOUNTING_CAPITAL_LOWER = 301
    ACCOUNTING_CAPITAL_UPPER = 306

    EXCEL = 1
    PDF = 2

    def __init__(self, title, lower_account_number, upper_account_number, fiscal_period_year, fiscal_period_month,
                 only_with_transactions, only_with_balance):
        self.title = title
        self.lower_account_number = lower_account_number
        self.upper_account_number = upper_account_number
        self.fiscal_period_year = fiscal_period_year
        self.fiscal_period_month = fiscal_period_month
        if only_with_transactions is not None:
            self.only_with_transactions = bool(int(only_with_transactions))
        else:
            self.only_with_transactions = False

        if only_with_balance is not None:
            self.only_with_balance = bool(int(only_with_balance))
        else:
            self.only_with_balance = False

    def get_filtered_records(self):
        q = Q()
        if self.lower_account_number is not None:
            q &= Q(account__number__gte=self.lower_account_number)
        if self.upper_account_number is not None:
            q &= Q(account__number__lte=self.upper_account_number)
        if self.fiscal_period_year is not None:
            q &= Q(accounting_policy__fiscal_period__accounting_year=self.fiscal_period_year)
        if self.fiscal_period_month is not None:
            q &= Q(accounting_policy__fiscal_period__account_period=self.fiscal_period_month)
        return AccountingPolicyDetail.objects.filter(q)

    def generate(self):

        accumulate_dict = {}

        records = self.get_filtered_records()

        for record in records:
            account = record.account

            if account.level is None:
                # Top Level
                pass
            elif account.grouping_code.level == 1:
                # Level 1
                pass
            else:
                # Level 2, we should add the amount to credit or debit

                # First, we need to get the parent grouping code.
                # We do this by getting the number before the decimal point.
                current_grouping_code = account.grouping_code.grouping_code
                parent_grouping_code_number = int(current_grouping_code)
                parent_grouping_code = GroupingCode.objects.get(grouping_code=parent_grouping_code_number)

                # Increase debit amount for parent
                if not accumulate_dict.has_key(parent_grouping_code):
                    accumulate_dict[parent_grouping_code] = 0

                code = account.grouping_code.grouping_code

                if self.SHORT_TERM_ACTIVE_LOWER <= code <= self.LONG_TERM_ACTIVE_UPPER:
                    # 100.01 - Active
                    # Las cuentas de activo son de naturaleza deudora
                    # -- Deber aumenta su saldo
                    # -- Haber disminuye su saldo
                    accumulate_dict[parent_grouping_code] += record.debit
                    accumulate_dict[parent_grouping_code] -= record.credit
                elif self.SHORT_TERM_PASSIVE_LOWER <= code <= self.LONG_TERM_PASSIVE_UPPER:
                    # 200.01 - Passive
                    # Las cuentas de pasivo son de naturaleza acreedora
                    # -- Deber disminuye su saldo
                    # -- Haber aumenta su saldo
                    accumulate_dict[parent_grouping_code] -= record.debit
                    accumulate_dict[parent_grouping_code] += record.credit
                elif self.ACCOUNTING_CAPITAL_LOWER <= code <= self.ACCOUNTING_CAPITAL_UPPER:
                    # 300.00 - Capital
                    # Las cuentas de capital son de naturaleza crédito
                    # -- Deber disminuye su saldo
                    # -- Haber aumenta su saldo
                    accumulate_dict[parent_grouping_code] -= record.debit
                    accumulate_dict[parent_grouping_code] += record.credit

        # Now we have all the totals. Great.

        debit_accumulate = self.create_accumulative_dict(accumulate_dict)

        report_info = debit_accumulate

        response = self.generate_file(report_info, self.EXCEL)
        return response

    def create_accumulative_dict(self, dict):
        # Get Grouping Code Objects
        short_term_active = GroupingCode.objects.get(grouping_code=100.01)
        long_term_active = GroupingCode.objects.get(grouping_code=100.02)

        short_term_passive = GroupingCode.objects.get(grouping_code=200.01)
        long_term_passive = GroupingCode.objects.get(grouping_code=200.02)

        accounting_capital = GroupingCode.objects.get(grouping_code=300.00)

        response = {
            short_term_active: [],
            long_term_active: [],
            short_term_passive: [],
            long_term_passive: [],
            accounting_capital: []

        }

        if not self.only_with_transactions:
            # We have to add all the accounts that have no transactions
            accounts = Account.objects.filter(grouping_code__level=2)
            for account in accounts:
                parent_groping_code_number = int(account.grouping_code.grouping_code)
                parent_groping_code = GroupingCode.objects.get(grouping_code=parent_groping_code_number)
                if not parent_groping_code in dict.keys():
                    dict[parent_groping_code] = 0

        for (code, amount) in dict.iteritems():
            if not self.only_with_balance or amount != 0:
                if self.SHORT_TERM_ACTIVE_LOWER <= code.grouping_code <= self.SHORT_TERM_ACTIVE_UPPER:
                    # 100.01 - Short Term Active
                    response[short_term_active].append({"code": code, "amount": amount})
                elif self.LONG_TERM_ACTIVE_LOWER <= code.grouping_code <= self.LONG_TERM_ACTIVE_UPPER:
                    # 100.02 - Long Term Active
                    response[long_term_active].append({"code": code, "amount": amount})
                elif self.SHORT_TERM_PASSIVE_LOWER <= code.grouping_code <= self.SHORT_TERM_PASSIVE_UPPER:
                    # 200.01 - Short Term Passive
                    response[short_term_passive].append({"code": code, "amount": amount})
                elif self.LONG_TERM_PASSIVE_LOWER <= code.grouping_code <= self.LONG_TERM_PASSIVE_UPPER:
                    # 200.02 - Long Term Active
                    response[long_term_passive].append({"code": code, "amount": amount})
                elif self.ACCOUNTING_CAPITAL_LOWER <= code.grouping_code <= self.ACCOUNTING_CAPITAL_UPPER:
                    # 300.00 - Accounting Capital
                    response[accounting_capital].append({"code": code, "amount": amount})

        return response

    def generate_file(self, info, type):
        if type == self.EXCEL:
            response = self.generate_excel_document(info)
            return response

        if type == self.PDF:
            return self.generate_pdf_document(info)

    def generate_excel_document(self, info):
        # Get Grouping Code Objects
        short_term_active = GroupingCode.objects.get(grouping_code=100.01)
        long_term_active = GroupingCode.objects.get(grouping_code=100.02)

        short_term_passive = GroupingCode.objects.get(grouping_code=200.01)
        long_term_passive = GroupingCode.objects.get(grouping_code=200.02)

        accounting_capital = GroupingCode.objects.get(grouping_code=300.00)

        output = StringIO.StringIO()
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Get all the formats
        formats = self.get_formats(workbook)

        offset = 1  # Horizontal offset
        header_start_row = 1  # Everything else should be dynamic
        start_row = header_start_row + 6  # Everything else should be dynamic
        current_row = start_row  # Everything else should be dynamic
        active_column_width = 30
        passive_column_width = 30

        # Setup Worksheet
        worksheet.set_portrait()
        worksheet.set_paper(1)
        worksheet.fit_to_pages(1, 1)
        # Left, right, top, bottom
        worksheet.set_margins(0, 0.7, 0.75, 0.75)

        # Header
        # Insert Logo
        worksheet.insert_image(header_start_row, offset,
                               os.path.dirname(os.path.abspath(__file__)) + '/assets/images/salcedo.png',
                               {
                                   'x_offset': 80,
                                   'y_offset': 0
                               })

        worksheet.merge_range(header_start_row + 2, 1 + offset, header_start_row + 2, 4 + offset,
                              'Salcedo Construcción y Supervision SA de CV', formats['report_header'])
        worksheet.merge_range(header_start_row + 3, 1 + offset, header_start_row + 3, 4 + offset,
                              'Balance General al ' + time.strftime("%d de %B de %Y"), formats['report_header'])

        # Add the 'Active' label
        worksheet.set_column(offset, offset, active_column_width)
        worksheet.merge_range(current_row, 0 + offset, current_row, 1 + offset, 'Activo', formats['level_0_header'])

        current_row += 1
        # -- Short Term Actives Section
        # Add label
        short_term_active_label = short_term_active.account_name
        worksheet.merge_range(current_row, 0 + offset, current_row, 1 + offset, short_term_active_label,
                              formats['level_00_header'])
        current_row += 1
        # Add records.
        total_short_term_active = len(info[short_term_active])  # For readability
        short_term_active_total = 0
        for idx, record in enumerate(info[short_term_active]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + offset, ammount, formats['currency_1'])

            short_term_active_total += ammount

            current_row += 1

        # Write Totals
        short_term_active_total_row = current_row
        worksheet.write(current_row, 0 + offset, 'Total de ' + short_term_active_label, formats['level_1_total_label'])

        if total_short_term_active > 0:
            cell_value = '=SUM(' + xlsxwriter.utility.xl_col_to_name(
                1 + offset) + '' + str(
                current_row - total_short_term_active + 1) + ':' + xlsxwriter.utility.xl_col_to_name(
                1 + offset) + '' + str(current_row) + ')'
        else:
            cell_value = 0

        worksheet.write(current_row, 1 + offset, cell_value,
                        formats['currency_1'])

        current_row += 2
        # -- Long Term Actives Section
        # Add label
        long_term_active_label = long_term_active.account_name
        worksheet.merge_range(current_row, 0 + offset, current_row, 1 + offset, long_term_active_label,
                              formats['level_00_header'])
        current_row += 1
        # Add records.
        total_long_term_active = len(info[long_term_active])  # For readability
        for idx, record in enumerate(info[long_term_active]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + offset, ammount, formats['currency_1'])

            current_row += 1

        # Write Totals
        long_term_active_total_row = current_row
        worksheet.write(current_row, 0 + offset, 'Total de ' + long_term_active_label, formats['level_1_total_label'])

        if total_long_term_active > 0:
            cell_value = '=SUM(' + xlsxwriter.utility.xl_col_to_name(
                1 + offset) + '' + str(
                current_row - total_long_term_active + 1) + ':' + xlsxwriter.utility.xl_col_to_name(
                1 + offset) + '' + str(current_row) + ')'
        else:
            cell_value = 0

        worksheet.write(current_row, 1 + offset, cell_value,
                        formats['currency_1'])

        current_row += 2

        # Absolute Totals
        active_absolute_total_row = current_row
        worksheet.write(current_row, 0 + offset, 'Total de Activo', formats['level_00_total_label'])
        worksheet.write(current_row, 1 + offset, '=SUM(' + xlsxwriter.utility.xl_col_to_name(
            1 + offset) + '' + str(
            short_term_active_total_row + 1) + ',' + xlsxwriter.utility.xl_col_to_name(
            1 + offset) + '' + str(long_term_active_total_row + 1) + ')',
                        formats['currency_2'])

        current_row = start_row

        # Use to write the next sections
        passive_offset = offset + 3

        # Add the 'Passive' label
        worksheet.set_column(passive_offset, passive_offset, passive_column_width)
        worksheet.merge_range(current_row, 0 + passive_offset, current_row, 1 + passive_offset, 'Pasivo',
                              formats['level_0_header'])

        current_row += 1

        # -- Short Term Passives Section
        # Add label
        short_term_passive_label = short_term_passive.account_name
        worksheet.merge_range(current_row, 0 + passive_offset, current_row, 1 + passive_offset,
                              short_term_passive_label,
                              formats['level_00_header'])
        current_row += 1
        # Add records.
        total_short_term_passive = len(info[short_term_passive])  # For readability
        for idx, record in enumerate(info[short_term_passive]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + passive_offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + passive_offset, ammount, formats['currency_1'])

            current_row += 1

        # Write Totals
        short_term_passive_total_row = current_row
        worksheet.write(current_row, 0 + passive_offset, 'Total de ' + short_term_passive_label,
                        formats['level_1_total_label'])

        if total_short_term_active > 0:
            cell_value = '=SUM(' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(
                current_row - total_short_term_passive + 1) + ':' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(current_row) + ')'
        else:
            cell_value = 0
        worksheet.write(current_row, 1 + passive_offset, cell_value,
                        formats['currency_1'])
        current_row += 2

        # -- Long Term Pasives Section
        # Add label
        long_term_passive_label = long_term_passive.account_name
        worksheet.merge_range(current_row, 0 + passive_offset, current_row, 1 + passive_offset, long_term_passive_label,
                              formats['level_00_header'])
        current_row += 1
        # Add records.
        total_long_term_passive = len(info[long_term_passive])  # For readability
        for idx, record in enumerate(info[long_term_passive]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + passive_offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + passive_offset, ammount, formats['currency_1'])

            current_row += 1

        # Write Totals
        long_term_passive_total_row = current_row
        worksheet.write(current_row, 0 + passive_offset, 'Total de ' + long_term_passive_label,
                        formats['level_1_total_label'])

        if total_long_term_passive > 0:
            cell_value = '=SUM(' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(
                current_row - total_long_term_passive + 1) + ':' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(current_row) + ')'
        else:
            cell_value = 0

        worksheet.write(current_row, 1 + passive_offset, cell_value,
                        formats['currency_1'])

        current_row += 2

        # Absolute Totals
        passive_absolute_total_row = current_row
        worksheet.write(current_row, 0 + passive_offset, 'Total de Passivo', formats['level_00_total_label'])
        worksheet.write(current_row, 1 + passive_offset, '=SUM(' + xlsxwriter.utility.xl_col_to_name(
            1 + passive_offset) + '' + str(
            short_term_passive_total_row + 1) + ',' + xlsxwriter.utility.xl_col_to_name(
            1 + passive_offset) + '' + str(long_term_passive_total_row + 1) + ')',
                        formats['currency_2'])

        current_row += 2

        # -- Accounting Capital Section
        # Add label
        accounting_capital_label = accounting_capital.account_name
        worksheet.merge_range(current_row, 0 + passive_offset, current_row, 1 + passive_offset,
                              accounting_capital_label,
                              formats['level_0_header'])
        current_row += 1
        # Add records.
        total_accounting_capital = len(info[long_term_passive])  # For readability
        for idx, record in enumerate(info[accounting_capital]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + passive_offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + passive_offset, ammount, formats['currency_1'])

            current_row += 1

        # Write Totals
        accounting_capital_total_row = current_row
        worksheet.write(current_row, 0 + passive_offset, 'Total de Capital Contable',
                        formats['level_00_total_label'])

        if total_accounting_capital > 0:
            cell_value = '=SUM(' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(
                current_row - total_accounting_capital + 1) + ':' + xlsxwriter.utility.xl_col_to_name(
                1 + passive_offset) + '' + str(current_row) + ')'
        else:
            cell_value = 0
        worksheet.write(current_row, 1 + passive_offset, cell_value,
                        formats['currency_1'])

        current_row += 2

        worksheet.write(current_row, 0 + passive_offset, 'Capital Contable + Pasivo',
                        formats['level_00_total_label'])
        worksheet.write(current_row, 1 + passive_offset, '=SUM(' + xlsxwriter.utility.xl_col_to_name(
            1 + passive_offset) + '' + str(
            passive_absolute_total_row + 1) + ',' + xlsxwriter.utility.xl_col_to_name(
            1 + passive_offset) + '' + str(accounting_capital_total_row + 1) + ')',
                        formats['currency_1'])

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
            'blue-2': '#96C6FF'
        }
        formats = {}

        formats['level_0_header'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['gray-1']})

        formats['level_00_header'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['gray-2']})

        formats['currency_1'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '$#,##0',
            'fg_color': colors['white']})

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


def generate_pdf_document(self, info):
    pass
