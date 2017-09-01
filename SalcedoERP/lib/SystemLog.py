# coding=utf-8


import logging
from django.contrib.admin.models import LogEntry

from ERP.lib.utilities import Utilities
from ERP.models import SystemLogEntry

from django.utils.encoding import python_2_unicode_compatible


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


@python_2_unicode_compatible
class SystemException(Exception):
    def __str__(self):
        return self.message.encode('utf-8')

    def __unicode__(self):
        return self.message.encode('utf-8')

    def __init__(self, message, type, priority, user_id):
        self.logger = logging.getLogger(type)
        self.type = type
        self.priority = priority
        self.message = message.encode('utf-8')
        self.user_id = user_id

        self.process_exception()
        Exception.__init__(self, self.message.encode('utf-8'))

    def process_exception(self):
        obj = SystemLogEntry(
            label=self.type,
            information=Utilities.json_to_safe_string(self.get_information()),
            priority=self.priority,
            user_id=self.user_id)

        obj.save()

    def get_information(self):
        information = {
            "message": self.message.encode('utf-8')
        }
        return information

    def get_error_message(self):
        return self.message.encode('utf-8')

    def save(self):
        self.process_exception()


class SystemLog(object):
    pass