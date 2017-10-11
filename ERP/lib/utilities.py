# coding=utf-8
import json
import copy

from decimal import Decimal
from datetime import date
from django.utils.safestring import mark_safe


class Utilities():
    @staticmethod
    def query_set_to_json_string(query_set):
        return mark_safe(json.dumps(map(lambda query_set: query_set.to_serializable_dict(), query_set),
                                    ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ))

    @staticmethod
    def query_set_to_json(query_set):
        return json.loads(json.dumps(map(lambda query_set: query_set.to_serializable_dict(), query_set),
                                     ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True, ))

    @staticmethod
    def json_to_safe_string(the_json):
        return mark_safe(json.dumps(the_json))

    # Toma un queryset, lo vuelve serializable y lo serializa para poder devolverlo al cliente.
    @staticmethod
    def query_set_to_dumps(query_set_object):
        return json.dumps(map(lambda model_object: model_object.to_serializable_dict(), query_set_object),
                          indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False
                          )

    # Toma un objeto tipo json, y lo serializa para poder mandarlo al cliente.
    @staticmethod
    def json_to_dumps(json_object):
        return json.dumps(json_object, indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False)

    # Transforma un queryset a un objeto tipo JSON.
    @staticmethod
    def query_set_to_dictionary(query_set_object):
        return map(lambda model_object: model_object.to_serializable_dict(), query_set_object)

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

    @staticmethod
    def clean_generic_queryset_from_nones(query_set_object):
        """
        Cleans a QuerySet object, converting it's decimal properties to strings.
        :param query_set_object: object to clean
        :return: the QuerySet object with the decimal attributes converted to strings
        """
        response = []
        for obj_attr in query_set_object.keys():
            if query_set_object[obj_attr] is None:
                query_set_object[obj_attr] = 'None'
        response.append(query_set_object)
        return response

    @staticmethod
    def remove_empty_values_keys_from_object(object):

        object_as_dict = copy.deepcopy(object).__dict__
        keys_to_remove = []
        for key in object_as_dict:
            if object_as_dict[str(key)] is None:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            object_as_dict.pop(key)

        return object_as_dict


    @staticmethod
    def number_to_currency(number):
        if number >= 0:
            return '${:,.2f}'.format(number)
        else:
            return '-${:,.2f}'.format(-number)
