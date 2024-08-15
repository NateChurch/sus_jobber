from datetime import date, datetime
import uuid


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, bytearray):
        return obj.hex()

    if isinstance(obj, uuid.UUID):
        return str(obj)

    return obj.__dict__



