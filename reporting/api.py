# coding=utf-8

from __future__ import unicode_literals

from decimal import Decimal
from django.db.models import F
from django.db.models import Q, Count, Sum
from django.views.generic import View
from django.db.models.functions import TruncMonth

from ERP.models import LineItem, Concept_Input, ProgressEstimate, PaymentSchedule, Project, Estimate, \
    ContratoContratista, Contratista
import os, sys
sys.setdefaultencoding('utf-8')
from xlsxwriter.workbook import Workbook

import datetime
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.http import HttpResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper


class ReportingUtilities():
    @staticmethod
    def get_parent_from_array(line_item, parents_array):
        '''
        :param line_item: line_item to inspect.
        :param parents_array: list of line items to be checked as parents.
        :return: the id of the parent_line_item the sub_line_item belongs to.
        '''

        if line_item.id in parents_array:
            return line_item.id

        elif line_item.parent_line_item is not None:
            return ReportingUtilities.get_parent_from_array(line_item.parent_line_item,
                                                            parents_array)

        else:
            return None

    @staticmethod
    def check_if_line_item_is_parent(concept_input, parent_id):
        '''
        :param concept_input: concept_input to inspect.
        :param parent_id: The line_item to be evaluated as a parent.
        :return: True or False depending on whether the line_item is parent or not.
        '''

        if concept_input.line_item.id == parent_id:
            return True

        elif concept_input.line_item.parent_line_item is not None:
            parents_array = [parent_id]
            result = ReportingUtilities.get_parent_from_array(concept_input.line_item,
                                                            parents_array)
            if result is not None:
                return True

        return False

    @staticmethod
    def get_sub_line_items(line_item_obj):
        '''
        :param line_item: line_item object to inspect.
        :return: An array containing the sub_line_items.
        '''
        parents_array = [line_item_obj.id]
        sub_line_items_array = []

        line_items_set = LineItem.objects.filter(Q(project__id=line_item_obj.project.id))
        for line_item in line_items_set:
            result = ReportingUtilities.get_parent_from_array(line_item, parents_array)
            if result is not None:
                sub_line_items_array.append(line_item.id)

        return sub_line_items_array



    @staticmethod
    def get_first_two_line_item_levels(project_id):
        top_line_items = LineItem.objects.filter(Q(project_id=project_id) & Q(parent_line_item=None))
        top_line_items_array = []
        for each in top_line_items:
            top_line_items_array.append(each.id)

        second_level = LineItem.objects.filter(Q(parent_line_item__in=top_line_items_array))
        second_level_array = []

        for each in second_level:
            second_level_array.append(each.id)

        return second_level_array



class FinancialHistoricalProgressReport(View):


    @staticmethod
    def get_report(project_id, selected_line_items):

        # Final structure to response.
        structured_response = {
            "line_items" : []
        }

        # Defining a dictionary to be populated by the selected line item info, including the estimated amounts.
        selected_line_items_dictionary = {}
        for item in selected_line_items:
            current_line_item = LineItem.objects.get(pk=int(item))
            selected_line_items_dictionary[str(item)] = {
                'name': current_line_item.description,
                'line_item_key': current_line_item.key,
                'total_programmed': 0,
                'total_estimated': 0,
                'total_pending': 0
            }

        # Getting all the estimates for the project.
        estimates_set = Estimate.objects.filter(contract__project_id=project_id)
        for estimate in estimates_set:

            # Getting all the progresses for the current estimate and the global amount.
            progress_estimate_set = ProgressEstimate.objects.filter(estimate__id=estimate.id).values('estimate__id') \
                .annotate(Count('estimate__id'), total_estimated=Sum('amount'))

            # Getting the line_item from the selected_line_items the estimate belongs to.
            estimate_belongs_to = ReportingUtilities.get_parent_from_array(
                estimate.contract.line_item, selected_line_items)


            # If the estimate belongs to one of the selected line items.
            if estimate_belongs_to is not None and len(progress_estimate_set) > 0:
                current_estimate = selected_line_items_dictionary[str(estimate_belongs_to)]['total_estimated']
                # Assigning th values.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_estimated'] = float(current_estimate) + float(
                    progress_estimate_set[0]['total_estimated'])

                selected_line_items_dictionary[str(estimate_belongs_to)]['total_programmed'] = float(estimate.contract.monto_contrato)

                selected_line_items_dictionary[str(estimate_belongs_to)]['total_pending'] = float(
                    estimate.contract.monto_contrato) - selected_line_items_dictionary[str(estimate_belongs_to)][
                                                                                                'total_estimated']

        # Getting the top line items for the project
        top_line_items = LineItem.objects.filter(Q(project__id=project_id) & Q(parent_line_item=None))
        for top_line_item in top_line_items:
            temp_json = {
                "top_line_item_id": top_line_item.id,
                "top_line_item_key": top_line_item.key,
                "name": top_line_item.description,
                "total_programmed": 0,
                "total_estimated": 0,
                "total_pending": 0,
                "sub_line_items": [],
            }

            for key in selected_line_items_dictionary:
                line_item_obj = LineItem.objects.get(pk=int(key))
                if temp_json['top_line_item_id'] == line_item_obj.top_parent_line_item.id:
                    # Decimal to string to be able to serialize it.
                    temp_json['sub_line_items'].append(selected_line_items_dictionary[key])
                    temp_json['total_programmed'] += selected_line_items_dictionary[key]['total_programmed']
                    temp_json['total_pending'] += selected_line_items_dictionary[key]['total_pending']
                    temp_json['total_estimated'] += selected_line_items_dictionary[key]['total_estimated']

            structured_response['line_items'].append(temp_json)

        return structured_response


class PhysicalFinancialAdvanceReport(View):
    @staticmethod
    def get_report(project_id, selected_line_items_array, type='C'):
        structured_response = {}

        structured_response['physical_financial_advance'] = PhysicalFinancialAdvanceReport.get_physical_financial_advance(project_id,
                                                                                                          selected_line_items_array,
                                                                                                          type)

        structured_response['biddings_programs'] = PhysicalFinancialAdvanceReport.get_biddings_report(project_id)

        return structured_response

    @staticmethod
    def get_physical_financial_advance(project_id, selected_line_items, type):
        # Final structure to response.
        structured_response = {
            "line_items": []
        }

        # Defining a dictionary to be populated by the selected line item info, including the estimated amounts.
        selected_line_items_dictionary = {}
        for item in selected_line_items:
            current_line_item = LineItem.objects.get(pk=int(item))

            sub_line_items_array = ReportingUtilities.get_sub_line_items(current_line_item)
            # Getting all the concepts for the current line_item or its childs
            concept_input_set = Concept_Input.objects.filter(Q(line_item__id__in=sub_line_items_array))
            concepts_amount = 0
            for concept in concept_input_set:
                concepts_amount += (concept.quantity * concept.unit_price)


            selected_line_items_dictionary[str(item)] = {
                'name': current_line_item.description,
                'line_item_key': current_line_item.key,
                'total_programmed': float(concepts_amount),
                'total_contracted': 0,
                'total_physical_advance': 0,
                'total_financial_advance': 0,
                'total_programmed_tax': float(concepts_amount) * 1.16,
                'total_contracted_tax': 0,
                'total_physical_advance_tax': 0,
                'total_financial_advance_tax': 0,

            }

        # Getting all the estimates for the project.
        estimates_set = Estimate.objects.filter(contract__project_id=project_id)
        for estimate in estimates_set:

            # Getting the line_item from the selected_line_items the estimate belongs to.
            estimate_belongs_to = ReportingUtilities.get_parent_from_array(
                estimate.contract.line_item, selected_line_items)


            # Getting all the progresses for the physical report which means it doesn't matter if the estimate has
            # been paid or not
            physical_progress_estimate_set = ProgressEstimate.objects.filter(estimate__id=estimate.id).values('estimate__id') \
                .annotate(Count('estimate__id'), physical_advance_amount=Sum('amount'),
                          contracted_amount=Sum('estimate__contract__monto_contrato'))

            # Getting all the progresses for the financial report: paid progress estimates.
            financial_progress_estimate_set = ProgressEstimate.objects\
                .filter(Q(estimate__id=estimate.id) & Q(payment_status=ProgressEstimate.PAID)) \
                .values('estimate__id') \
                .annotate(Count('estimate__id'), total_financial=Sum('amount'))



            # If the estimate belongs to one of the selected line items.
            if estimate_belongs_to is not None and len(physical_progress_estimate_set) > 0:
                contracted = selected_line_items_dictionary[str(estimate_belongs_to)]['total_contracted']
                physical_advance = selected_line_items_dictionary[str(estimate_belongs_to)]['total_physical_advance']
                financial_advance = selected_line_items_dictionary[str(estimate_belongs_to)]['total_financial_advance']


                # With taxes.
                contracted_tax = selected_line_items_dictionary[str(estimate_belongs_to)]['total_contracted_tax']
                physical_advance_tax = selected_line_items_dictionary[str(estimate_belongs_to)]['total_physical_advance_tax']
                financial_advance_tax = selected_line_items_dictionary[str(estimate_belongs_to)]['total_financial_advance_tax']


                # Contracted Amount.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_contracted'] = float(contracted) \
                                                                                              + float(physical_progress_estimate_set[0]['contracted_amount'])
                # Physical Advance Amount.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_physical_advance'] = float(physical_advance) \
                                                                                               + float(physical_progress_estimate_set[0]['physical_advance_amount'])
                # Financial Advance Amount.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_financial_advance'] = float(
                    financial_advance) + float(financial_progress_estimate_set[0]['total_financial'])

                #------ Amounts with taxes included. ------
                estimate_tax = float(estimate.contract.porcentaje_iva) / 100

                # Contracted Amount with taxes.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_contracted_tax'] = float(contracted_tax) \
                                      + (float(physical_progress_estimate_set[0]['contracted_amount']) * estimate_tax)
                # Physical Advance Amount with taxes.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_physical_advance_tax'] = float(
                    physical_advance_tax) + (float(physical_progress_estimate_set[0]['physical_advance_amount']) * estimate_tax)

                # Financial Advance Amount with taxes.
                selected_line_items_dictionary[str(estimate_belongs_to)]['total_financial_advance_tax'] = float(
                    financial_advance_tax) + (float(financial_progress_estimate_set[0]['total_financial']) * estimate_tax)


        # Getting the top line items for the project
        top_line_items = LineItem.objects.filter(Q(project__id=project_id) & Q(parent_line_item=None))
        for top_line_item in top_line_items:
            temp_json = {
                "top_line_item_id": top_line_item.id,
                "top_line_item_key": top_line_item.key,
                "name": top_line_item.description,
                "sub_line_items": [],
            }

            for key in selected_line_items_dictionary:
                line_item_obj = LineItem.objects.get(pk=int(key))
                if temp_json['top_line_item_id'] == line_item_obj.top_parent_line_item.id:
                    # Decimal to string to be able to serialize it.
                    temp_json['sub_line_items'].append(selected_line_items_dictionary[key])

            structured_response['line_items'].append(temp_json)

        return structured_response

    @staticmethod
    def get_biddings_report(project_id):
        response = []

        # Getting the years found in the schedule.
        schedule_years = PaymentSchedule.objects.filter(project_id=project_id).values('year').annotate(Count('year')) \
            .order_by('year')


        # Years JSON.

        accumulated_paid_estimate = 0
        accumulated_total_estimate = 0
        acummulated_program = 0

        for year in schedule_years:
            temp_year = year['year']
            yearly_json = {}
            yearly_json['year'] = str(temp_year)
            yearly_json['months'] = []

            monthly_program = PaymentSchedule.objects.filter(Q(project_id=project_id) & Q(year=temp_year)) \
                .order_by('month')

            for record in monthly_program:

                month_paid_estimate = 0
                month_total_estimate = 0
                # Obtaining all the estimates for the current month and year.
                progress_estimate_set = ProgressEstimate.objects.filter(Q(estimate__contract__project__id=project_id)
                                                                        & Q(estimate__period__month=record.month)
                                                                        & Q(estimate__period__year=temp_year)).values('estimate__id').annotate(Count('estimate__id'), total=Sum('amount'))


                paid_progress_estimate_set = progress_estimate_set.filter(Q(payment_status='P'))

                total_amount = 0
                total_paid_amount = 0

                for each in progress_estimate_set:
                    total_amount += float(each['total'])

                for each in paid_progress_estimate_set:
                    total_paid_amount += float(each['total'])
                    estimate = Estimate.objects.get(pk=each['estimate__id'])
                    if estimate.advance_payment_status == Estimate.PAID:
                        total_paid_amount += float(estimate.advance_payment_amount)

                # Total amount for every estimate
                # Estimates that have been paid.
                month_total_estimate = total_amount

                # Estimates that have been paid.
                month_paid_estimate = round(total_paid_amount, 2)

                accumulated_total_estimate += round(month_total_estimate, 2)
                accumulated_paid_estimate += round(month_paid_estimate, 2)
                acummulated_program += round(record.amount, 2)

                yearly_json['months'].append({
                    "month": record.get_month_display(),
                    "accumulated_programmed": acummulated_program,
                    "accumulated_paid_estimate": accumulated_paid_estimate,
                    "accumulated_total_estimate": accumulated_total_estimate,
                    "month_program": float(record.amount),
                    "month_paid_estimate": float(month_paid_estimate),
                    "month_estimate": float(month_total_estimate),
                })

            response.append(yearly_json)

        return response

    @staticmethod
    def get_biddings_report_aux(project_id):

        response = []

        # Getting the years found in the schedule.
        schedule_years = PaymentSchedule.objects.filter(project_id=project_id).values('year').annotate(Count('year')) \
            .order_by('year')

        payment_schedule_grouped = schedule_years.values('project_id').annotate(Count('project_id'),
                                                                                total=Sum('amount'))

        # Years JSON.

        accumulated_paid_estimate = 0
        accumulated_total_estimate = 0
        acummulated_program = 0

        for year in schedule_years:
            temp_year = year['year']
            yearly_json = {}
            yearly_json['year'] = str(temp_year)
            yearly_json['months'] = []

            monthly_program = PaymentSchedule.objects.filter(Q(project_id=project_id) & Q(year=temp_year)) \
                .order_by('month')

            for record in monthly_program:

                month_paid_estimate = 0
                month_total_estimate = 0
                # Obtaining all the estimates for the current month and year.
                progress_estimate_set = ProgressEstimate.objects.filter(
                    Q(estimate__concept_input__line_item__project=project_id)
                    & Q(estimate__start_date__month=record.month)
                    & Q(estimate__start_date__year=temp_year)) \
                    .values('estimate__concept_input__line_item__project__id') \
                    .annotate(Count('estimate__concept_input__line_item__project__id'), total=Sum('amount'))

                paid_progress_estimate_set = progress_estimate_set.filter(Q(payment_status='P'))

                # Total amount for every estimate
                # Estimates that have been paid.
                if progress_estimate_set.exists():
                    month_total_estimate = progress_estimate_set[0]['total']

                # Estimates that have been paid.
                if paid_progress_estimate_set.exists():
                    month_paid_estimate = round(paid_progress_estimate_set[0]['total'], 2)

                accumulated_total_estimate += round(month_total_estimate, 2)
                accumulated_paid_estimate += round(month_paid_estimate, 2)
                acummulated_program += round(record.amount, 2)

                cjson = {}
                cjson['month'] = record.get_month_display()
                cjson['category'] = []
                cjson['category'].append({
                    "total": acummulated_program,
                    "name": "Programado Acumulado",
                })
                cjson['category'].append({
                    "total": accumulated_paid_estimate,
                    "name": "Estimación Pagada Acumulada",
                })
                cjson['category'].append({
                    "total": accumulated_total_estimate,
                    "name": "Estimación Total Acumulada",
                })
                cjson['category'].append({
                    "total": round(record.amount, 2),
                    "name": "Progamado Mensual",
                })
                cjson['category'].append({
                    "total": month_paid_estimate,
                    "name": "Pago Estimado Mensual",
                })

                yearly_json['months'].append(cjson)

            response.append(yearly_json)

        return response


class EstimatesReport():
    @staticmethod
    def getReport(project_id):

        response = []

        project = Project.objects.get(pk=project_id)
        estimate_set = Estimate.objects.filter(contract__project__id=project_id)

        for estimate in estimate_set:
            concepts_array = []
            contract_obj = ContratoContratista.objects.get(pk=estimate.contract.id)
            for concept in contract_obj.concepts.all():
                concepts_array.append({
                    'concept_name': concept.description,
                    'concept_key': concept.key
                })

            estimate_json = {
                'contractor_name': estimate.contract.contratista.nombreContratista,
                'contract_amount_with_tax': float(estimate.contract.monto_contrato) * 1.16,
                'concepts': concepts_array,
                'project': estimate.contract.project.nombreProyecto,
                'line_item': estimate.contract.line_item.description,
                'start_date': str(estimate.start_date.strftime('%m/%d/%Y')),
                'end_date': str(estimate.end_date.strftime('%m/%d/%Y')),
                'period': str(estimate.period.strftime('%m/%d/%Y')),
                'total_physical_estimate_amount': 0,
                'total_financial_estimate_amount': 0,
                'financial_advance': {
                    'advance_payment': float(estimate.advance_payment_amount),
                    'progress_estimate':[]
                },
                'physical_advance':{
                    'progress_estimate': []
                }

            }

            progress_estimate_set = ProgressEstimate.objects.filter(Q(estimate__id=estimate.id))

            # Physical Adavance:
            for progress_estimate in progress_estimate_set:
                progress_estimate_json = {
                    'progress_estimate_amount': float(progress_estimate.amount),
                    'progress_estimate_key': progress_estimate.key,
                    'percentage': round(float(progress_estimate.amount) * 100 / estimate_json['contract_amount_with_tax'], 2)
                }
                estimate_json['physical_advance']['progress_estimate'].append(progress_estimate_json)
                # Adding to the general amount
                estimate_json['total_physical_estimate_amount'] += float(progress_estimate.amount)


            # Financial Advance:
            not_paid_progress_estimate_set = ProgressEstimate.objects.filter(Q(estimate__id=estimate.id)&Q(payment_status=ProgressEstimate.PAID))

            # Physical Adavance:
            for progress_estimate in not_paid_progress_estimate_set:
                progress_estimate_json = {
                    'progress_estimate_amount': float(progress_estimate.amount),
                    'progress_estimate_key': progress_estimate.key
                }
                estimate_json['financial_advance']['progress_estimate'].append(progress_estimate_json)
                # Adding to the general amount
                estimate_json['total_financial_estimate_amount'] += float(progress_estimate.amount)

            response.append(estimate_json)



        return response



class EstimateReportByContractor():
    @staticmethod
    def get_report(project_id):
        response = {}
        response['data'] = []

        project_obj = Project.objects.get(pk=project_id)
        response['project_key'] = project_obj.key
        response['project_name'] = project_obj.nombreProyecto
        response['project_start_date'] = str(project_obj.fecha_inicial)
        response['project_end_date'] = str(project_obj.fecha_final)

        # Getting all the contracts in a project grouped by contractor.
        contracts_set = ContratoContratista.objects.filter(project_id=project_id).values('contratista_id').annotate(Count('contratista_id'))

        for contract in contracts_set:
            contractor_id = contract['contratista_id']
            contractor_obj = Contratista.objects.get(pk=contractor_id)

            contractor_json = {
                'contractor_name': contractor_obj.nombreContratista,
                'estimates': []
            }

            # Getting all the estimates for a contractor in a .
            estimates_set = Estimate.objects.filter(contract__contratista__id=contractor_obj.id)
            for estimate in estimates_set:
                estimate_json = {
                    'estimate_start_date': str(estimate.start_date),
                    'estimate_end_date': str(estimate.end_date),
                    'estimate_period': str(estimate.period),
                    'progress_estimates': [{
                        'key': 'Avance',
                        'amount': float(estimate.advance_payment_amount),
                        'status': progress_estimate.get_payment_status_display(),
                    }]
                }
                progress_estimate_set = ProgressEstimate.objects.filter(estimate__id = estimate.id)
                for progress_estimate in progress_estimate_set:
                    pe_json = {
                        'key': progress_estimate.key,
                        'amount': float(progress_estimate.amount),
                        'status': progress_estimate.get_payment_status_display(),
                    }




        print contracts_set

        return response
