# coding=utf-8
from __future__ import unicode_literals

from decimal import Decimal
from django.db.models import F
from django.db.models import Q, Count, Sum
from django.views.generic import View
from django.db.models.functions import TruncMonth

from ERP.models import LineItem, Concept_Input, ProgressEstimate, PaymentSchedule, Project, Estimate


class FinancialHistoricalProgressReport(View):
    @staticmethod
    def check_if_node_is_parents_array(line_item, parents_array):

        if line_item.id in parents_array:
            return line_item.id

        elif line_item.parent_line_item is not None:
            return FinancialHistoricalProgressReport.check_if_node_is_parents_array(line_item.parent_line_item,
                                                                                    parents_array)

        else:
            return None

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
            estimate_belongs_to = FinancialHistoricalProgressReport.check_if_node_is_parents_array(
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
    def get_report(project_id, type='C'):
        structured_response = {}

        structured_response[
            'physical_financial_advance'] = PhysicalFinancialAdvanceReport.get_physical_financial_advance(project_id,
                                                                                                          type)
        structured_response['biddings_programs'] = PhysicalFinancialAdvanceReport.get_biddings_report(project_id)

        return structured_response

    @staticmethod
    def get_physical_financial_advance(project_id, type):
        # Get Line Items
        response = []

        line_items = LineItem.objects.filter(project_id=project_id)

        for line_item in line_items:
            line_item_record = {
                'line_item_name': line_item.description
            }

            # Get programmed
            line_item_concepts = Concept_Input.objects.filter(Q(type=type) & Q(line_item_id=line_item.id))
            total_programmed = 0  # The amount programmed for the line item
            total_physical_advance = 0
            total_financial_advance = 0
            for concept in line_item_concepts:
                programmed_for_concept = concept.quantity * concept.unit_price
                total_programmed += programmed_for_concept

                #  All the estimates for the concept
                estimated = ProgressEstimate.objects.filter(estimate__concept_input_id=concept.id).values(
                    'estimate__concept_input_id').annotate(Count('estimate__concept_input_id'),
                                                           total_estimated=Sum('amount'))

                if estimated.exists():
                    total_estimated = estimated[0]['total_estimated']
                    total_physical_advance += total_estimated

                # All the PAID estimates for the concept
                estimated = ProgressEstimate.objects.filter(
                    Q(estimate__concept_input_id=concept.id) & Q(payment_status=ProgressEstimate.PAID)).values(
                    'estimate__concept_input_id').annotate(Count('estimate__concept_input_id'),
                                                           total_estimated=Sum('amount'))

                if estimated.exists():
                    total_estimated = estimated[0]['total_estimated']
                    total_financial_advance += total_estimated

            line_item_record['total_programmed'] = total_programmed
            line_item_record['total_physical_advance'] = total_physical_advance
            line_item_record['total_financial_advance'] = total_financial_advance

            response.append(line_item_record)

        return response

    @staticmethod
    def get_biddings_report(project_id):

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
                progress_estimate_set = ProgressEstimate.objects.filter(Q(estimate__contract__project__id=project_id)
                                                                        & Q(estimate__start_date__month=record.month)
                                                                        & Q(estimate__start_date__year=temp_year)) \
                    .values('estimate__contract__project__id') \
                    .annotate(Count('estimate__contract__project__id'), total=Sum('amount'))

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
