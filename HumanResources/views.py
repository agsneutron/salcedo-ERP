# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports.
import operator

import django

from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView
from django.db.models import Q

# Model Imports.
from HumanResources.models import *
from Accounting.models import *
from django.template import Context

# Create your views here.
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader

from HumanResources.api import PayrollUtilities


def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))

def employeehome(request):
    return render(request, 'admin/HumanResources/employee-home.html')

def employeerequisitionhome(request):
    return render(request, 'admin/HumanResources/employeerequisition-home.html')

def payrollhome(request):
    return render(request, 'admin/HumanResources/payroll-home.html')

def payrolltype(request):
    return render(request, 'admin/HumanResources/employee_payrolltype.html')


class JobInstanceListView(generic.ListView):
    model = JobInstance
    template_name = "HumanResources/job-instance-list.html"

    def get_context_data(self, **kwargs):
        context = super(JobInstanceListView, self).get_context_data(**kwargs)

        elements = context['object_list']

        first_node = JobInstance.objects.get(pk=1)

        first_node.children = self.get_children(first_node)

        context['chart'] = self.get_chart(first_node)

        print '----'
        print context['chart']

        return context

    def get_children(self, node):
        children = JobInstance.objects.filter(parent_job_instance_id=node.id)
        for child in children:
            child.children = self.get_children(child)

        return children

    def get_chart(self, first_node):
        html = '<ul id="org" style="display:none">'

        html += '<li>'

        html += self.get_chart_node_content(first_node)

        html += self.get_sub_chart(first_node.children)

        html += '</li>'
        html += '</ul>'

        return html

    def get_sub_chart(self, children):
        html = ''
        if children is not None and len(children) > 0:
            html += '<ul>'

        for child in children:
            style = ''
            if child.employee is None:
                style = 'uncovered'
            html += '<li class="' + style + '">' + self.get_chart_node_content(child)
            html += self.get_sub_chart(child.children)
            html += '</li>'

        if children is not None and len(children) > 0:
            html += '</ul>'

        return html

    def get_employee_photo(self, employee):
        if employee is not None and employee.photo is not None and str(employee.photo) != "":
            return '/media/' + str(employee.photo)
        return "/media/assets/avatar.jpg"

    def get_chart_node_content(self, job_instance):
        html = ""
        employee = job_instance.employee

        html += "<div class='overlay'>"

        if job_instance.employee is not None:
            html += "   <a href='/admin/HumanResources/employee/" + str(
                job_instance.employee_id) + "' class='node-button'><i class='fa fa-user'></i></a>"

        html += "   <a target='_blank' href='/admin/HumanResources/jobinstance/" + str(
            job_instance.id) + "/change/' class='node-button'><i class='fa fa-edit'></i></a>" \
                               "   <a href='#' class='node-button node-button-collapse' data-expanded='true'><i class='fa fa-arrow-circle-up'></i></a>" \
                               "   <a href='/admin/HumanResources/jobinstance/add/?parent_job_instance=" + str(
            job_instance.id) + "' class='node-button' data-expanded='true'><i class='fa fa-plus-circle'></i></a>" \
                               "" \
                               "</div>"

        html += "<div class='profile-photo' style=\"background-image:url('" + self.get_employee_photo(
            employee) + "');\"></div>"

        html += "<div>"

        if employee is not None:
            html += "<div>" + employee.get_full_name() + "</div>"
        else:
            html += "<div>Sin Cubrir</div>"

        html += "<div class='position-name'>" + job_instance.job_profile.job + " <br> " + job_instance.job_profile.area.name + "</div>"

        html += "</div>"

        return html


class EmployeeContractDetail(generic.DetailView):
    model = EmployeeContract
    template_name = "HumanResources/employee-contract-detail.html"


# class EmployeeFinancialDataview(generic.DetailView):
#     model = EmployeeFinancialData
#     template_name = "HumanResources/employee-detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(EmployeeFinancialDataview, self).get_context_data(**kwargs)
#
#         employeefinancialdata = context['employeefinancialdata']
#
#         infonavit_credit_number =InfonavitData.objects.filter(employee_financial_data_id=employeefinancialdata.id)
#         context['Numero_credito'] = infonavit_credit_number


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = "HumanResources/employee-detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)

        # The employee object.
        employee = context['employee']
        #employeefinancialdata = context['employeefinancialdata']

        # Obtaining the test applications of the employee and setting them to the context.
        test_applications = TestApplication.objects.filter(employee__id=employee.id)
        context['test_applications'] = test_applications

        # Obtaining the education info of the employee and setting it to the context.
        context['education'] = Education.objects.filter(employee__id=employee.id)

        # Obtaining the current education info of the employee and setting it to the context.
        current_education_array = []
        current_education_set = CurrentEducation.objects.filter(employee__id=employee.id)
        for record in current_education_set:
            record_json = {
                'type': record.get_type_display(),
                'name': record.name,
                'institution': record.institution,
                'sunday': record.sunday,
                'monday': record.monday,
                'tuesday': record.tuesday,
                'wednesday': record.wednesday,
                'thursday': record.thursday,
                'friday': record.friday,
                'saturday': record.saturday,
                'documents': []
            }

            # Obtaining the documents for the current education record.
            document_set = CurrentEducationDocument.objects.filter(current_education__id=record.id)
            for document in document_set:
                record_json['documents'].append(document)

            current_education_array.append(record_json)

        context['current_education'] = current_education_array

        # Obtaining the emergency contact info of the employee and setting it to the context.
        context['emergency_contacts'] = EmergencyContact.objects.filter(employee__id=employee.id)

        # Obtaining the family member info of the employee and setting it to the context.
        context['family_members'] = FamilyMember.objects.filter(employee__id=employee.id)

        # Obtaining the work references info of the employee and setting it to the context.
        context['work_references'] = WorkReference.objects.filter(employee__id=employee.id)

        # Obtaining the employee's documents and setting them to the context.
        context['employee_documents'] = EmployeeDocument.objects.filter(employee__id=employee.id)

        # Obtaining the employee's checker info and setting it to the context.
        checker_data = CheckerData.objects.filter(employee__id=employee.id)

        if (len(checker_data) > 0):
            context['checker_data'] = checker_data[0]

        # Obtaining the employee's position description and setting it to the context.
        context['employee_position_description'] = EmployeePositionDescription.objects.filter(employee__id=employee.id)

        employee_financial_data_id = EmployeeFinancialData.objects.values('id').filter(employee__id=employee.id)
        # Obtaining the employee's Employee Financial Data and setting it to the context.
        context['employee_financial_data'] = EmployeeFinancialData.objects.filter(employee__id=employee.id)

        #Infonavit
        Infonavit_array = []
        Infonavit_set = InfonavitData.objects.filter(employee_financial_data_id=employee_financial_data_id)
        for infonavit in Infonavit_set:
            infonavit_json = {
            'credit_number': infonavit.infonavit_credit_number,
            'discount_type': infonavit.discount_type,
            'discount_amount': infonavit.discount_amount,
            'start_date': infonavit.start_date,
            'credit_term': infonavit.credit_term,
            'comments': infonavit.comments,
             }
            Infonavit_array.append(infonavit_json)

        context['employee_infonavit'] = Infonavit_array

        # Obtaining the employee's Employee Has TAG Data and setting it to the context.
        context['employee_has_tag'] = EmployeeHasTag.objects.filter(employee__id=employee.id)

        # Obtaining the employee's Employee EmployeeEarningsDeductions Data and setting it to the context.
        context['employee_ed'] = EmployeeEarningsDeductions.objects.filter(employee__id=employee.id)

        return context


'''@login_required()
def EmployeeByPeriod(request):
    model = EmployeePositionDescription
    template_name = "admin/HumanResources/employee_by_payroll.html"

    context = Context({"my_name": "Dolores"})
    template = loader.get_template('admin/HumanResources/employee_by_payroll.html')
    payrollgroup = request.GET.get('payrollgroup')
    employees = EmployeePositionDescription.objects.values('employee__id').filter(payroll_group__id=payrollgroup)
    return HttpResponse(template.render(context))'''


@login_required()
def Tests(request):
    template = loader.get_template('HumanResources/testapplication_list.html')

    test_applications = TestApplication.objects.all()

    # context = RequestContext.request
    context = {'object_list': test_applications}
    return HttpResponse(template.render(context, request))


@login_required()
def TestApplicationDetail(request, pk):
    template = loader.get_template('HumanResources/testapplication_detail.html')

    object = TestApplication.objects.get(pk=pk)

    context = {'object': object}

    return HttpResponse(template.render(context, request))


@login_required()
def EmployeeByPeriod(request):
    payrollperiod = request.GET.get('payrollperiod')
    payrollgroup = PayrollPeriod.objects.get(pk=payrollperiod).payroll_group_id

    # Check if the payroll has been processed.
    payroll_receipt_processed = PayrollReceiptProcessed.objects.filter(payroll_period__id=payrollperiod)

    # The payroll has already been processed. Show the processed payroll.
    if len(payroll_receipt_processed) > 0:
        return HttpResponseRedirect("/admin/HumanResources/payrollreceiptprocessed/receipts_by_period/"+payrollperiod)


    template = loader.get_template('admin/HumanResources/employee_by_payroll.html')
    employees = EmployeePositionDescription.objects.filter(payroll_group__id=payrollgroup)
    period_data = PayrollPeriod.objects.filter(id=payrollperiod)


    # Payroll information by employee to know base salary and final salary.
    employee_data_set = []
    for record in employees:
        try:
            employee_payroll = PayrollUtilities.generate_single_payroll(record.employee, period_data.first())

        except EmployeeFinancialData.DoesNotExist as e:
            print "Exception was: " + str(e)
            django.contrib.messages.error(request, "No existen datos financieros para el empleado: " + record.employee.employee_key +
                                          " - "+record.employee.get_full_name()+".")
            return HttpResponseRedirect("/admin/HumanResources/payrollperiod/")



        employee_data_set.append({
            "employee_position_description.id": record.id,
            "employee_id": record.employee.id,
            "employee_key" : record.employee.employee_key,
            "employee_fullname" : record.employee.get_full_name(),
            "employee_job" : record.job_profile.job,
            "employee_payroll" : employee_payroll
        })

        print PayrollUtilities.generate_single_payroll(record.employee, period_data.first())

    # context = RequestContext.request
    context = {'employees_data_set': employee_data_set,
               'payrollperiod': payrollperiod,
               'payrolldata': period_data}
    return HttpResponse(template.render(context, request))


@login_required()
def payrollhome(request):
    template = loader.get_template('admin/HumanResources/payroll-home.html')
    period_data = PayrollPeriod.objects.all().query
    employees = EmployeePositionDescription.objects.all()
    employees.group_by = ['payroll_group_id']
    period_data
    # context = RequestContext.request
    context = {'employees': employees,
               'payrolldata': period_data}
    return HttpResponse(template.render(context, request))


class PayrollPeriodListView(generic.ListView):
    model = PayrollPeriod
    template_name = "HumanResources/payroll-period-list.html"

    def get_queryset(self):
        result = super(PayrollPeriodListView, self).get_queryset()

        payroll_group_id = self.kwargs['pk']

        result = result.filter(payroll_group_id=payroll_group_id)

        return result

    def get_context_data(self, **kwargs):
        context = super(PayrollPeriodListView, self).get_context_data(**kwargs)

        payroll_group_id = self.kwargs['pk']
        payroll_group = PayrollGroup.objects.get(pk=payroll_group_id)

        context['payrollgroup'] = payroll_group

        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(PayrollPeriodListView, self).dispatch(request, args, kwargs)


class PayrollPeriodDetail(generic.ListView):
    model = Employee
    template_name = "HumanResources/payroll-period-detail.html"

    def get_queryset(self):
        result = super(PayrollPeriodDetail, self).get_queryset()

        payroll_period_id = self.kwargs['pk']

        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payroll_group_id = payroll_period.payroll_group_id

        employees = EmployeePositionDescription.objects.filter(payroll_group_id=payroll_group_id).values('employee')
        employee_ids = []

        for employee in employees:
            employee_ids.append(employee['employee'])

        result = result.filter(id__in=employee_ids)

        return result

    def get_context_data(self, **kwargs):
        context = super(PayrollPeriodDetail, self).get_context_data(**kwargs)

        payroll_period_id = self.kwargs['pk']

        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payroll_group_id = payroll_period.payroll_group_id

        payroll_group = PayrollGroup.objects.get(pk=payroll_group_id)

        context['payrollgroup'] = payroll_group
        context['payrollperiod'] = payroll_period

        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(PayrollPeriodDetail, self).dispatch(request, args, kwargs)


class PayrollPeriodEmployeeDetail(generic.DetailView):
    model = Employee
    template_name = "HumanResources/payroll-period-employee-detail.html"

    def get_queryset(self):
        result = super(PayrollPeriodEmployeeDetail, self).get_queryset()

        employee_id = self.kwargs['pk']

        return result

    def get_context_data(self, **kwargs):
        context = super(PayrollPeriodEmployeeDetail, self).get_context_data(**kwargs)

        employee_id = self.kwargs['pk']

        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(PayrollPeriodEmployeeDetail, self).dispatch(request, args, kwargs)



class EmployeeRequisitionDetailView(generic.DetailView):
    model = EmployeeRequisition
    template_name = "HumanResources/employee-requisition-detail.html"

    def get_queryset(self):
        result = super(EmployeeRequisitionDetailView, self).get_queryset()

        return result

    def get_context_data(self, **kwargs):
        context = super(EmployeeRequisitionDetailView, self).get_context_data(**kwargs)

        employee_id = self.kwargs['pk']

        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(EmployeeRequisitionDetailView, self).dispatch(request, args, kwargs)

class PayrollTypeDetailView(generic.DetailView):
    model = PayrollType
    template_name = "HumanResources/payroll-type-detail.html"

    def get_queryset(self):
        result = super(PayrollTypeDetailView, self).get_queryset()

        return result

    def get_context_data(self, **kwargs):
        context = super(PayrollTypeDetailView, self).get_context_data(**kwargs)

        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(PayrollTypeDetailView, self).dispatch(request, args, kwargs)





class EmployeeDropOutDetail(generic.DetailView):
    model = EmployeeDropOut
    template_name = "HumanResources/employee-dropout-detail.html"

    def get_queryset(self):
        result = super(EmployeeDropOutDetail, self).get_queryset()

        return result

    def get_context_data(self, **kwargs):
        context = super(EmployeeDropOutDetail, self).get_context_data(**kwargs)


        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(EmployeeDropOutDetail, self).dispatch(request, args, kwargs)


class EmployeeLoanDetail(generic.DetailView):
    model = EmployeeLoan
    template_name = "HumanResources/employee-loan-detail.html"

    def get_queryset(self):
        result = super(EmployeeLoanDetail, self).get_queryset()

        return result

    def get_context_data(self, **kwargs):
        context = super(EmployeeLoanDetail, self).get_context_data(**kwargs)


        return context

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.has_perm('ERP.view_list_empresa'):
        #     raise PermissionDenied
        return super(EmployeeLoanDetail, self).dispatch(request, args, kwargs)



class IncidencesByPayrollPeriod(ListView):
    model = EmployeeAssistance
    template_name = "HumanResources/inicidences-by-payroll-period.html"

    def get_context_data(self, **kwargs):
        context = super(IncidencesByPayrollPeriod, self).get_context_data(**kwargs)

        payroll_period_id = self.kwargs['payroll_period_id']
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        incidences = EmployeeAssistance.objects.filter(Q(absence=True) & Q(payroll_period=payroll_period)) \
            .values('employee__id', 'employee__employee_key', 'employee__name', 'employee__first_last_name',
                    'employee__second_last_name') \
            .annotate(Count('employee__id'))

        context['payroll_period'] = payroll_period
        context['incidences'] = incidences

        print incidences

        return context


class IncidencesByEmployee(ListView):
    model = EmployeeAssistance
    template_name = "HumanResources/inicidences-by-employee.html"

    def get_context_data(self, **kwargs):
        context = super(IncidencesByEmployee, self).get_context_data(**kwargs)

        employee_key = self.kwargs['employee_key']
        payroll_period_id = self.kwargs['payroll_period_id']

        print "Got: "
        print str(employee_key)
        print str(payroll_period_id)


        employee = Employee.objects.get(employee_key=employee_key)
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        print "Objects"
        print employee
        print payroll_period

        incidences = EmployeeAssistance.objects.filter(
            Q(employee_id=employee.id) & Q(payroll_period_id=payroll_period.id) &Q(absence=True))

        print "Length"
        print len(incidences)

        absence_proofs = AbsenceProof.objects.filter(
            Q(employee_id=employee.id) & Q(payroll_period_id=payroll_period.id))

        context['employee'] = employee
        context['payroll_period'] = payroll_period
        context['incidences'] = incidences
        context['absence_proofs'] = absence_proofs

        return context



# Views for the model Payroll Receipt Processed.
class PayrollReceiptProcessedListView(ListView):
    model = PayrollReceiptProcessed
    template_name = "HumanResources/payroll_receipt-processed-list.html"


    def get_context_data(self, **kwargs):
        context = super(PayrollReceiptProcessedListView, self).get_context_data(**kwargs)

        payroll_period_id = self.kwargs['payroll_period_id']
        payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payroll_receipts_processed = PayrollReceiptProcessed.objects.filter(payroll_period_id=payroll_period_id)


        context['receipts'] = payroll_receipts_processed
        context['payroll_period'] = payroll_period

        return context


class EarningsDeductionsListView(ListView):
    model = EarningsDeductions
    template_name = "HumanResources/penalties-list.html"
    query = None

    """
       Display a Blog List page filtered by the search query.
    """
    paginate_by = 10
    title_list = 'Incidencias'
    penalty = ''

    def get_queryset(self):
        result = super(EarningsDeductionsListView, self).get_queryset()

        query = self.request.GET.get('q')
        query_penalty = self.request.GET.get('penalty')
        if query_penalty:
            EarningsDeductionsListView.title_list = 'Incidencias'
            EarningsDeductionsListView.penalty = '?tipo=2'
            EarningsDeductionsListView.query = query_penalty
            query_list = query_penalty.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(penalty__icontains=q) for q in query_list))
                #|
                #reduce(operator.and_,
                #       (Q(account____icontains=q) for q in query_list))
            )
        else:
            EarningsDeductionsListView.title_list='Percepciones y Deducciones'
            EarningsDeductionsListView.penalty = ''
            EarningsDeductionsListView.query = ''
            query_list = ['N']
            result = result.filter(
                reduce(operator.and_,
                       (Q(penalty__icontains=q) for q in query_list)))

        return result

    def get_context_data(self, **kwargs):
        context = super(EarningsDeductionsListView, self).get_context_data(**kwargs)
        context['title_list'] = EarningsDeductionsListView.title_list
        context['penalty'] = EarningsDeductionsListView.penalty
        context['query'] = EarningsDeductionsListView.query
        context['query_string'] = '&q=' + EarningsDeductionsListView.query
        context['has_query'] = (EarningsDeductionsListView.query is not None) and (EarningsDeductionsListView.query != "")
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('ERP.view_list_empresa'):
            raise PermissionDenied
        return super(EarningsDeductionsListView, self).dispatch(request, args, kwargs)


# For  Transactions by account filter objects view
def SearchTransactions(request):
    template = loader.get_template('HumanResources/search_transactions.html')
    context = {
               'internalcompany': InternalCompany.objects.all(), }

    return HttpResponse(template.render(context, request))


# Views for the model AccessToProjectAdmin.
class AccessToDirectionAdminListView(ListView):

    model = AccessToDirection
    template_name = "HumanResources/accesstodirection-list.html"
    query = None
    title_list = "Acceso a Dirección"
    """
       Display a Project List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):

        result = super(AccessToDirectionAdminListView, self).get_queryset()
        user = int(self.request.GET.get('user'))

        query = Q()
        query = query & Q(user_id=int(user))
        result = result.filter(query)

        query = self.request.GET.get('q')
        if query:
            AccessToDirectionAdminListView.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(direction__name__icontains=q) for q in query_list))
            )
        else:
            AccessToDirectionAdminListView.query = ''

        return result

    def get_context_data(self, **kwargs):
        context = super(AccessToDirectionAdminListView, self).get_context_data(**kwargs)
        context['title_list'] = AccessToDirectionAdminListView.title_list
        context['query'] = AccessToDirectionAdminListView.query
        context['query_string'] = '&q=' + AccessToDirectionAdminListView.query
        context['has_query'] = (AccessToDirectionAdminListView.query is not None) and (
                AccessToDirectionAdminListView.query != "")

        context['user_id'] = self.request.GET.get('user')

        return context
