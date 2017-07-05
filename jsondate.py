import datetime
import json

DATE_FMT = '%Y-%m-%d'
ISO8601_FMT = '%Y-%m-%dT%H:%M:%SZ'
__version__ = "0.2"

def _datetime_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime(ISO8601_FMT)
    elif isinstance(obj, datetime.date):
        return obj.strftime(DATE_FMT)

    raise TypeError


def _datetime_decoder(dict_):
    for key, value in dict_.iteritems():
        # The built-in `json` library will `unicode` strings, except for empty
        # strings which are of type `str`. `jsondate` patches this for
        # consistency so that `unicode` is always returned.
        if isinstance(value, str):
            if value == '':
                dict_[key] = u''
                continue

            if len(value) == len("yyyy-mm-ddThh:mm:ssz"):
                try:
                    datetime_obj = datetime.datetime.strptime(value, ISO8601_FMT)
                    dict_[key] = datetime_obj
                except (ValueError, TypeError):
                    continue
            elif len(value) == len("yyyy-mm-dd"):
                try:
                    date_obj = datetime.datetime.strptime(value, DATE_FMT)
                    dict_[key] = date_obj.date()
                except (ValueError, TypeError):
                    continue
    return dict_


def dumps(*args, **kwargs):
    kwargs['default'] = _datetime_encoder
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs['default'] = _datetime_encoder
    return json.dump(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs['object_hook'] = _datetime_decoder
    return json.loads(*args, **kwargs)


def load(*args, **kwargs):
    kwargs['object_hook'] = _datetime_decoder
    return json.load(*args, **kwargs)