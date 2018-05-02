# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class EarningsDeductionsTotalEarnings(object):


    @staticmethod
    def generate_report(data_set):

        if len(data_set) == 0:
            output = StringIO.StringIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Totales por Percepciones y Deducciones')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.write('A1', 'No se encontraron registros.')
        else:

            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Totales')


            # Widen the first column to make the text clearer.
            worksheet.set_column('A:D', 20)


            EarningsDeductionsTotalEarnings.add_headers(workbook, worksheet, data_set)



        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Totales_por_percepciones_y_deducciones.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet, data_set):

        formats = EarningsDeductionsTotalEarnings.get_formats(workbook)

        # Title and subtitle.
        worksheet.merge_range('A3:D3', 'SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.', formats['white_border'])
        worksheet.merge_range('A5:D5', 'PERCEPCIONES Y DEDUCCIONES', formats['white_bg_blue_border'])

        # General Data.
        worksheet.write('A7', 'Grupo de Nómina', formats['blue_bg_white_font'])
        worksheet.write('A8', data_set['payroll_group_name'], formats['centered_bold'])

        worksheet.write('B7', 'Periodo de Nómina', formats['blue_bg_white_font'])
        worksheet.write('B8', data_set['payroll_period_name'], formats['centered_bold'])

        headers_init_row = 12
        worksheet.merge_range('A' + str(headers_init_row) + ":D" + str(headers_init_row), 'PERCEPCIONES',
                              formats['white_bg_blue_border'])

        headers_init_row += 1
        worksheet.write('A'+str(headers_init_row), 'Nombre de la deducción', formats['blue_bg_white_font'])
        worksheet.write('B'+str(headers_init_row), 'Clave del SAT', formats['blue_bg_white_font'])
        worksheet.write('C'+str(headers_init_row), 'Fijo', formats['blue_bg_white_font'])
        worksheet.write('D'+str(headers_init_row), 'Variable', formats['blue_bg_white_font'])

        row_counter = headers_init_row + 1
        init_perceptions_row_counter = row_counter
        NAME_COL = 'A'
        KEY_COL = 'B'
        FIXED_COL = 'C'
        VARIABLE_COL = 'D'

        # Perceptions.
        for record in data_set["perceptions"]:
            worksheet.write(NAME_COL + str(row_counter), record['name'], formats['left_bold'])
            worksheet.write(KEY_COL + str(row_counter), record['sat_key'], formats['left_bold'])
            worksheet.write(FIXED_COL + str(row_counter), float(record['total_fixed']), formats['currency_centered_bold'])
            worksheet.write(VARIABLE_COL + str(row_counter), float(record['total_variable']), formats['currency_centered_bold'])
            row_counter += 1

        # Perceptions Totals
        row_counter += 1
        worksheet.write('A' + str(row_counter), 'Totales', formats['blue_bg_white_font'])

        fixed_summatory_string = "=SUM("+FIXED_COL+str(init_perceptions_row_counter)+\
                           ":"+FIXED_COL+str(init_perceptions_row_counter + len(data_set["perceptions"]) - 1)+")"

        variable_summatory_string = "=SUM(" + VARIABLE_COL + str(init_perceptions_row_counter) + \
                                 ":" + VARIABLE_COL + str(
            init_perceptions_row_counter + len(data_set["perceptions"]) - 1) + ")"

        worksheet.write(FIXED_COL + str(row_counter), fixed_summatory_string, formats['currency_centered_bold'])
        worksheet.write(VARIABLE_COL + str(row_counter), variable_summatory_string, formats['currency_centered_bold'])



        #------------
        # Deductions.
        #------------
        row_counter += 4
        #worksheet.write('A' + str(row_counter), 'DEDUCCIONES', formats['left_bold'])
        worksheet.merge_range('A' + str(row_counter)+":D"+str(row_counter), 'DEDUCCIONES', formats['white_bg_blue_border'])

        row_counter += 1
        worksheet.write('A' + str(row_counter), 'Nombre de la deducción', formats['blue_bg_white_font'])
        worksheet.write('B' + str(row_counter), 'Clave del SAT', formats['blue_bg_white_font'])
        worksheet.write('C' + str(row_counter), 'Fijo', formats['blue_bg_white_font'])
        worksheet.write('D' + str(row_counter), 'Variable', formats['blue_bg_white_font'])

        row_counter += 1
        init_perceptions_row_counter = row_counter

        for record in data_set["deductions"]:
            worksheet.write(NAME_COL + str(row_counter), record['name'], formats['left_bold'])
            worksheet.write(KEY_COL + str(row_counter), record['sat_key'], formats['left_bold'])
            worksheet.write(FIXED_COL + str(row_counter), float(record['total_fixed']), formats['currency_centered_bold'])
            worksheet.write(VARIABLE_COL + str(row_counter), float(record['total_variable']), formats['currency_centered_bold'])
            row_counter += 1

        # Deductions Totals
        row_counter += 1
        worksheet.write('A' + str(row_counter), 'Totales', formats['blue_bg_white_font'])

        fixed_summatory_string = "=SUM(" + FIXED_COL + str(init_perceptions_row_counter) + \
                                 ":" + FIXED_COL + str(
            init_perceptions_row_counter + len(data_set["deductions"]) - 1) + ")"

        variable_summatory_string = "=SUM(" + VARIABLE_COL + str(init_perceptions_row_counter) + \
                                    ":" + VARIABLE_COL + str(
            init_perceptions_row_counter + len(data_set["deductions"]) - 1) + ")"

        worksheet.write(FIXED_COL + str(row_counter), fixed_summatory_string, formats['currency_centered_bold'])
        worksheet.write(VARIABLE_COL + str(row_counter), variable_summatory_string,
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
            'bold': 1
            }

        formats['centered_bold'] = workbook.add_format(centered_info)

        # Create a format to use in the merged range.
        left_bold_info = {
            'align': 'left',
            'valign': 'vcenter',
            'bold': 1,
        }

        formats['left_bold'] = workbook.add_format(left_bold_info)


        # Create a format to use in the merged range.
        centered_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1,
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

        formats['white_border'] = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        formats['white_border'].set_border_color('white')
        formats['white_border'].set_border(1)
        formats['white_border'].set_bold(True)
        formats['white_border'].set_font_size(18)

        formats['blue_bg_white_font'] = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': '6f8eb4'})
        formats['blue_bg_white_font'].set_border_color('9FB0BC')
        formats['blue_bg_white_font'].set_font_color('white')
        formats['blue_bg_white_font'].set_align('center')

        formats['white_bg_blue_border'] = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'bottom': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})
        formats['white_bg_blue_border'].set_border_color('9FB0BC')
        formats['white_bg_blue_border'].set_font_color('black')

        return formats
