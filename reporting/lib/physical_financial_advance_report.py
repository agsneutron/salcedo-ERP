# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class PhysicalFinancialAdvanceReport(object):
    show_concepts = False

    @staticmethod
    def generate_report(information_json, show_concepts=True):
        print 'json'
        print information_json

        PhysicalFinancialAdvanceReport.show_concepts = show_concepts

        output = StringIO.StringIO()

        # Create an new Excel file and add a worksheet.
        # workbook = Workbook('report.xlsx')
        workbook = Workbook(output)
        worksheet_1 = workbook.add_worksheet('Programado')
        worksheet_2 = workbook.add_worksheet('Avance Físico Financiero')

        # Widen the first column to make the text clearer.
        worksheet_1.set_column('A:H', 20)

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some simple text.
        worksheet_1.write('A1', 'Avance Físico Financiero', bold)

        PhysicalFinancialAdvanceReport.add_programmed_table(workbook, worksheet_1)
        PhysicalFinancialAdvanceReport.add_progress_table(workbook, worksheet_2)

        workbook.close()

        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Avance_Fisico_Financiero.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def get_formats(workbook):
        formats = {}
        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'border': 1}

        formats['centered'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,#00.00'}

        formats['currency_centered'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1,
            'border': 1}

        formats['centered_bold'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1,
            'border': 1,
            'num_format': '$#,#00.00'}

        formats['currency_centered_bold'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'fg_color': '#D0F1B8',
            'num_format': '$#,#00.00'}

        formats['light_green_currency'] = workbook.add_format(info)
        formats['light_green_currency'].set_num_format('$#,#00.00')

        # Create a format to use in the merged range.
        info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'fg_color': '#F1B6C0',
            'num_format': '$#,#00.00'}

        formats['light_red_currency'] = workbook.add_format(info)

        return formats

    @staticmethod
    def add_programmed_table(workbook, worksheet):
        pass

    @staticmethod
    def add_progress_table(workbook, worksheet):
        pass
