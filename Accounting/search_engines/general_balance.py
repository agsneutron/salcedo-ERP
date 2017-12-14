# coding=utf-8
import StringIO
from rexec import FileWrapper

from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
import xlsxwriter
from django.http import StreamingHttpResponse

from Accounting.models import AccountingPolicyDetail, AccountingPolicy, GroupingCode


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

    def __init__(self):
        pass

    def generate(self):

        accumulate_dict = {}

        records = AccountingPolicyDetail.objects.all()

        for record in records:
            account = record.account
            print record.account.grouping_code

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
                print 'Parent ' + str(parent_grouping_code)

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

        print 'Accumulate'
        print accumulate_dict

        # Now we have all the totals. Great.

        debit_accumulate = self.create_accumulative_dict(accumulate_dict)

        report_info = debit_accumulate
        print report_info

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

        for (code, amount) in dict.iteritems():
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
        start_row = 9  # Everything else should be dynamic
        current_row = start_row  # Everything else should be dynamic
        active_column_width = 20
        passive_column_width = 30

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
        for idx, record in enumerate(info[short_term_active]):
            name = record['code'].account_name
            ammount = record['amount']

            worksheet.write(current_row, 0 + offset, name, formats['level_1_label'])
            worksheet.write(current_row, 1 + offset, ammount, formats['currency_1'])

            current_row += 1

        current_row += 1
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

        current_row = start_row

        passive_offset = offset + 3

        # Add the 'Passive' label
        worksheet.set_column(passive_offset, passive_offset, passive_column_width)
        worksheet.merge_range(current_row, 0 + passive_offset, current_row, 1 + passive_offset, 'Pasivo', formats['level_0_header'])

        current_row += 1

        # -- Short Term Pasives Section
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

        current_row += 1
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

        #
        # # Widen the first column to make the text clearer.
        # worksheet.set_column('A:A', 20)
        #
        # # Add a bold format to use to highlight cells.
        # bold = workbook.add_format({'bold': True})
        #
        # # Write some simple text.
        # worksheet.write('A1', 'Hello')
        #
        # # Text with formatting.
        # worksheet.write('A2', 'World', bold)
        #
        # # Write some numbers, with row/column notation.
        # worksheet.write(2, 0, 123)
        # worksheet.write(3, 0, 123.456)
        #
        # # Insert an image.
        # worksheet.insert_image('B5', 'logo.png')
        #




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
            'white': '#FFFFFF',
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
            'fg_color': colors['white']})

        formats['currency_1'] = workbook.add_format({
            'border': 1,
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

        return formats


def generate_pdf_document(self, info):
    pass
