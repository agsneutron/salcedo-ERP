# coding=utf-8
from django.db.models.aggregates import Count, Sum

import StringIO
from rexec import FileWrapper

from django.http.response import StreamingHttpResponse
from xlsxwriter.workbook import Workbook

from Accounting.models import FiscalPeriod


class TrialBalanceReport():

    @staticmethod
    def generate_report(general_data, policies_details_set):
        """
        Entry point to generate the trial report.

        :param general_data: General Data for the report, such as Fiscal Period, Year, etc.
        :param policies_details_set: Set of policy details to be processed.
        :return: HttpResponse containing the downloadable file.
        """

        output = StringIO.StringIO()
        workbook = Workbook(output)
        worksheet = workbook.add_worksheet('Balanza de Comprobación')


        if len(policies_details_set) == 0:
            # Widen the first column to make the text clearer.
            #worksheet.write('A1', 'No se encontraron datos pertenecientes al periodo.')
            pass


        else:
            TrialBalanceReport.add_headers(workbook, worksheet, general_data)
            TrialBalanceReport.add_policies_details(workbook, worksheet, policies_details_set)



        workbook.close()
        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=Balanza_de_Comprobación.xlsx'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response


    @staticmethod
    def add_headers(workbook, worksheet, general_data):
        """
        Adds the necessary headers to the worksheet.

        :param workbook: Workbook Object.
        :param worksheet: Worksheet Object.
        :param general_data: Data to set info in the headers section.
        """

        formats = TrialBalanceReport.get_formats(workbook)

        # Formats
        blue_header_format_info = formats['blue_header_format_info']
        white_centered_bold_header = formats['white_centered_bold_header']
        white_bold_header = formats['white_bold_header']


        worksheet.set_column('A:F', 20)


        # Row 1.
        if general_data['title'] is None or general_data['title'] == "":
            title = "Balance de Comprobación de Sumas y Saldos"
        else:
            title = general_data['title']

        worksheet.merge_range('A1:F1', title, white_centered_bold_header)

        # Row 2.
        worksheet.merge_range('A2:C2', "Salcedo Construcción y Supervisión", white_bold_header)
        # Line Commented until definition of CUIT.
        #worksheet.merge_range('D2:F2', "CUIT", white_bold_header)

        # Row 3.
        month_number = int(general_data['month'])
        year_number = int(general_data['year'])

        worksheet.merge_range('A3:C3', FiscalPeriod.get_month_name_from_number(month_number) + " " + str(year_number), white_bold_header)


        # Table headers.
        worksheet.merge_range('A5:A6', "N. Orden", blue_header_format_info)
        worksheet.merge_range('B5:B6', "Cuenta", blue_header_format_info)

        worksheet.merge_range('C5:D5', "Sumas", blue_header_format_info)
        worksheet.write('C6', "Debe", blue_header_format_info)
        worksheet.write('D6', "Haber", blue_header_format_info)

        worksheet.merge_range('E5:F5', "Sumas", blue_header_format_info)
        worksheet.write('E6', "Deudor", blue_header_format_info)
        worksheet.write('F6', "Acreedor", blue_header_format_info)


    @staticmethod
    def get_formats(workbook):
        formats = {}

        # Format with blue background and white letters.
        blue_header_format_info = {
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#3E84CF',
            'border_color': '#000000',
            'font_color': '#FFFFFF'
        }
        formats['blue_header_format_info'] = workbook.add_format(blue_header_format_info)

        # Format with white background and bold centered text.
        white_centered_bold_header_info = {
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1
        }
        formats['white_centered_bold_header'] = workbook.add_format(white_centered_bold_header_info)

        # Format with white background and bold text aligned to the left.
        white_bold_header_info = {
            'align': 'left',
            'valign': 'vcenter',
            'bold': 1
        }
        formats['white_bold_header'] = workbook.add_format(white_bold_header_info)

        # Format with white background and bold text aligned to the left with black border.
        white_bold_record_info = {
            'align': 'left',
            'valign': 'vcenter',
            'bold': 1,
            'border': 1,
            'border_color':'#000000'
        }
        formats['white_bold_record'] = workbook.add_format(white_bold_record_info)

        # Format with white background and bold text aligned to the right with black border for currency.
        white_bold_right_currency_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'num_format': '$#,#00.00',
            'bold':1
        }
        formats['white_bold_right_currency'] = workbook.add_format(white_bold_right_currency_info)

        # Format with gray background and bold text aligned to the right with black border for currency.
        gray_bold_right_currency_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'num_format': '$#,#00.00',
            'bold': 1,
            'fg_color':'#E8E8E8'
        }
        formats['gray_bold_right_currency'] = workbook.add_format(gray_bold_right_currency_info)

        # Format with yellow background and bold text aligned to the right.
        yellow_total_right_info = {
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'border_color': '#000000',
            'bold': 1,
            'fg_color': '#FDB709'
        }
        formats['yellow_total_right'] = workbook.add_format(yellow_total_right_info)


        return formats


    @staticmethod
    def add_policies_details(workbook, worksheet, policy_detail_set):
        """
        Takes a set of policy details and processes it to define the amount of debit and credit related to an
         account.

        :param workbook: Workbook Object.
        :param worksheet: Worksheet Object.
        :param policies_set: Set of policies that were found for the given fiscal period and account ranges.

        """
        START_ROW = 6

        COUNTER_COL = 0
        ACCOUNT_COL = 1
        DEBIT_COL = 2
        CREDIT_COL = 3
        DEBTOR_COL = 4
        CREDITOR_COL = 5


        # Getting the formats.
        formats = TrialBalanceReport.get_formats(workbook)
        white_bold_record = formats['white_bold_record']
        white_bold_right_currency = formats['white_bold_right_currency']
        gray_bold_right_currency = formats['gray_bold_right_currency']
        yellow_total_right = formats['yellow_total_right']

        grouped_by_account_policies_set = policy_detail_set.values('account__grouping_code__id','account__grouping_code__account_name')\
            .annotate(Count('account__grouping_code__id'), Count('account__grouping_code__account_name'), total_credit=Sum('credit'), total_debit=Sum('debit'))

        row_counter = START_ROW
        counter = 1

        # To keep track of the accumulates.
        accumulated_credit = 0
        accumulated_debit = 0
        accumulated_debtor = 0
        accumulated_creditor = 0


        for account_record in grouped_by_account_policies_set:

            name = account_record['account__grouping_code__account_name']
            total_credit = account_record['total_credit']
            total_debit = account_record['total_debit']

            total_debtor = total_credit - total_debit
            total_creditor = total_debit - total_credit

            # Short if. If the value is negative, then turn it into 0.
            total_debtor = 0 if total_debtor <= 0 else total_debtor
            total_creditor = 0 if total_creditor <= 0 else total_creditor

            worksheet.write(row_counter, COUNTER_COL, counter, white_bold_record)
            worksheet.write(row_counter, ACCOUNT_COL, name, white_bold_record)
            worksheet.write(row_counter, DEBIT_COL, total_debit, white_bold_right_currency)
            worksheet.write(row_counter, CREDIT_COL, total_credit, white_bold_right_currency)
            worksheet.write(row_counter, DEBTOR_COL, total_debtor, gray_bold_right_currency)
            worksheet.write(row_counter, CREDITOR_COL, total_creditor, gray_bold_right_currency)

            # Adding to the accumulates.
            accumulated_credit += total_credit
            accumulated_debit += total_debit
            accumulated_debtor += total_debtor
            accumulated_creditor += total_creditor

            row_counter += 1
            counter += 1

        # Adding the accumulated values to the worksheet.

        worksheet.write(row_counter+1, ACCOUNT_COL, "Total", yellow_total_right)
        worksheet.write(row_counter+1, DEBIT_COL, accumulated_debit, white_bold_right_currency)
        worksheet.write(row_counter+1, CREDIT_COL, accumulated_credit, white_bold_right_currency)
        worksheet.write(row_counter+1, DEBTOR_COL, accumulated_debtor, white_bold_right_currency)
        worksheet.write(row_counter+1, CREDITOR_COL, accumulated_creditor, white_bold_right_currency)




