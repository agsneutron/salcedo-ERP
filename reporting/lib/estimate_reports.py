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
                worksheet.set_column('A:E', 20)
                worksheet.set_column('F:F', 2)
                worksheet.set_column('G:K', 20)

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

        suma_monto=0
        suma_porcentaje=0

        borde_blanco = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        borde_blanco.set_border_color('white')
        borde_blanco.set_border(1)
        borde_blanco.set_bold(True)
        borde_blanco.set_font_size(20)

        fondo_verde = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': '6f8eb4'})
        fondo_verde.set_border_color('9FB0BC')
        fondo_verde_center=fondo_verde
        fondo_verde_center.set_align('center')

        fondo_blanco_border_gray = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'bottom': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})
        fondo_blanco_border_gray.set_border_color('9FB0BC')

        fondo_blanco_border_gray_center = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'bottom': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})
        fondo_blanco_border_gray_center.set_border_color('9FB0BC')

        fondo_blanco_border_blue = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'bottom': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})
        fondo_blanco_border_blue.set_border_color('9FB0BC')
        fondo_blanco_border_blue.set_font_color('black')

        fondo_blanco_border_blue_rigth = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'bottom': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})
        fondo_blanco_border_blue_rigth.set_border_color('9FB0BC')
        fondo_blanco_border_blue_rigth.set_font_color('black')
        fondo_blanco_border_blue_rigth.set_right(1)
        fondo_blanco_border_blue_rigth.set_right_color('9FB0BC')



        merge_format_blanco = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        merge_format_blanco_CENTER = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'FFFFFF'})

        merge_format_blanco.set_font_color('black')

        worksheet.insert_image('A1', 'static/ERP/admin/img/logo_2_salcedo.png', {'x_scale': 0.5, 'y_scale': 0.4})

        worksheet.merge_range('C3:I3', 'SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.', borde_blanco)


        worksheet.merge_range('A5:E5', 'HOJA ESTIMACIÓN', fondo_blanco_border_blue)
        worksheet.merge_range('G5:K5', '', fondo_blanco_border_blue)

        worksheet.write('A6', 'CONTRATISTA: ', fondo_verde)
        worksheet.write('A7', 'OBRA: ', fondo_verde)
        worksheet.write('A8', 'PARTIDA: ', fondo_verde)

        worksheet.write('G6', 'PERIODO: ', fondo_verde)
        worksheet.write('G7', 'DEL: ', fondo_verde)
        worksheet.write('G8', 'AL: ', fondo_verde)

        worksheet.merge_range('B6:E6', info['contractor_name'], fondo_blanco_border_gray)
        worksheet.merge_range('B7:E7', info['project'], fondo_blanco_border_gray)
        worksheet.merge_range('B8:E8', info['line_item'], fondo_blanco_border_gray)

        worksheet.merge_range('H6:K6', info['period'], fondo_blanco_border_gray)
        worksheet.merge_range('H7:K7', info['start_date'], fondo_blanco_border_gray)
        worksheet.merge_range('H8:K8', info['end_date'], fondo_blanco_border_gray)

        worksheet.merge_range('A10:E10', 'AVANCE FINANCIERO', fondo_blanco_border_blue)
        worksheet.merge_range('G10:K10', 'AVANCE FÍSICO', fondo_blanco_border_blue)

        worksheet.merge_range('A12:C12', 'IMPORTE DEL CONTRATO (C/IVA)', fondo_blanco_border_blue)
        worksheet.merge_range('D12:E12', '${0:,.2f}'.format(info['contract_amount_with_tax']), fondo_blanco_border_blue)

        worksheet.merge_range('G11:H11', 'CANTIDAD', fondo_blanco_border_blue)
        worksheet.write('I11', 'UNIDAD', fondo_blanco_border_blue)
        worksheet.merge_range('J11:K11', 'P.U.', fondo_blanco_border_blue)

        worksheet.merge_range('G12:H12', 'falta', fondo_blanco_border_blue)
        worksheet.write('I12', 'falta', fondo_blanco_border_blue)
        worksheet.merge_range('J12:K12', 'falta', fondo_blanco_border_blue)

        worksheet.merge_range('A14:E14', 'ANTICIPO / AVANCE', fondo_blanco_border_blue)
        worksheet.merge_range('G14:K14', 'ESTIMACIONES', fondo_blanco_border_blue)

        suma_monto = info['financial_advance']['advance_payment']
        suma_porcentaje = (info['financial_advance']['advance_payment']/info['contract_amount_with_tax'])*100

        #avance financiero
        sEstimate=""
        amount=suma_monto
        percent=suma_porcentaje


        worksheet.write('A15', 'ANTICIPO', fondo_verde_center)
        worksheet.write('A16', str('${0:,.2f}'.format(suma_monto)), fondo_blanco_border_blue_rigth)
        worksheet.write('A17', str('{0:,.2f}%'.format(suma_porcentaje)), fondo_blanco_border_blue_rigth)

        indice=1
        renglon =15
        for avance in info['financial_advance']['progress_estimate']:
            sCell = EstimateReports.get_char(indice,1)
            sEstimate = avance['progress_estimate_key']
            amount=avance['progress_estimate_amount']
            percent=(avance['progress_estimate_amount']/info['contract_amount_with_tax'])*100

            worksheet.write(sCell+ str(renglon), sEstimate, fondo_verde_center)
            worksheet.write(sCell+ str(renglon+1), str('${0:,.2f}'.format(amount)), fondo_blanco_border_blue_rigth)
            worksheet.write(sCell+ str(renglon+2), str('{0:,.2f}%'.format(percent)), fondo_blanco_border_blue_rigth)
            suma_monto = suma_monto + amount
            suma_porcentaje = suma_porcentaje + percent
            indice+=1
            if indice ==5:
                indice =0
                renglon += 3

        #rellenar espacios vacios
        if indice<4:
            for i in range(indice, 4):
                sCell = EstimateReports.get_char(i, 1)
                worksheet.write(sCell + str(renglon), '', fondo_verde_center)
                worksheet.write(sCell + str(renglon + 1), '', fondo_blanco_border_blue_rigth)
                worksheet.write(sCell + str(renglon + 2), '', fondo_blanco_border_blue_rigth)

        worksheet.write('E'+ str(renglon), 'TOTAL', fondo_verde_center)
        worksheet.write('E'+ str(renglon+1), str('${0:,.2f}'.format(suma_monto)), fondo_blanco_border_blue_rigth)
        worksheet.write('E'+ str(renglon+2), str('{0:,.2f}%'.format(suma_porcentaje)), fondo_blanco_border_blue_rigth)

        range1 = 'A' + str(renglon + 4) + ':C' + str(renglon + 4)
        range2 = 'D' + str(renglon + 4) + ':E' + str(renglon + 4)
        worksheet.merge_range(range1, 'IMPORTE POR ESTIMAR', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '${0:,.2f}'.format(amount),fondo_blanco_border_gray_center)

        range1 = 'A' + str(renglon + 6) + ':C' + str(renglon + 6)
        range2 = 'D' + str(renglon + 6) + ':E' + str(renglon + 6)
        worksheet.merge_range(range1, 'SUBTOTAL ESTIMACIÓN', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '${0:,.2f}'.format(amount), fondo_blanco_border_gray_center)

        range1 = 'A' + str(renglon + 8) + ':C' + str(renglon + 8)
        range2 = 'D' + str(renglon + 8) + ':E' + str(renglon + 8)
        worksheet.merge_range(range1, 'RETENCIÓN DEL 5% POR VICIOS OCULTOS', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '${0:,.2f}'.format(0), fondo_blanco_border_gray_center)

        range1 = 'A' + str(renglon + 10) + ':C' + str(renglon + 10)
        range2 = 'D' + str(renglon + 10) + ':E' + str(renglon + 10)
        worksheet.merge_range(range1, 'IMPORTE TOTAL DE ESTIMACIÓN', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '${0:,.2f}'.format(amount), fondo_blanco_border_gray_center)

        range1 = 'A' + str(renglon + 11) + ':E' + str(renglon + 11)
        #worksheet.set_column(range1, 10)
        worksheet.set_row('A11', 50)
        worksheet.merge_range(range1, 'OBSERVACIONES: ', merge_format_blanco)

        # SECCIÓN DE FIRMAS ******************************************************************************
        range1 = 'A' + str(renglon + 13) + ':B' + str(renglon + 13)
        range2 = 'A' + str(renglon + 16) + ':B' + str(renglon + 16)
        range3 = 'A' + str(renglon + 17) + ':B' + str(renglon + 17)
        range4 = 'A' + str(renglon + 18) + ':B' + str(renglon + 18)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, info['contractor_name'], merge_format_blanco_CENTER)
        worksheet.merge_range(range3, info['contract_name'], merge_format_blanco_CENTER)
        worksheet.merge_range(range4, 'CONTRATISTA', merge_format_blanco_CENTER)

        range1 = 'C' + str(renglon + 13) + ':D' + str(renglon + 13)
        range2 = 'C' + str(renglon + 16) + ':D' + str(renglon + 16)
        range3 = 'C' + str(renglon + 17) + ':D' + str(renglon + 17)
        range4 = 'C' + str(renglon + 18) + ':D' + str(renglon + 18)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, 'ARQ. EDGARDO SÁNCHEZ JUÁREZ', merge_format_blanco_CENTER)
        worksheet.merge_range(range3, 'DIRECTOR GENERAL', merge_format_blanco_CENTER)
        worksheet.merge_range(range4, '', merge_format_blanco_CENTER)

        range1 = 'E' + str(renglon + 13) + ':G' + str(renglon + 13)
        range2 = 'E' + str(renglon + 16) + ':G' + str(renglon + 16)
        range3 = 'E' + str(renglon + 17) + ':G' + str(renglon + 17)
        range4 = 'E' + str(renglon + 18) + ':G' + str(renglon + 18)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '', merge_format_blanco_CENTER)
        worksheet.merge_range(range3, 'DIRECTOR DE OBRAS', merge_format_blanco_CENTER)
        worksheet.merge_range(range4, '', merge_format_blanco_CENTER)

        range1 = 'H' + str(renglon + 13) + ':I' + str(renglon + 13)
        range2 = 'H' + str(renglon + 16) + ':I' + str(renglon + 16)
        range3 = 'H' + str(renglon + 17) + ':I' + str(renglon + 17)
        range4 = 'H' + str(renglon + 18) + ':I' + str(renglon + 18)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '', merge_format_blanco_CENTER)
        worksheet.merge_range(range3, 'VICEPRESIDENTE EMPRESARIAL', merge_format_blanco_CENTER)
        worksheet.merge_range(range4, '', merge_format_blanco_CENTER)

        range1 = 'J' + str(renglon + 13) + ':K' + str(renglon + 13)
        range2 = 'J' + str(renglon + 16) + ':K' + str(renglon + 16)
        range3 = 'J' + str(renglon + 17) + ':K' + str(renglon + 17)
        range4 = 'J' + str(renglon + 18) + ':K' + str(renglon + 18)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, '', merge_format_blanco_CENTER)
        worksheet.merge_range(range3, 'JEFE DE ADMON.', merge_format_blanco_CENTER)
        worksheet.merge_range(range4, '', merge_format_blanco_CENTER)


        #avance físico
        suma_monto = 0
        suma_porcentaje = 0
        indice=0
        renglon =15
        for avance in info['physical_advance']['progress_estimate']:
            sCell = EstimateReports.get_char(indice,2)
            amount=avance['progress_estimate_amount']
            percent=(avance['percentage'])*100
            worksheet.write(sCell+ str(renglon), avance['progress_estimate_key'], fondo_verde_center)
            worksheet.write(sCell+ str(renglon+1), str('${0:,.2f}'.format(amount)), fondo_blanco_border_blue_rigth)
            worksheet.write(sCell+ str(renglon+2), str('{0:,.2f}%'.format(percent)), fondo_blanco_border_blue_rigth)
            suma_monto = suma_monto + amount
            suma_porcentaje = suma_porcentaje + percent
            indice+=1
            if indice ==5:
                indice =0
                renglon += 3

        # rellenar espacios vacios
        if indice < 4:
            for i in range(indice, 4):
                sCell = EstimateReports.get_char(i, 2)
                worksheet.write(sCell + str(renglon), '', fondo_verde_center)
                worksheet.write(sCell + str(renglon + 1), '', fondo_blanco_border_blue_rigth)
                worksheet.write(sCell + str(renglon + 2), '', fondo_blanco_border_blue_rigth)

        worksheet.write('K'+ str(renglon), 'TOTAL', fondo_verde_center)
        worksheet.write('K'+ str(renglon+1), str('${0:,.2f}'.format(suma_monto)), fondo_blanco_border_blue_rigth)
        worksheet.write('K'+ str(renglon+2), str('{0:,.2f}%'.format(suma_porcentaje)), fondo_blanco_border_blue_rigth)

        #range1 = 'G' + str(renglon + 4) + ':I' + str(renglon + 4)
        #range2 = 'J' + str(renglon + 4) + ':K' + str(renglon + 4)
        #worksheet.merge_range(range1, 'AVANCE EN ESTA ESTIMACIÓN', fondo_blanco_border_gray_center)
        #worksheet.merge_range(range2, '', fondo_blanco_border_gray_center)

        #range1 = 'G' + str(renglon + 6) + ':I' + str(renglon + 6)
        #range2 = 'J' + str(renglon + 6) + ':K' + str(renglon + 6)
        #worksheet.merge_range(range1, 'CANTIDAD POR EJECUTAR', fondo_blanco_border_gray_center)
        #worksheet.merge_range(range2, '', fondo_blanco_border_gray_center)

        #range1 = 'G' + str(renglon + 10)
        #worksheet.write(range1, sEstimate, fondo_verde_center)

        #firma del presidente
        range1 = 'I' + str(renglon + 8) + ':K' + str(renglon + 8)
        range2 = 'I' + str(renglon + 9) + ':K' + str(renglon + 9)
        range3 = 'I' + str(renglon + 10) + ':K' + str(renglon + 10)
        range4 = 'I' + str(renglon + 11) + ':K' + str(renglon + 11)
        worksheet.merge_range(range1, '', fondo_blanco_border_gray_center)
        worksheet.merge_range(range2, 'ING. ÓSCAR GERARDO SALCEDO GONZÁLEZ', merge_format_blanco_CENTER)
        worksheet.merge_range(range3, 'PRESIDENTE EMPRESARIAL', merge_format_blanco_CENTER)
        worksheet.merge_range(range4, 'SALCEDO CONST. Y SUP. S.A. DE C.V.', merge_format_blanco_CENTER)




    @staticmethod
    def get_char(indice,seccion):
        cChar=''
        if seccion ==1:
            if indice==0:
                cChar = 'A'
            elif indice == 1:
                cChar = 'B'
            elif indice == 2:
                cChar = 'C'
            elif indice == 3:
                cChar = 'D'
            elif indice == 4:
                cChar = 'E'
        else:
            if indice==0:
                cChar = 'G'
            elif indice == 1:
                cChar = 'H'
            elif indice == 2:
                cChar = 'I'
            elif indice == 3:
                cChar = 'J'
            elif indice == 4:
                cChar = 'K'
        return  cChar

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
