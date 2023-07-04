import datetime
import json

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, '__str__'):  # This will handle ObjectIds
            return str(obj)

        return super(JsonEncoder, self).default(obj)