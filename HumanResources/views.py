# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports.
from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView


# Model Imports.
from HumanResources.models import *

def employeedetail(request):
    return render(request, 'HumanResources/employee-detail.html')

def employeehome(request):
    return render(request, 'admin/HumanResources/employee-home.html')

class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = "HumanResources/employee-detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)

        # The employee object.
        employee = context['employee']

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
      #  context['employee_documents'] = EmployeeDocument.objects.filter(employee__id=employee.id)

        # Obtaining the employee's checker info and setting it to the context.
        context['checker_data'] = CheckerData.objects.get(employee__id=employee.id)


        return context