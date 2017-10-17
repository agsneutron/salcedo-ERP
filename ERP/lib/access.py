from ERP.models import *

class ERPAccess(object):
    @staticmethod
    def user_has_access(user_id, access_code):
        return True
