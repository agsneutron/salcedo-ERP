# coding=utf-8
from __future__ import unicode_literals

from decimal import Decimal
from django.db.models import F
from django.db.models import Q, Count, Sum
from django.views.generic import View
from django.db.models.functions import TruncMonth

from ERP.models import LineItem, Concept_Input, ProgressEstimate, PaymentSchedule, Project


class FinancialHistoricalProgressReport(View):
	@staticmethod
	def get_report(project_id):
		# project_id = request.GET.get('project_id')  # The project for which we will make the report.

		line_items = LineItem.objects.filter(project_id=project_id)
		type = 'C'

		response = []
		structured_response = {}
		structured_line_items = []
		parent_keys = {}
		line_item_general_programmed = {}
		line_item_general_estimated = {}

		global_total_programmed = 0
		global_total_estimated = 0

		for line_item in line_items:
			temp_concepts = Concept_Input.objects.filter(Q(type=type) & Q(line_item_id=line_item.id))

			parent_line_item_key = LineItem.objects.filter(pk=line_item.parent_line_item_id)

			tem_obj = {"key": line_item.key, "parent_key": parent_line_item_key, 'name': line_item.description}

			# Check if line item has parent
			if len(parent_line_item_key) > 0:
				# There's a parent, assing it's information
				tem_obj['parent_key'] = parent_line_item_key[0].key
				parent_keys[str(line_item.key)] = str(parent_line_item_key[0].key)
				is_sub_line_item = True
			else:
				# There's no parent, leave empty
				tem_obj['parent_key'] = ''
				parent_keys[str(line_item.key)] = ''
				is_sub_line_item = False

			concepts = []
			# Get concepts info
			for concept in temp_concepts:

				concept_info = {
					'concept_key': concept.key,
					'total_programmed': str(concept.unit_price * concept.quantity)
				}

				estimated = ProgressEstimate.objects.filter(estimate__concept_input_id=concept.id).values(
					'estimate__concept_input_id').annotate(Count('estimate__concept_input_id'),
														   total_estimated=Sum('amount'))

				if estimated.exists():
					total_estimated = estimated[0]['total_estimated']
					concept_info['total_estimated'] = str(total_estimated)
					concept_info['total_pending'] = str(
						Decimal(concept_info['total_programmed']) - Decimal(concept_info['total_estimated']))

					if str(line_item.key) not in line_item_general_estimated.keys():
						line_item_general_estimated[str(line_item.key)] = 0
						line_item_general_estimated[str(line_item.key)] = line_item_general_estimated[
																			  str(line_item.key)] + total_estimated
				else:
					concept_info['total_estimated'] = '0.00'
					concept_info['total_pending'] = concept_info['total_programmed']

				concepts.append(concept_info)

			tem_obj['concepts'] = concepts

			programmed = temp_concepts.values('line_item_id').annotate(Count('line_item_id'),
																	   total_programmed=Sum(
																		   F('unit_price') * F('quantity')))

			estimated = ProgressEstimate.objects.filter(estimate__concept_input__line_item_id=line_item.id).values(
				'estimate__concept_input__line_item_id').annotate(Count('estimate__concept_input__line_item_id'),
																  total_estimated=Sum('amount'))

			if programmed.exists():
				total_programmed = programmed[0]['total_programmed']
				if str(line_item.key) not in line_item_general_programmed.keys():
					line_item_general_programmed[str(line_item.key)] = 0
				line_item_general_programmed[str(line_item.key)] = line_item_general_programmed[
																	   str(line_item.key)] + total_programmed
				tem_obj['total_programmed'] = str(total_programmed)
				global_total_programmed = global_total_programmed + total_programmed
			else:
				tem_obj['total_programmed'] = '0.00'

			if estimated.exists():
				total_estimated = estimated[0]['total_estimated']
				tem_obj['total_estimated'] = str(total_estimated)
				tem_obj['total_pending'] = str(
					Decimal(tem_obj['total_programmed']) - Decimal(tem_obj['total_estimated']))

				global_total_estimated = global_total_estimated + total_estimated

				if str(line_item.key) not in line_item_general_estimated.keys():
					line_item_general_estimated[str(line_item.key)] = 0
					line_item_general_estimated[str(line_item.key)] = line_item_general_estimated[
																		  str(line_item.key)] + total_estimated
			else:
				tem_obj['total_estimated'] = '0.00'
				tem_obj['total_pending'] = tem_obj['total_programmed']

			response.append(tem_obj)

		for element in response:
			temp_parent_key = element['parent_key']
			temp_current_key = element['key']

			if temp_parent_key == '':
				element['greatest_parent'] = ''
			else:
				while temp_parent_key != "":
					temp_current_key = temp_parent_key
					temp_parent_key = parent_keys[temp_parent_key]
				element['greatest_parent'] = temp_current_key

		for element in response:
			key = element['key']
			if parent_keys[key] == '':
				general_programmed_sum = 0
				general_estimated_sum = 0
				for element2 in response:
					parent_key = element2['greatest_parent']
					current_key = element2['key']
					if parent_key == key and current_key in line_item_general_programmed.keys():
						general_programmed_sum = general_programmed_sum + line_item_general_programmed[str(current_key)]

					if parent_key == key and current_key in line_item_general_estimated.keys():
						general_estimated_sum = general_estimated_sum + line_item_general_estimated[str(current_key)]

				element['general_programmed_sum'] = str(general_programmed_sum)
				element['general_estimated_sum'] = str(general_estimated_sum)
				element['general_pending_sum'] = str(general_programmed_sum - general_estimated_sum)

				sub_line_items = []

				for record in response:
					if record['greatest_parent'] == element['key']:
						sub_line_items.append(record)

				element['sub_line_items'] = sub_line_items

				structured_line_items.append(element)

			structured_response['line_items'] = structured_line_items
			structured_response['global_total_programmed'] = str(global_total_programmed)
			structured_response['global_total_estimated'] = str(global_total_estimated)
			structured_response['global_total_pending'] = str(global_total_programmed - global_total_estimated)

		# return HttpResponse(
		#    Utilities.json_to_dumps(structured_response), 'application/json; charset=utf-8')
		return structured_response


class PhysicalFinancialAdvanceReport(View):
	@staticmethod
	def get_report(project_id, type='C'):
		structured_response = {}

		structured_response[
			'physical_financial_advance'] = PhysicalFinancialAdvanceReport.get_physical_financial_advance(project_id,
																										  type)
		structured_response['biddings_programs'] = PhysicalFinancialAdvanceReport.get_biddings_report(project_id, type)

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

		payment_schedule_grouped = schedule_years.values('project_id').annotate(Count('project_id'), total=Sum('amount'))

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
				progress_estimate_set = ProgressEstimate.objects.filter(Q(estimate__concept_input__line_item__project=project_id)
											   & Q(estimate__start_date__month=record.month)
											   & Q(estimate__start_date__year=temp_year))\
					.values('estimate__concept_input__line_item__project__id')\
					.annotate(Count('estimate__concept_input__line_item__project__id'), total = Sum('amount'))

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
					"month_program": round(record.amount, 2),
					"month_paid_estimate": month_paid_estimate,
				})


			response.append(yearly_json)


		return response
