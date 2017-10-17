# coding=utf-8
from decimal import Decimal

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook


class BudgetReportsByContractor(object):

    @staticmethod
    def generate_report(information_json):
        if len(information_json) == 0:
            output = StringIO.StringIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet('Estimaciones por contratista')

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.write('A1', 'Aún no se ha generado información suficiente para generar el reporte.')
        else:


            output = StringIO.StringIO()

            # Create an new Excel file and add a worksheet.
            workbook = Workbook(output)

            # Iterate through the contractors array.
            for contractor in information_json['data']:
                for estimate in contractor['estimates']:
                    worksheet = workbook.add_worksheet(estimate['contract_key'])
                    BudgetReportsByContractor.add_headers(workbook, worksheet, information_json, contractor, estimate)
                    BudgetReportsByContractor.add_estimates_table(workbook, worksheet, estimate)




        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Estimaciones_por_Contratista.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response

    @staticmethod
    def add_headers(workbook, worksheet, general_info, contractor_info, contract_info):

        # Create a format to use in the merged range.
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#19306D',
            'font_size':14,
            'font_color': '#FFFFFF'
        }

        general_format_info = {
            'bold': 1,
            'border': 0,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': '#F3F2F3',
            'font_size': 12,
            'font_color': '#202020'
        }

        formats = BudgetReportsByContractor.get_formats(workbook)
        light_blue_format = formats['light_blue']
        currency_bold_format = formats['currency_left_bold']

        header_format = workbook.add_format(header_format_info)
        general_format = workbook.add_format(general_format_info)

        header_format_info['fg_color'] = '#F43C37'  # Red

        header_format_info['fg_color'] = '#6BB067'  # Green

        worksheet.merge_range('A1:J1', general_info['project_name'], header_format)

        # Clave del Proyecto.
        worksheet.write('A2', "Código de la Obra: ", general_format)
        worksheet.merge_range('B2:J2',general_info['project_key'],general_format)

        # Fecha del Proyecto.
        worksheet.write('A3', "Fecha: ", general_format)
        worksheet.merge_range('B3:J3', "Del " + general_info['project_start_date'] + " al " +general_info['project_end_date'], general_format)

        # Nombre del Contratista.
        worksheet.write('A4', "Contratista: ", general_format)
        worksheet.merge_range('B4:J4', contractor_info['contractor_name'], general_format)

        # Clave del contrato.
        worksheet.write('A5', "Clave del Contrato: ", general_format)
        worksheet.merge_range('B5:J5', contract_info['contract_key'], general_format)

        # Monto del contrato.
        worksheet.write('A6', "Monto del Contrato: ", general_format)
        worksheet.merge_range('B6:J6', contract_info['contract_amount'], currency_bold_format)

        # Monto pendiente.
        worksheet.write('A7', "Monto Pendiente: ", general_format)
        worksheet.merge_range('B7:J7', contract_info['contract_amount']-contract_info['estimate_financial_advance'], currency_bold_format)

        worksheet.set_row(1, 20)
        worksheet.set_row(2, 20)
        worksheet.set_row(3, 20)
        worksheet.set_row(4, 20)

        worksheet.set_column('A:J', 18)
        worksheet.merge_range('A9:J9', 'Estimaciones', light_blue_format)
        worksheet.write('A10', 'Fecha de Inicio', light_blue_format)
        worksheet.write('B10', 'Fecha de Fin', light_blue_format)
        worksheet.write('C10', 'Periodo', light_blue_format)
        worksheet.write('D10', 'Clave de la Estimación', light_blue_format)
        worksheet.write('E10', 'Cantidad', light_blue_format)
        worksheet.write('F10', 'Estatus', light_blue_format)
        worksheet.write('G10', 'Avance Físico', light_blue_format)
        worksheet.write('H10', '%', light_blue_format)
        worksheet.write('I10', 'Avance Financiero', light_blue_format)
        worksheet.write('J10', '%', light_blue_format)



    @staticmethod
    def add_estimates_table(workbook, worksheet, info):

        START_DATE_COL = 0
        END_DATE_COL = 1
        PERIOD_COL = 2
        KEY_COL = 3
        AMOUNT_COL = 4
        STATUS_COL = 5
        PHYSICAL_COL = 6
        PHYSICAL_PERCENTAGE_COL = 7
        FINANCIAL_COL = 8
        FINANCIAL_PERCENTAGE_COL = 9

        START_ROW = 9


        formats = BudgetReportsByContractor.get_formats(workbook)
        light_border_format = formats['light_border']
        light_border_format.set_text_wrap()
        light_border_grey_format = formats['light_border_grey']
        light_blue_format = formats['light_blue']
        percentage_format = formats['percentage']


        row_counter = START_ROW
        estimate_counter = 0
        estimate = info
        estimate_counter += 1
        estimate_row = row_counter

        if estimate_counter % 2 == 0:
            cell_format = light_border_grey_format
        else:
            cell_format = light_border_format

        for progress_estimate in estimate['progress_estimates']:
            worksheet.write(row_counter, KEY_COL, progress_estimate['key'], cell_format)
            worksheet.write(row_counter, AMOUNT_COL, progress_estimate['amount'], cell_format)
            worksheet.write(row_counter, STATUS_COL, progress_estimate['status'], cell_format)
            row_counter += 1

        worksheet.merge_range('A'+str(estimate_row+1)+':A'+str(row_counter), estimate['estimate_start_date'], cell_format)
        worksheet.merge_range('B'+str(estimate_row+1)+':B'+str(row_counter), estimate['estimate_end_date'], cell_format)
        worksheet.merge_range('C'+str(estimate_row+1)+':C'+str(row_counter), estimate['estimate_period'], cell_format)
        worksheet.merge_range('G'+str(estimate_row+1)+':G'+str(row_counter), estimate['estimate_physical_advance'], cell_format)
        worksheet.merge_range('I'+str(estimate_row+1)+':I'+str(row_counter), estimate['estimate_financial_advance'], cell_format)

        #Percentages.
        # Physical.
        condition = '=IF(B6=0,0,G'+str(START_ROW+1)+'/B6)'
        worksheet.merge_range('H' + str(START_ROW + 1) + ':H' + str(row_counter), condition, percentage_format)

        # Financial.
        condition = '=IF(B6=0,0,I' + str(START_ROW + 1) + '/B6)'
        worksheet.merge_range('J' + str(START_ROW + 1) + ':J' + str(row_counter), condition, percentage_format)

        row_counter += 1

        # Concepts.
        row_counter += 2
        worksheet.merge_range('A'+str(row_counter+1)+':F'+str(row_counter+1), 'Conceptos del Contrato', light_blue_format)
        row_counter += 1
        worksheet.write(row_counter, START_DATE_COL, "Clave", light_blue_format)
        worksheet.merge_range('B' + str(row_counter + 1) + ':C' + str(row_counter + 1), 'Descripción',
                              light_blue_format)
        worksheet.write(row_counter, KEY_COL, "Unidad", light_blue_format)
        worksheet.write(row_counter, AMOUNT_COL, "Precio Unitario", light_blue_format)
        worksheet.write(row_counter, STATUS_COL, "Cantidad", light_blue_format)

        row_counter += 1
        for concept in estimate['concepts']:
            worksheet.set_row(row_counter, 130)
            worksheet.write(row_counter, START_DATE_COL, concept['concept_key'], light_border_format)
            worksheet.merge_range('B' + str(row_counter + 1) + ':C' + str(row_counter + 1), concept['concept_description'], light_border_format)
            worksheet.write(row_counter, KEY_COL, concept['concept_unit'],light_border_format)
            worksheet.write(row_counter, AMOUNT_COL, concept['concept_price'],light_border_format)
            worksheet.write(row_counter, STATUS_COL, str(concept['concept_quantity']),light_border_format)
            row_counter += 1










    @staticmethod
    def get_formats(workbook):
        formats = {}
        # Create a format to use in the merged range.
        format_info = {
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#D5D5D5',
            'num_format': '$#,#00.00'
        }

        formats['light_border'] = workbook.add_format(format_info)

        format_info = {
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'fg_color': '#F3F2F3',
            'border_color': '#D5D5D5',
            'num_format': '$#,#00.00'
        }

        formats['light_border_grey'] = workbook.add_format(format_info)


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
            'align': 'center',
            'valign': 'vcenter',
            'border': 0,
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
        centered_info = {
            'border': 0,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': '#F3F2F3',
            'bold': 1,
            'num_format': '$#,#00.00'}

        formats['currency_left_bold'] = workbook.add_format(centered_info)

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
        header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#139189',
            'border_color': '#139189',
            'font_color': '#FFFFFF'
        }

        formats['light_blue'] = workbook.add_format(header_format_info)

        # Create a format to use in the merged range.
        centered_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,#00.00',
            'fg_color': '#A9C1F4'}

        formats['blue_currency'] = workbook.add_format(centered_info)

        return formats