# coding=utf-8


from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import enums
from reportlab.platypus.flowables import PageBreak


class EmployeePaymentReceipt:

    @staticmethod
    def generate_employee_payment_receipts(receipts_data):
        cm = 2.54

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        pages = []

        doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=3.5 * cm, topMargin=50 * cm, bottomMargin=0)

        for receipt in receipts_data:
            receipt_page = EmployeePaymentReceipt.generate_receipt_page(receipt)
            pages += receipt_page



        doc.build(pages)
        return response





    @staticmethod
    def generate_receipt_page(receipt_data):
        page = []
        cm = 2.54
        line_break = Paragraph("<br />", EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)

        # SALCEDO Headers.
        company_name = "<strong>SALCEDO CONSTRUCCIÓN Y SUPERVISIÓN S.A. DE C.V.</strong>"
        paragraph = Paragraph(company_name, EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)
        page.append(paragraph)


        employer_registration = "<strong>REGISTRO PATRONAL: C6213152104</strong>"
        paragraph = Paragraph(employer_registration, EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)
        page.append(paragraph)



        rfc = "<strong>R.F.C: SCS111017F27</strong>"
        paragraph = Paragraph(rfc, EmployeePaymentReceipt.Styles.HEADERS_PARAGRAPH_STYLE)
        page.append(paragraph)






        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)





        # Employee personal data table.
        employee_number_label = Paragraph('<strong>No. de Trabajador:</strong> '+receipt_data['employee_key'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        rfc_label = Paragraph('<strong>RFC:</strong> '+receipt_data['rfc'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        employee_name_label = Paragraph('<strong>Nombre del Trabajador:</strong> '+receipt_data['employee_fullname'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)
        employee_ssn_label = Paragraph('<strong>NSS:</strong> '+receipt_data['ssn'], EmployeePaymentReceipt.Styles.EMPLOYEE_LABEL_PARAGRAPH_STYLE)

        data = [
            [employee_number_label, rfc_label],
            [employee_name_label, employee_ssn_label],
        ]
        employee_table = Table(data, colWidths=92*cm, rowHeights=(10*cm, 15*cm))
        employee_table.setStyle(EmployeePaymentReceipt.Styles.EMPLOYEE_INFO_TABLE_STYLE)

        page.append(employee_table)





        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)






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

        page.append(earnings_and_deductions_table)






        # Adding breaklines to separate the headers from the next table.
        page.append(line_break)
        page.append(line_break)
        page.append(line_break)




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
        page.append(totals_table)


        # End Page.
        page.append(PageBreak())




        return page



    class Styles:
        EMPLOYEE_INFO_TABLE_STYLE = TableStyle([
            ('BACKGROUND', (0, 0), (1, 1), colors.Color(.16, .3, .5)),
            ('GRID', (0, 0), (1, 1),1, colors.black),
            ('TEXTCOLOR', (0, 0), (1, 1), colors.white),
            ('FONTNAME', (0, 0), (1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (1, 1),10),
            ('VALIGN', (0, 0), (1, 1), 'MIDDLE')
        ])


        HEADERS_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=11,
            alignment=enums.TA_CENTER,
            spaceAfter=5
        )


        EMPLOYEE_LABEL_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_LEFT,
            textColor=colors.white
        )



        # Earnings and deductions styling.


        EARNINGS_AND_DEDUCTIONS_TABLE_STYLE = TableStyle([
            # Headers.
            ('BACKGROUND', (0, 0), (1, 0), colors.Color(.06, .3, .5)),
            ('GRID', (0, 0), (1, 0), 0, colors.black),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (1, 0), 10),

            # Data.

        ])


        EARNINGS_AND_DEDUCTIONS_HEADERS_PARAGRAPH_STYLE = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=enums.TA_CENTER,
            textColor=colors.white
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
