import logging


class LoggingConstants:
    def __init__(self):
        pass

    DATA_UPLOAD = 'erp.dataupload'

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    PRIORITIES = {
        logging.DEBUG: "Debug",
        logging.INFO: "Info",
        logging.WARNING: "Warning",
        logging.ERROR: "Error",
        logging.CRITICAL: "Critical",
    }


class SystemException(Exception):
    def __init__(self, message, type, priority):
        self.logger = logging.getLogger(type)
        self.type = type
        self.priority = priority
        self.process_exception()

        Exception.__init__(self, message)

    def process_exception(self):
        print 'Exception of type ' + self.type + ' and priority ' + LoggingConstants.PRIORITIES[self.priority]
        pass


class SystemLog(object):
    pass
