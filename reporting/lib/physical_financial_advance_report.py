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
        worksheet_1.write('A1', 'Programa Licitación', bold)

        #PhysicalFinancialAdvanceReport.add_programmed_table(workbook, worksheet_1, information_json)
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
    def add_programmed_table(workbook, worksheet, info):
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:H', 15)

        START_ROW = 3
        DATE_COL = 0
        PROGRAMMED_COL = 1
        PROGRAMMED_COL_ALPHA = "B"
        PROGRAMMED_PERCENTAGE_COL = 2
        PROGRAMMED_PERCENTAGE_COL_ALPHA = "C"
        ESTIMATED_COL = 3
        ESTIMATED_COL_ALPHA = "D"
        ESTIMATED_PERCENTAGE_COL = 4
        ESTIMATED_PERCENTAGE_COL_ALPHA = "E"

        # Add all the headers of the report
        PhysicalFinancialAdvanceReport.add_headers_for_programmed_report(workbook, worksheet)

        formats = PhysicalFinancialAdvanceReport.get_formats(workbook)
        bold_format = formats['bold']
        currency_format = formats['currency']
        percentage_format = formats['percentage']

        yellow_bold_format = formats['yellow_bold']
        yellow_currency_format = formats['yellow_currency']
        yellow_percentage_format = formats['yellow_percentage']
        blue_bold_format = formats['blue_bold']
        blue_currency_format = formats['blue_currency']

        row_count = START_ROW
        for year in info['biddings_programs']:
            for month in year['months']:
                worksheet.write(row_count, DATE_COL, month['month'] + ", " + year['year'],
                                bold_format)
                worksheet.write(row_count, PROGRAMMED_COL, month['accumulated_programmed'],
                                currency_format)
                worksheet.write(row_count, ESTIMATED_COL, month['accumulated_paid_estimate'],
                                currency_format)
                row_count += 1

        # Generating the automatic columns.
                for i in range(START_ROW, row_count):
                    conditional = '=IF(' + PROGRAMMED_COL_ALPHA + str(row_count) + '=0,0,' + PROGRAMMED_COL_ALPHA + ''\
                                  + str(i+1) + '/' + PROGRAMMED_COL_ALPHA + str(row_count) + ')'
                    worksheet.write(i, PROGRAMMED_PERCENTAGE_COL, conditional,percentage_format)

                    conditional = '=IF(' + PROGRAMMED_COL_ALPHA + str(row_count) + '=0,0,' + ESTIMATED_COL_ALPHA + '' \
                                  + str(i + 1) + '/' + PROGRAMMED_COL_ALPHA + str(row_count) + ')'
                    worksheet.write(i, ESTIMATED_PERCENTAGE_COL, conditional, percentage_format)

    #month['percentage_estimated']

    @staticmethod
    def add_progress_table(workbook, worksheet, info):
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:H', 15)

        # Add all the headers of the report
        PhysicalFinancialAdvanceReport.add_headers_for_progress_report(workbook, worksheet)

        start_cell = 3
        count_cell = start_cell

        TOP_LINE_ITEM_COL = 0
        SUB_LINE_ITEM_COL = 1
        IMPORT_COL = 2
        FINANCIAL_ESTIMATED_COL = 3
        FINANCIAL_ADVANCE_COL = 4
        PHYSICAL_ESTIMATED_COL = 5
        PHYSICAL_ADVANCE_COL = 6


        formats = PhysicalFinancialAdvanceReport.get_formats(workbook)
        bold_format = formats['bold']
        currency_format = formats['currency']
        percentage_format = formats['percentage']

        yellow_bold_format = formats['yellow_bold']
        yellow_currency_format = formats['yellow_currency']
        yellow_percentage_format = formats['yellow_percentage']
        blue_bold_format = formats['blue_bold']
        blue_currency_format = formats['blue_currency']

        worksheet.merge_range('A1:G1', 'Avance Físico Financiero', blue_bold_format)

        financial_report = info['physical_financial_advance']

        for top_line_item in financial_report['line_items']:
            pass




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

        worksheet.merge_range('B2:B3', 'Subpartida', header_format)

        worksheet.write('C2', 'Presupuesto Base', header_format)
        worksheet.write('C3', 'Importe', header_format)

        worksheet.merge_range('D2:E2', 'Avance Financiero', header_format)
        worksheet.write('D3', 'Estimado', header_format)
        worksheet.write('E3', 'Avance', header_format)

        worksheet.merge_range('F2:G2', 'Avance Físico', header_format)
        worksheet.write('F3', 'Estimado', header_format)
        worksheet.write('G3', 'Avance', header_format)

    @staticmethod
    def add_headers_for_programmed_report(workbook, worksheet):
        # Create a format to use in the merged range.
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#A9C1F4'}

        header_format = workbook.add_format(header_format_info)

        #header_format_info['fg_color'] = '#F43C37'  # Red

        #header_format_info['fg_color'] = '#6BB067'  # Green

        worksheet.merge_range('A2:A3', 'Mes', header_format)

        worksheet.merge_range('A1:E1', 'Programa General', header_format)

        # Programado
        worksheet.merge_range('B2:C2', 'Programado de Proyecto', header_format)
        worksheet.write('B3', 'Importe S/IVA', header_format)
        worksheet.write('C3', 'Porcentaje', header_format)

        # Estimado
        worksheet.merge_range('D2:E2', 'Estimado', header_format)
        worksheet.write('D3', 'Importe S/IVA', header_format)
        worksheet.write('E3', 'Porcentaje', header_format)
