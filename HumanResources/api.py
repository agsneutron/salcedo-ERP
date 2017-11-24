from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from ERP.lib.utilities import Utilities
from HumanResources.models import EmployeeAssistance


class ChangeAbsenceJustifiedStatus(View):
    def post(self, request):

        employee_assitance_id = request.POST.get('employee_assistance')
        new_status = request.POST.get('status')

        employee_assistance = EmployeeAssistance.objects.get(pk=employee_assitance_id)

        employee_assistance.justified = new_status
        employee_assistance.save()

        redirect_url = request.POST.get('redirect_url')

        return HttpResponseRedirect(redirect_url)