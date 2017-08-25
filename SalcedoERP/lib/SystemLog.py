import logging
from django.contrib.admin.models import LogEntry

from ERP.lib.utilities import Utilities
from ERP.models import SystemLogEntry


class LoggingConstants:
    def __init__(self):
        pass

    DATA_UPLOAD = 'erp.dataupload'

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    TYPE_OFFSET = 1000

    PRIORITIES = {
        logging.DEBUG: "Debug",
        logging.INFO: "Info",
        logging.WARNING: "Warning",
        logging.ERROR: "Error",
        logging.CRITICAL: "Critical",
    }


class SystemException(Exception):
    def __init__(self, message, type, priority, user_id):
        self.logger = logging.getLogger(type)
        self.type = type
        self.priority = priority
        self.message = message
        self.user_id = user_id


        print 'Por procesar error con mensaje: '+message


        self.process_exception()
        Exception.__init__(self, self.message)

    def process_exception(self):
        print 'Exception of type ' + self.type + ' and priority ' + LoggingConstants.PRIORITIES[self.priority]
        print 'Guardando error.'
        obj = SystemLogEntry(
            label=self.type,
            information=Utilities.json_to_safe_string(self.get_information()),
            priority=self.priority,
            user_id=self.user_id)
        print obj
        obj.save()
        print 'Error guardado.'

    def get_information(self):
        information = {
            "message": self.message
        }
        return information

    def save(self):
        self.process_exception()


class SystemLog(object):
    pass