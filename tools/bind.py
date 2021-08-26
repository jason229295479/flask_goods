import logging

from flask import request

import enums


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
