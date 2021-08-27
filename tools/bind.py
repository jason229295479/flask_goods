import logging

from flask import request

import enums

_sa_instance_state = '_sa_instance_state'


def bind_json(params):
    items = {}
    try:
        for k, v in request.json.items():
            if hasattr(params, k):
                v = type(getattr(params, k))(v)
                items[k] = v
                setattr(params, k, v)
        setattr(params, "json", items)
    except Exception as e:
        logging.error(e)
        return enums.param_err


def to_json(ormObject, needList: list = None, ignoreList: list = None) -> dict:
    items = ormObject.__dict__
    if _sa_instance_state in items:
        items.pop("_sa_instance_state")
    if needList:
        items = {k: v for k, v in items.items() if k in needList}
    elif ignoreList:
        for ignore in ignoreList:
            if ignore in items:
                items.pop(ignore)
    return items
