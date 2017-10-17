# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class EstimateReports(object):
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

            EstimateReports.show_concepts = show_concepts

            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            workbook = Workbook(output)
            numberSheet=1
            for info in information_json:
                worksheet = workbook.add_worksheet('Hoja de Estimación ' + str(numberSheet))
                numberSheet+=1

                # Widen the first column to make the text clearer.
                worksheet.set_column('A:J', 20)

                EstimateReports.add_headers(workbook, worksheet, info)

            #EstimateReports.add_concepts(workbook, worksheet, information_json)

            # Insert an image.
            # worksheet.insert_image('B5', 'logo.png')

        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=hoja de estimación.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet,info):

        borde_negro = workbook.add_format({
            'border': 1})
        borde_negro.set_border_color('black')
        borde_negro.set_border(1)

        merge_format_blanco = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        merge_format_blanco_CENTER = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        merge_format_blanco.set_font_color('black')

        worksheet.merge_range('C3:H3', 'SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.', merge_format_blanco_CENTER)

        worksheet.merge_range('A5:E5', '', borde_negro)
        worksheet.merge_range('F5:J5', '', borde_negro)
        worksheet.merge_range('A5:E5', 'HOJA ESTIMACIÓN', merge_format_blanco_CENTER)
        worksheet.merge_range('F5:J5', '', merge_format_blanco)

        worksheet.write('A6', 'CONTRATISTA: ', merge_format_blanco)
        worksheet.write('A7', 'OBRA: ', merge_format_blanco)
        worksheet.write('A8', 'CONCEPTO: ', merge_format_blanco)

        worksheet.write('F6', 'PERIODO: ', merge_format_blanco)
        worksheet.write('F7', 'DEL: ', merge_format_blanco)
        worksheet.write('F8', 'AL: ', merge_format_blanco)

        worksheet.merge_range('B6:E6', info['contractor_name'], merge_format_blanco)
        worksheet.merge_range('B7:E7', info['project'], merge_format_blanco)
        worksheet.merge_range('B8:E8', info['line_item'], merge_format_blanco)

        worksheet.merge_range('G6:J6', info['period'], merge_format_blanco)
        worksheet.merge_range('G7:J7', info['start_date'], merge_format_blanco)
        worksheet.merge_range('G8:J8', info['end_date'], merge_format_blanco)

        worksheet.merge_range('A10:E10', 'AVANCE FINANCIERO', merge_format_blanco_CENTER)
        worksheet.merge_range('F10:J10', 'AVANCE FÍSICO', merge_format_blanco)



    @staticmethod
    def add_concepts(workbook, worksheet, info):
        # The first cell is A7
        formats = EstimateReports.get_formats(workbook)

        if EstimateReports.show_concepts:
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

            if EstimateReports.show_concepts:
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

            if EstimateReports.show_concepts:
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

            if EstimateReports.show_concepts:
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
