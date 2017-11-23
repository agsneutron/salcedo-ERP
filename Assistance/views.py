# coding=utf-8

from django.db import transaction
from django.http import HttpResponse
from django.views.generic.list import ListView

from helper import AssistanceFileInterface, AssistanceDBObject, ErrorDataUpload



def assistance_upload_test_view(request):

    payroll_period_id = int(request.GET.get('payroll_period'))

    # Creating an object to work with the specified excel document.
    # The file_path has been set for temporary testing.
    file_path = "/Users/oscarsanchez/Documents/Work/Salcedo/Fase_2/Archivos/test.xlsx"
    file_interface_obj = AssistanceFileInterface(file_path)

    # Getting the elements from the file.
    elements = file_interface_obj.get_element_list()

    # Getting the user that is processing the task.
    current_user = request.user


    # Processing the results.
    assitance_db_object = AssistanceDBObject(current_user,elements[1:], payroll_period_id)

    try:
        with transaction.atomic():
             assitance_db_object.process_records()

    except ErrorDataUpload as e:
        e.save()
        raise e




    return HttpResponse('Done')




