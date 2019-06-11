# coding=utf-8
import os

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import enums
from reportlab.platypus.flowables import PageBreak, Image

from SalcedoERP import settings


def get_none(the_string):
    if the_string is None:
        the_string = ""
    return the_string


class EmployeePaymentReceipt:

    @staticmethod
    def generate_employee_payment_receipts(receipts_data, company):
        cm = 2.54

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        pages = []

        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=3.5 * cm, topMargin=15 * cm, bottomMargin=0)

        add_bp = 0
        pagenumber = 1
        for receipt in receipts_data:
            # breakpage = 1
            receipt_page, add_bp = EmployeePaymentReceipt.generate_receipt_page(receipt, company, pagenumber, add_bp)
            pagenumber += 1
            pages += receipt_page
        doc.build(pages)
        return response


    @staticmethod
    def generate_receipt_page(receipt_data, company, pagenumber, add_bp):
        page = []
        cm = 2.54
        line_break = Paragraph("<br />", EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)

        #internal company values for header
        company_name_value = ""
        company_rfc_value = ""
        company_dir_value = ""
        company_logo_value = ""
        for company_values in company:
            company_name_value = get_none(company_values.name)
            company_rfc_value = get_none(company_values.rfc)
            company_dir_value = get_none(company_values.street) + " No. " + get_none(company_values.outdoor_number) + ", " + get_none(company_values.colony) + ", " + get_none(company_values.town.nombreMunicipio) + ", " + get_none(company_values.state.nombreEstado) + ". C.P. " + get_none(company_values.zip_code)
            company_logo_value = get_none(company_values.logo_file)

        # SALCEDO Headers.

        company_logo = os.path.join(settings.MEDIA_ROOT, str(company_logo_value))
        imagen = Image(company_logo, width=90, height=50, hAlign='LEFT')

        company_name = Paragraph("<strong>"+company_name_value+"</strong>", EmployeePaymentReceipt.Styles.HEADERS_TITLE_STYLE)
        employer_registration = Paragraph("<strong>R.F.C. " + company_rfc_value + "</strong>", EmployeePaymentReceipt.Styles.HEADERS_TITLE_STYLE)

        rfc = Paragraph("<strong>DIRECCIÓN: " + company_dir_value + "</strong>", EmployeePaymentReceipt.Styles.HEADERS_SUBTITLE_STYLE)

        encabezado = [[imagen, company_name],
                      ['', employer_registration],
                      ['', rfc]]
        tabla_encabezado = Table(encabezado, colWidths=(40*cm, 144*cm))
        tabla_encabezado.setStyle(EmployeePaymentReceipt.Styles.EMPLOYEE_HEADER_TABLE_STYLE)



        titulo = "<strong> RECIBO DE PAGO " + receipt_data['periodicity'] +" </strong>"
        paragraph = Paragraph(titulo, EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)


        # Employee personal data table.
        employee_number_label = Paragraph('<strong>No. de Trabajador:</strong> '+receipt_data['employee_key'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        rfc_label = Paragraph('<strong>RFC:</strong> '+receipt_data['rfc'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        periodo_label = Paragraph('<strong>Periodo:</strong> ' + receipt_data['start'] + ' - ' + receipt_data['end'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        curp_label = Paragraph('<strong>CURP:</strong> ' + receipt_data['curp'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)

        employee_name_label = Paragraph('<strong>Nombre del Trabajador:</strong> '+receipt_data['employee_fullname'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        employee_ssn_label = Paragraph('<strong>NSS:</strong> '+receipt_data['ssn'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)


        data = [
            [employee_number_label, rfc_label],
            [periodo_label, curp_label],
            [employee_name_label, employee_ssn_label],
        ]
        employee_table = Table(data, colWidths=92*cm, rowHeights=(10*cm, 10*cm, 10*cm))
        employee_table.setStyle(EmployeePaymentReceipt.Styles.EMPLOYEE_INFO_TABLE_STYLE)


        # Earnings and deductions table.
        earnings_label = Paragraph('<strong>PERCEPCIONES</strong>', EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_HEADERS_PARAGRAPH_STYLE)
        deductions_label = Paragraph('<strong>DEDUCCIONES</strong>', EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_HEADERS_PARAGRAPH_STYLE)


        earnings_deductions_data = [
            [earnings_label, deductions_label]
        ]


        number_of_earnings = len(receipt_data['earnings'])
        number_of_deductions = len(receipt_data['deductions'])

        if number_of_earnings >= number_of_deductions:
            total_rows = number_of_earnings
        else:
            total_rows = number_of_deductions

        for i in range(total_rows):

            table_row = []

            earnings_cell = []
            deductions_cell = []
            earnings_data = []
            deductions_data = []

            try:
                earnings_record = receipt_data['earnings'][i]
                name = Paragraph(earnings_record['name'],
                                 EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
                amount = Paragraph("$ " + str(earnings_record['amount']),
                                   EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
                earnings_data.append(name)
                earnings_data.append(amount)

            except IndexError as error:
                earnings_data.append('')
                earnings_data.append('')

            earnings_cell.append(earnings_data)
            earnings_table = Table(earnings_cell, colWidths=(60*cm, 40*cm), rowHeights=20)
            table_row.append(earnings_table)

            try:
                deductions_record = receipt_data['deductions'][i]
                name = Paragraph(deductions_record['name'], EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
                amount = Paragraph("$ " + str(deductions_record['amount']), EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
                deductions_data.append(name)
                deductions_data.append(amount)

            except IndexError as error:
                deductions_data.append('')
                deductions_data.append('')

            deductions_cell.append(deductions_data)

            deductions_table = Table(deductions_cell, colWidths=(60*cm, 40*cm), rowHeights=20)
            table_row.append(deductions_table)

            earnings_deductions_data.append(table_row)

        earnings_and_deductions_table = Table(earnings_deductions_data, colWidths=92*cm, rowHeights=20)
        earnings_and_deductions_table.setStyle(EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TABLE_STYLE)
        wrap_style = EmployeePaymentReceipt.Styles.wrap_earnings_and_deductions(total_rows)
        earnings_and_deductions_table.setStyle(wrap_style)



        # Totals.
        total_earnings_label = Paragraph('<strong>Total de Percepciones</strong>', EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
        total_deductions_label = Paragraph('<strong>Total de Deducciones</strong>', EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)
        net_salary_label = Paragraph('<strong>Salario Neto</strong>', EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE)

        total_earnings = Paragraph("$ " + receipt_data['total_earnings'], EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_RIGHT_STYLE)
        total_deductions = Paragraph("$ " + receipt_data['total_deductions'], EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_RIGHT_STYLE)

        net_salary_amount = float(receipt_data['total_earnings']) - float(receipt_data['total_deductions'])
        net_salary = Paragraph("$ " + str(net_salary_amount), EmployeePaymentReceipt.Styles.EARNINGS_AND_DEDUCTIONS_TEXT_RIGHT_STYLE)

        total_earnings_cell = [[total_earnings_label, total_earnings]]
        total_earnings_table = Table(total_earnings_cell, colWidths=(40*cm, 40*cm), rowHeights=20)

        total_deductions_cell = [[total_deductions_label, total_deductions]]
        total_deductions_table = Table(total_deductions_cell, colWidths=(40 * cm, 40 * cm), rowHeights=20)

        net_salary_cell = [[net_salary_label, net_salary]]
        net_salary_table = Table(net_salary_cell, colWidths=(40 * cm, 40 * cm), rowHeights=20)

        totals_data = [
            [total_earnings_table, total_deductions_table],
            ['', net_salary_table]
        ]
        totals_table = Table(totals_data, colWidths=(92*cm), rowHeights=20)

        breakpage = 0
        if total_rows > 5 and add_bp == 0 and pagenumber > 1:
            page.append(PageBreak())
            breakpage = 1

        #begin page
        page.append(tabla_encabezado)

        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)

        page.append(paragraph)

        page.append(employee_table)

        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)

        page.append(earnings_and_deductions_table)

        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)

        page.append(totals_table)
        # End Page.

        if total_rows > 5:
            page.append(PageBreak())
            breakpage = 1
        else:
            if add_bp == 1:
                # es estado de cuenta corto y hubo corte de pagina anterior entonces sólo agregamos espacios
                breakpage = 0   # anotamos que no hay corte de página
                page.append(line_break)
                page.append(line_break)
                page.append(line_break)
            elif add_bp == 0 and pagenumber > 1:
                # es estado de cuenta corto y no hubo corte de pagina anterior entonces hacemos corte de página
                page.append(PageBreak())
                breakpage = 1   # anotamos que hay corte de página

        #if breakpage % 2 != 0:
        #    if pagebreak:
        #        page.append(PageBreak())
        #else:
        #        page.append(line_break)
        #        page.append(line_break)
        #        page.append(line_break)

        return page, breakpage



    class Styles:
        EMPLOYEE_INFO_TABLE_STYLE = TableStyle([
            ('BACKGROUND', (0, 0), (1, 2), colors.white),
            ('GRID', (0, 0), (1, 2),1, colors.black),
            ('TEXTCOLOR', (0, 0), (1, 2), colors.black),
            ('FONTNAME', (0, 0), (1, 2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (1, 2),10),
            ('VALIGN', (0, 0), (1, 2), 'MIDDLE')
        ])

        EMPLOYEE_HEADER_TABLE_STYLE = TableStyle([
            ('BACKGROUND', (0, 0), (1, 2), colors.white),
            ('TEXTCOLOR', (0, 0), (1, 2), colors.black),
            ('FONTNAME', (0, 0), (1, 2), 'Helvetica'),
            ('VALIGN', (0, 0), (0, 2), 'MIDDLE'),
            ('VALIGN', (0, 1), (1, 2), 'TOP'),
            ('SPAN', (0, 0), (0, 2)),

        ])

        HEADERS_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=10,
            alignment=enums.TA_CENTER,
            spaceAfter=4
        )

        HEADERS_TITLE_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=10,
            alignment=enums.TA_RIGHT,
            spaceAfter=4
        )

        HEADERS_SUBTITLE_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_RIGHT,
            spaceAfter=4
        )


        EMPLOYEE_LABEL_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_LEFT,
            textColor=colors.black
        )



        # Earnings and deductions styling.


        EARNINGS_AND_DEDUCTIONS_TABLE_STYLE = TableStyle([
            # Headers.
            ('BACKGROUND', (0, 0), (1, 0), '#a8a8a8'),
            ('GRID', (0, 0), (1, 0), 0, colors.black),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (1, 0), 8),

            # Data.

        ])


        EARNINGS_AND_DEDUCTIONS_HEADERS_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_CENTER,
            textColor=colors.black
        )

        EARNINGS_AND_DEDUCTIONS_TEXT_LEFT_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_LEFT,
            textColor=colors.black
        )

        EARNINGS_AND_DEDUCTIONS_TEXT_RIGHT_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_RIGHT,
            textColor=colors.black
        )



        # Generic Styling.
        PLAIN_PARAGRAPH_STYLE = ParagraphStyle([])

        @staticmethod
        def wrap_earnings_and_deductions(number_of_rows):
            style = TableStyle([
                # Headers.
                ('BOX', (0, 1), (0, number_of_rows), 1, colors.black),      # Earnings
                ('BOX', (1, 1), (1, number_of_rows), 1, colors.black),      # Deductions
                ('BOX', (0, 1), (1, number_of_rows), 1, colors.black),      # Main Wrap.

            ])

            return  style
