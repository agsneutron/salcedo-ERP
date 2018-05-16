# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class AccountsListFile(object):


    @staticmethod
    def generate_accounts_list(accounts_array):

        if len(accounts_array) == 0:
            output = StringIO.StringIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Cuentas Contables')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.write('A1', 'No se encontraron registros para la búsqueda de cuentas contables.')
        else:

            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Lista Nominal')


            # Widen the first column to make the text clearer.
            worksheet.set_column('A:J', 15)
            worksheet.set_column('A:K', 25)

            AccountsListFile.add_headers(workbook, worksheet, accounts_array)



        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Cuentas_Contables.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet, accounts_array):

        formats = AccountsListFile.get_formats(workbook)

        worksheet.merge_range('C3:G3', 'SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.', formats['white_border'])


        worksheet.merge_range('D5:F5', 'CUENTAS CONTABLES', formats['white_bg_blue_border'])
        worksheet.merge_range('G5:K5', '', formats['white_bg_blue_border'])

        worksheet.write('A6', 'Número de cuenta', formats['blue_bg_white_font'])
        worksheet.write('B6', 'Nombre ', formats['blue_bg_white_font'])
        worksheet.write('C6', 'Empresa ', formats['blue_bg_white_font'])
        worksheet.write('D6', 'Estatus ', formats['blue_bg_white_font'])
        worksheet.write('E6', 'Naturaleza', formats['blue_bg_white_font'])
        worksheet.write('F6', 'Tipo', formats['blue_bg_white_font'])
        worksheet.write('G6', 'Rubro de la Cuenta', formats['blue_bg_white_font'])
        worksheet.write('H6', 'Código Agrupador', formats['blue_bg_white_font'])
        worksheet.write('I6', 'Es subcuenta de', formats['blue_bg_white_font'])



        row = 7
        NUMBER_COL = 'A'
        NAME_COL = 'B'
        COMPANY_COL = 'C'
        STATUS_COL = 'D'
        NATURE_COL = 'E'
        TYPE_COL = 'F'
        ITEM_COL = 'G'
        GROUPING_COL = 'H'
        SUBSIDIARY_COL = 'I'


        for account in accounts_array:
            worksheet.write(NUMBER_COL+str(row), account['id'], formats['left_bold'])
            worksheet.write(NAME_COL+str(row), account['name'], formats['left_bold'])
            worksheet.write(COMPANY_COL+str(row), account['internal_company'], formats['left_bold'])
            worksheet.write(STATUS_COL+str(row), account['status'], formats['left_bold'])
            worksheet.write(NATURE_COL+str(row), account['nature_account'], formats['left_bold'])
            worksheet.write(TYPE_COL+str(row), account['type_account'], formats['left_bold'])
            worksheet.write(GROUPING_COL+str(row), account['grouping_code'], formats['left_bold'])
            if(account['subsidiary_account_id'] == None):
                account['subsidiary_account'] = "-"
            worksheet.write(SUBSIDIARY_COL+str(row),account['subsidiary_account'], formats['left_bold'])

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
