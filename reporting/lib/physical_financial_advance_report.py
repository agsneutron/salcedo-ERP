# coding=utf-8
import fractions
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
        PhysicalFinancialAdvanceReport.add_progress_table(workbook, worksheet_2, information_json)

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
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,#00.00'}

        formats['currency'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,#00.00',
            'fg_color': '#FFFF00'}

        formats['yellow_currency'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '0.00%'}

        formats['percentage'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '0.00%',
            'fg_color': '#FFFF00'}

        formats['yellow_percentage'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1,
            'border': 1}

        formats['centered_bold'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'valign': 'vcenter',
            'bold': 1,
            'border': 1}

        formats['bold'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        centered_info = {
            'valign': 'vcenter',
            'bold': 1,
            'border': 1,
            'fg_color': '#FFFF00'}

        formats['yellow_bold'] = workbook.add_format(centered_info)

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

        # Create a format to use in the merged range.
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#A9C1F4'}

        formats['blue_bold'] = workbook.add_format(header_format_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,#00.00',
            'fg_color': '#A9C1F4'}

        formats['blue_currency'] = workbook.add_format(centered_info)

        return formats

    @staticmethod
    def add_programmed_table(workbook, worksheet):
        pass

    @staticmethod
    def add_progress_table(workbook, worksheet, info):
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:H', 15)

        # Add all the headers of the report
        PhysicalFinancialAdvanceReport.add_headers_for_progress_report(workbook, worksheet)

        start_cell = 3
        count_cell = start_cell

        LINE_ITEM_COL = 0
        IMPORT_COL = 1
        FINANCIAL_ESTIMATED_COL = 2
        FINANCIAL_ADVANCE_COL = 3
        PHYSICAL_ESTIMATED_COL = 4
        PHYSICAL_ADVANCE_COL = 5

        formats = PhysicalFinancialAdvanceReport.get_formats(workbook)
        bold_format = formats['bold']
        currency_format = formats['currency']
        percentage_format = formats['percentage']

        yellow_bold_format = formats['yellow_bold']
        yellow_currency_format = formats['yellow_currency']
        yellow_percentage_format = formats['yellow_percentage']
        blue_bold_format = formats['blue_bold']
        blue_currency_format = formats['blue_currency']

        worksheet.merge_range('A1:F1', 'Avance Físico Financiero', blue_bold_format)

        for line_item in info['physical_financial_advance']:
            total_programmed = line_item['total_programmed']

            total_physical_advance = line_item['total_physical_advance']
            # total_physical_advance / total_programmed

            # =IF(B4=0,0,E4/B4)
            total_physical_advance_percentage = '=IF(B' + str(count_cell + 1) + '=0,0, E' + str(
                count_cell + 1) + '/B' + str(count_cell + 1) + ')'
            total_financial_advance = line_item['total_financial_advance']
            # total_financial_advance / total_programmed
            total_financial_advance_percentage = '=IF(B' + str(count_cell + 1) + '=0,0, C' + str(
                count_cell + 1) + '/B' + str(count_cell + 1) + ')'

            worksheet.write(count_cell, LINE_ITEM_COL, line_item['line_item_name'], bold_format)
            worksheet.write(count_cell, IMPORT_COL, total_programmed, currency_format)
            worksheet.write(count_cell, FINANCIAL_ESTIMATED_COL, total_financial_advance, currency_format)
            worksheet.write(count_cell, FINANCIAL_ADVANCE_COL, total_financial_advance_percentage, percentage_format)
            worksheet.write(count_cell, PHYSICAL_ESTIMATED_COL, total_physical_advance, currency_format)
            worksheet.write(count_cell, PHYSICAL_ADVANCE_COL, total_physical_advance_percentage, percentage_format)

            count_cell += 1

        # Importe general
        worksheet.write(count_cell, LINE_ITEM_COL, 'Importe', yellow_bold_format)

        worksheet.write(count_cell, IMPORT_COL, '=SUM(B' + str(start_cell + 1) + ':B' + str(count_cell) + ')',
                        yellow_currency_format)

        worksheet.write(count_cell, FINANCIAL_ESTIMATED_COL,
                        '=SUM(C' + str(start_cell + 1) + ':C' + str(count_cell) + ')', yellow_currency_format)
        worksheet.write(count_cell, FINANCIAL_ADVANCE_COL,
                        '=SUM(D' + str(start_cell + 1) + ':D' + str(count_cell) + ')', yellow_percentage_format)
        worksheet.write(count_cell, PHYSICAL_ESTIMATED_COL,
                        '=SUM(E' + str(start_cell + 1) + ':E' + str(count_cell) + ')', yellow_currency_format)
        worksheet.write(count_cell, PHYSICAL_ADVANCE_COL, '=SUM(F' + str(start_cell + 1) + ':F' + str(count_cell) + ')',
                        yellow_percentage_format)

        count_cell += 1
        # IVA

        worksheet.write(count_cell, LINE_ITEM_COL, 'IVA', bold_format)

        worksheet.write(count_cell, IMPORT_COL, '=B' + str(count_cell) + '*0.16',
                        currency_format)

        worksheet.write(count_cell, FINANCIAL_ESTIMATED_COL,
                        '=C' + str(count_cell) + '*0.16', currency_format)
        worksheet.write(count_cell, FINANCIAL_ADVANCE_COL,
                        '-', bold_format)
        worksheet.write(count_cell, PHYSICAL_ESTIMATED_COL,
                        '=E' + str(count_cell) + '*0.16', currency_format)
        worksheet.write(count_cell, PHYSICAL_ADVANCE_COL, '-',
                        bold_format)

        count_cell += 1
        # Total

        worksheet.write(count_cell, LINE_ITEM_COL, 'Total', yellow_bold_format)

        worksheet.write(count_cell, IMPORT_COL, '=B' + str(count_cell - 1) + '*1.16',
                        yellow_currency_format)

        worksheet.write(count_cell, FINANCIAL_ESTIMATED_COL,
                        '=C' + str(count_cell - 1) + '*1.16', yellow_currency_format)
        worksheet.write(count_cell, FINANCIAL_ADVANCE_COL,
                        '=D' + str(count_cell - 1), yellow_percentage_format)
        worksheet.write(count_cell, PHYSICAL_ESTIMATED_COL,
                        '=E' + str(count_cell - 1) + '*1.16', yellow_currency_format)
        worksheet.write(count_cell, PHYSICAL_ADVANCE_COL, '=F' + str(count_cell - 1), yellow_percentage_format)

        count_cell += 1

        # Importe líquido

        worksheet.write(count_cell, LINE_ITEM_COL, 'Importe Líquido', blue_bold_format)

        worksheet.write(count_cell, IMPORT_COL, '=B' + str(count_cell),
                        blue_currency_format)

        worksheet.write(count_cell, FINANCIAL_ESTIMATED_COL,
                        '=C' + str(count_cell), blue_currency_format)

    @staticmethod
    def add_headers_for_progress_report(workbook, worksheet):
        # Create a format to use in the merged range.
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#A9C1F4'}

        header_format = workbook.add_format(header_format_info)

        header_format_info['fg_color'] = '#F43C37'  # Red

        header_format_info['fg_color'] = '#6BB067'  # Green

        worksheet.merge_range('A2:A3', 'Partida', header_format)

        worksheet.write('B2', 'Presupuesto Base', header_format)
        worksheet.write('B3', 'Importe', header_format)

        worksheet.merge_range('C2:D2', 'Avance Financiero', header_format)
        worksheet.write('C3', 'Estimado', header_format)
        worksheet.write('D3', 'Avance', header_format)

        worksheet.merge_range('E2:F2', 'Avance Físico', header_format)
        worksheet.write('E3', 'Estimado', header_format)
        worksheet.write('F3', 'Avance', header_format)
