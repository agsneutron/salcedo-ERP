import json
from django.utils.safestring import mark_safe

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
