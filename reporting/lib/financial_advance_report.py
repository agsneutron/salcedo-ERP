# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class FinancialAdvanceReport(object):
    show_concepts = False

    @staticmethod
    def generate_report(information_json, show_concepts=True):

        if len(information_json) == 0:
            output = StringIO.StringIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Avance Financiero Interno')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.write('A1', 'Aún no se ha agregado el catálogo de conceptos.')
        else:

            FinancialAdvanceReport.show_concepts = show_concepts

            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            # workbook = Workbook('report.xlsx')
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Avance Financiero Interno')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:H', 20)

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})

            # Write some simple text.
            worksheet.write('A1', 'Avance Financiero Interno', bold)

            FinancialAdvanceReport.add_headers(workbook, worksheet)

            FinancialAdvanceReport.add_concepts(workbook, worksheet, information_json['line_items'])

            # Insert an image.
            # worksheet.insert_image('B5', 'logo.png')

        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Reporte_Avance_Financiero.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet):

        # Create a format to use in the merged range.
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#A9C1F4'}

        header_format = workbook.add_format(header_format_info)

        header_format_info['fg_color'] = '#F43C37'  # Red

        red_header_format = workbook.add_format(header_format_info)

        header_format_info['fg_color'] = '#6BB067'  # Green

        green_header_format = workbook.add_format(header_format_info)

        worksheet.merge_range('A5:A6', 'Partida', header_format)

        if FinancialAdvanceReport.show_concepts:

            worksheet.merge_range('B5:B6', 'Concepto', header_format)

            worksheet.write('C5', 'Programado', header_format)
            worksheet.write('C6', 'Importe C/IVA', header_format)

            worksheet.write('D5', 'Estimado', green_header_format)
            worksheet.write('D6', 'Importe C/IVA', green_header_format)

            worksheet.write('E5', 'Pendiente', red_header_format)
            worksheet.write('E6', 'Importe C/IVA', red_header_format)

            worksheet.write('F5', 'Programa General', header_format)
            worksheet.write('F6', 'Importe C/IVA', header_format)

            worksheet.write('G5', 'Estimado General', green_header_format)
            worksheet.write('G6', 'Importe C/IVA', green_header_format)

            worksheet.write('H5', 'Pendiente General', red_header_format)
            worksheet.write('H6', 'Importe C/IVA', red_header_format)
        else:

            worksheet.write('B5', 'Programa General', header_format)
            worksheet.write('B6', 'Importe C/IVA', header_format)

            worksheet.write('C5', 'Estimado General', green_header_format)
            worksheet.write('C6', 'Importe C/IVA', green_header_format)

            worksheet.write('D5', 'Pendiente General', red_header_format)
            worksheet.write('D6', 'Importe C/IVA', red_header_format)

    @staticmethod
    def add_concepts(workbook, worksheet, info):
        # The first cell is A7
        formats = FinancialAdvanceReport.get_formats(workbook)

        if FinancialAdvanceReport.show_concepts:
            LINE_ITEM_COL = 0
            CONCEPT_COL = 1
            PROGRAMMED_COL = 2
            ESTIMATED_COL = 3
            PENDING_COL = 4
            GENERAL_PROGRAMMED_COL = 5
            GENERAL_ESTIMATED_COL = 6
            GENERAL_PENDING_COL = 7
        else:
            LINE_ITEM_COL = 0
            GENERAL_PROGRAMMED_COL = 1
            GENERAL_ESTIMATED_COL = 2
            GENERAL_PENDING_COL = 3

        START_ROW = 6
        row_count = START_ROW

        for line_item in info:

            number_of_concepts = len(line_item['sub_line_items'])

            if FinancialAdvanceReport.show_concepts:
                worksheet.merge_range(row_count, LINE_ITEM_COL, row_count + number_of_concepts - 1, LINE_ITEM_COL,
                                      line_item['name'], formats['centered_bold'])
                worksheet.merge_range(row_count, GENERAL_PROGRAMMED_COL, row_count + number_of_concepts - 1,
                                      GENERAL_PROGRAMMED_COL,
                                      Decimal(line_item['total_programmed']), formats['currency_centered_bold'])
                worksheet.merge_range(row_count, GENERAL_ESTIMATED_COL, row_count + number_of_concepts - 1,
                                      GENERAL_ESTIMATED_COL,
                                      Decimal(line_item['total_estimated']), formats['light_green_currency'])
                worksheet.merge_range(row_count, GENERAL_PENDING_COL, row_count + number_of_concepts - 1,
                                      GENERAL_PENDING_COL,
                                      Decimal(line_item['total_pending']), formats['light_red_currency'])
            else:
                worksheet.write(row_count, LINE_ITEM_COL,
                                line_item['name'], formats['centered_bold'])
                worksheet.write(row_count, GENERAL_PROGRAMMED_COL,
                                Decimal(line_item['total_programmed']), formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_ESTIMATED_COL,
                                Decimal(line_item['total_estimated']), formats['light_green_currency'])
                worksheet.write(row_count, GENERAL_PENDING_COL,
                                Decimal(line_item['total_pending']), formats['light_red_currency'])

            if FinancialAdvanceReport.show_concepts:
                i = row_count
                for sub_line_item in line_item['sub_line_items']:
                    worksheet.write(i, CONCEPT_COL, sub_line_item['name'], formats['centered'])
                    worksheet.write(i, PROGRAMMED_COL, Decimal(sub_line_item['total_programmed']),
                                    formats['currency_centered'])
                    worksheet.write(i, ESTIMATED_COL, Decimal(sub_line_item['total_estimated']),
                                    formats['light_green_currency'])
                    worksheet.write(i, PENDING_COL, Decimal(sub_line_item['total_pending']), formats['light_red_currency'])

                    i = i + 1

                row_count = row_count + number_of_concepts
            else:
                row_count += 1

            if FinancialAdvanceReport.show_concepts:
                worksheet.write(row_count, PROGRAMMED_COL, '=SUM(C' + str(START_ROW + 1) + ':C' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, ESTIMATED_COL, '=SUM(D' + str(START_ROW + 1) + ':D' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, PENDING_COL, '=SUM(E' + str(START_ROW + 1) + ':E' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_PROGRAMMED_COL,
                                '=SUM(F' + str(START_ROW + 1) + ':F' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_ESTIMATED_COL,
                                '=SUM(G' + str(START_ROW + 1) + ':G' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_PENDING_COL,
                                '=SUM(H' + str(START_ROW + 1) + ':H' + str(row_count) + ')',
                                formats['currency_centered_bold'])
            else:

                worksheet.write(row_count, GENERAL_PROGRAMMED_COL,
                                '=SUM(B' + str(START_ROW + 1) + ':B' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_ESTIMATED_COL,
                                '=SUM(C' + str(START_ROW + 1) + ':C' + str(row_count) + ')',
                                formats['currency_centered_bold'])
                worksheet.write(row_count, GENERAL_PENDING_COL,
                                '=SUM(D' + str(START_ROW + 1) + ':D' + str(row_count) + ')',
                                formats['currency_centered_bold'])

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
