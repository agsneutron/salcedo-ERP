import json
from django.utils.safestring import mark_safe
from decimal import Decimal
from datetime import date

class Utilities():

    @staticmethod
    def query_set_to_json_string(query_set):
        return mark_safe(json.dumps(map(lambda query_set: query_set.to_serializable_dict(), query_set),
                           ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True,))

    @staticmethod
    def query_set_to_json(query_set):
        return json.loads(json.dumps(map(lambda query_set: query_set.to_serializable_dict(), query_set),
                           ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True,))

    @staticmethod
    def json_to_safe_string(the_json):
        return mark_safe(json.dumps(the_json))

    @staticmethod
    def clean_generic_queryset(query_set_object):
        """
        Cleans a QuerySet object, converting it's decimal properties to strings.
        :param query_set_object: object to clean
        :return: the QuerySet object with the decimal attributes converted to strings
        """
        response = []
        for obj in query_set_object:
            for obj_attr in obj.keys():
                if type(obj[obj_attr]) is Decimal or type(obj[obj_attr]) is date:
                    obj[obj_attr] = str(obj[obj_attr])
            response.append(obj)
        return response
