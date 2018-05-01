# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class PayrollListFile(object):


    @staticmethod
    def generate_payroll_list(payroll_array):

        if len(payroll_array) == 0:
            output = StringIO.StringIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Lista Nominal')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.write('A1', 'No se encontraron registros para el periodo nominal seleccionado.')
        else:

            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Lista Nominal')


            # Widen the first column to make the text clearer.
            worksheet.set_column('A:K', 15)


            PayrollListFile.add_headers(workbook, worksheet, payroll_array)



        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Listado_Nominal.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet, payroll_array):

        formats = PayrollListFile.get_formats(workbook)

        worksheet.merge_range('C3:G3', 'SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.', formats['white_border'])


        worksheet.merge_range('D5:F5', 'LISTADO NOMINAL', formats['white_bg_blue_border'])
        worksheet.merge_range('G5:K5', '', formats['white_bg_blue_border'])

        worksheet.write('A6', 'Clave del empleado ', formats['blue_bg_white_font'])
        worksheet.write('B6', 'Nombre ', formats['blue_bg_white_font'])
        worksheet.write('C6', 'RFC ', formats['blue_bg_white_font'])
        worksheet.write('D6', 'Póliza de Seguro ', formats['blue_bg_white_font'])
        worksheet.write('E6', 'Puesto Asignado ', formats['blue_bg_white_font'])
        worksheet.write('F6', 'Sueldo Base ', formats['blue_bg_white_font'])
        worksheet.write('G6', 'Percepciones ', formats['blue_bg_white_font'])
        worksheet.write('H6', 'Deducciones ', formats['blue_bg_white_font'])
        worksheet.write('I6', 'Sueldo Neto ', formats['blue_bg_white_font'])



        row = 7
        KEY_COL = 'A'
        NAME_COL = 'B'
        RFC_COL = 'C'
        SSN_COL = 'D'
        POSITION_COL = 'E'
        SALARY_COL = 'F'
        EARNINGS_COL = 'G'
        DEDUCTIONS_COL = 'H'
        FINAL_SALARY_COL = 'I'


        for payroll in payroll_array:
            worksheet.write(KEY_COL+str(row), payroll['employee_key'], formats['left_bold'])
            worksheet.write(NAME_COL+str(row), payroll['employee_fullname'], formats['left_bold'])
            worksheet.write(RFC_COL+str(row), payroll['rfc'], formats['left_bold'])
            worksheet.write(SSN_COL+str(row), payroll['ssn'], formats['left_bold'])
            worksheet.write(POSITION_COL+str(row), payroll['position'], formats['left_bold'])
            worksheet.write(SALARY_COL+str(row), payroll['base_salary'], formats['currency_centered_bold'])
            worksheet.write(EARNINGS_COL+str(row), float(payroll['total_earnings']), formats['currency_centered_bold'])
            worksheet.write(DEDUCTIONS_COL+str(row), float(payroll['total_deductions']), formats['currency_centered_bold'])
            worksheet.write(FINAL_SALARY_COL+str(row), (float(payroll['total_earnings']) - float(payroll['total_deductions'])), formats['currency_centered_bold'])

            row += 1



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
        formats['white_border'].set_font_size(20)

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
