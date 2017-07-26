import json
from django.utils.safestring import mark_safe

class Utilities():

    @staticmethod
    def query_set_to_json(query_set):
        return mark_safe(json.dumps(map(lambda query_set: query_set.to_serializable_dict(), query_set),
                           ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True,))