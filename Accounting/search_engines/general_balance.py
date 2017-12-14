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
                if not accumulate_dict.has_key(parent_grouping_code_number):
                    accumulate_dict[parent_grouping_code_number] = 0

                code = account.grouping_code.grouping_code

                if self.SHORT_TERM_ACTIVE_LOWER <= code <= self.LONG_TERM_ACTIVE_UPPER:
                    # 100.01 - Active
                    # Las cuentas de activo son de naturaleza deudora
                    # -- Deber aumenta su saldo
                    # -- Haber disminuye su saldo
                    accumulate_dict[parent_grouping_code_number] += record.debit
                    accumulate_dict[parent_grouping_code_number] -= record.credit
                elif self.SHORT_TERM_PASSIVE_LOWER <= code <= self.LONG_TERM_PASSIVE_UPPER:
                    # 200.01 - Passive
                    # Las cuentas de pasivo son de naturaleza acreedora
                    # -- Deber disminuye su saldo
                    # -- Haber aumenta su saldo
                    accumulate_dict[parent_grouping_code_number] -= record.debit
                    accumulate_dict[parent_grouping_code_number] += record.credit
                elif self.ACCOUNTING_CAPITAL_LOWER <= code <= self.ACCOUNTING_CAPITAL_UPPER:
                    # 300.00 - Capital
                    # Las cuentas de capital son de naturaleza crédito
                    # -- Deber disminuye su saldo
                    # -- Haber aumenta su saldo
                    accumulate_dict[parent_grouping_code_number] -= record.debit
                    accumulate_dict[parent_grouping_code_number] += record.credit

        print 'Accumulate'
        print accumulate_dict

        # Now we have all the totals. Great.

        debit_accumulate = self.create_accumulative_dict(accumulate_dict)

        report_info = debit_accumulate
        print report_info

        response = self.generate_file(report_info, self.EXCEL)
        return response

    def create_accumulative_dict(self, dict):
        response = {
            100.01: {},
            100.02: {},
            200.01: {},
            200.02: {},
            300.00: {}

        }

        for (code, amount) in dict.iteritems():
            if self.SHORT_TERM_ACTIVE_LOWER <= code <= self.SHORT_TERM_ACTIVE_UPPER:
                # 100.01 - Short Term Active
                response[100.01][code] = dict[code]
            elif self.LONG_TERM_ACTIVE_LOWER <= code <= self.LONG_TERM_ACTIVE_UPPER:
                # 100.02 - Long Term Active
                response[100.02][code] = dict[code]
            elif self.SHORT_TERM_PASSIVE_LOWER <= code <= self.SHORT_TERM_PASSIVE_UPPER:
                # 200.01 - Short Term Passive
                response[200.01][code] = dict[code]
            elif self.LONG_TERM_PASSIVE_LOWER <= code <= self.LONG_TERM_PASSIVE_UPPER:
                # 200.02 - Long Term Active
                response[200.02][code] = dict[code]
            elif self.ACCOUNTING_CAPITAL_LOWER <= code <= self.ACCOUNTING_CAPITAL_UPPER:
                # 300.00 - Accounting Capital
                response[300.00][code] = dict[code]
        return response

    def generate_file(self, info, type):
        if type == self.EXCEL:
            response = self.generate_excel_document(info)
            return response

        if type == self.PDF:
            return self.generate_pdf_document(info)

    def generate_excel_document(self, info):

        # Get variables




        output = StringIO.StringIO()
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Create a format to use in the merged range.
        formats = self.get_formats(workbook)
        # Merge 3 cells.
        worksheet.merge_range('B10:D10', 'Activo', formats['level_0_header'])

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
            'gray-1': '#E7E7E7'
        }
        formats = {}
        formats['level_0_header'] = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': colors['gray-1']})
        return formats


def generate_pdf_document(self, info):
    pass
