from SalcedoERP.lib.SystemLog import SystemException, LoggingConstants


class OperationLogicError(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.DATA_UPLOAD, priority, user_id)
