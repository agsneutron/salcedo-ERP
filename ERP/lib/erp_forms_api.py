# coding=utf-8
from django.http import HttpResponse, HttpResponseServerError
from django.views.generic.list import ListView
import json
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage, Storage

# Custom classes
from ERP.lib.utilities import Utilities
from ERP.models import ProgressEstimateLog, ERPUser

# Model imports.
from ERP.models import *

class SaveProgressEstimateLogFormEndpoint(ListView):
    ''' Endpoint to save a new log record
    '''
    def post(self, request, *args, **kwargs):
        # Obtaining the logged user.

        progress_estimate = ProgressEstimate.objects.all().first()

        try:
            user = ERPUser.objects.get(pk=request.user.erpuser.id)
        except ERPUser.DoesNotExist:
            return HttpResponseServerError("User does not exist")


        description = request.POST.get('description')
        date_as_string = request.POST.get('date')
        try:
            date = datetime.strptime(date_as_string, '%d/%m/%Y')
        except ValueError as e:
            return HttpResponseServerError("The given format for the date is incorrect")



        pel_obj = ProgressEstimateLog()
        pel_obj.progress_estimate = progress_estimate
        pel_obj.user = user
        pel_obj.description = description
        pel_obj.date = date

        try:
            pel_obj.save()
        except ValidationError as e:
            return HttpResponseServerError("There was an error validating the progress estimate log")

        print "The object"
        print pel_obj


        return HttpResponse(json.dumps({'response':'ok', 'saved_log':pel_obj.to_serializable_dict()}), 'application/json',)


class SaveProgressEstimateLogFileFormEndpoint(ListView):
    ''' Endpoint to save a new log file record
    '''
    def post(self, request, *args, **kwargs):

        pel = ProgressEstimateLog.objects.get(pk=request.POST.get('id_progress_estimate_log'))
        mime = request.POST.get('mime')


        project_key = pel.progress_estimate.estimate.concept_master.line_item.project.key


        the_file = request.FILES['file']
        fs = FileSystemStorage(location="ERP/media/documentosFuente/"+project_key)
        file_name = fs.save(the_file.name, the_file)


        file_log_obj = LogFile()
        file_log_obj.progress_estimate_log = pel
        file_log_obj.mime = mime
        file_log_obj.file = file_name
        file_log_obj.save()


        print "The file object"
        print file_log_obj.to_serializable_dict()



        return HttpResponse(json.dumps({'response': 'ok', 'file_obj':file_log_obj.to_serializable_dict()}),
                            'application/json', )