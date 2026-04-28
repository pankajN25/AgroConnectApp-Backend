import sys
import datetime
from six import string_types


def to_json(obj, id):
    cls = type(obj)
    d = dict((c, getattr(obj, c)) for c in vars(cls) if isinstance(getattr(cls, c), property))
    d["id"] = id
    return d


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def datetime_decoder(d):
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()
    result = []
    for k, v in pairs:
        if isinstance(v, string_types):
            try:
                v = datetime.datetime.strptime(v, '%d-%m-%Y %H:%M:%S')
            except ValueError:
                try:
                    v = datetime.datetime.strptime(v, '%d-%m-%Y %H:%M:%S').date()
                except ValueError:
                    pass
        elif isinstance(v, (dict, list)):
            v = datetime_decoder(v)
        result.append((k, v))
    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)


def log_exception(file_name, function_name, payload=None, exc=None, extra=None):
    try:
        exc_msg = str(exc) if exc else "No exception"
        print(f"[ERROR] {file_name}.{function_name}: {exc_msg}")
        if payload:
            print(f"[ERROR] Payload: {payload}")
    except Exception as e:
        print("Error in log_exception:", e)
