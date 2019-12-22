import functools
import logging

from flask import request, jsonify
from flask_restful import reqparse, abort
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

logger = logging.getLogger(__name__)


def parse_request(*args, **kwargs):
    """
    Decorator used to parse request
    :param args: list of Arguments (flask_restful.reqparse.Argument)
    :param kwargs:
    :return:
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    for arg in args:
        parser.add_argument(arg)

    if kwargs.get('allow_ordering', None):
        parser_args = [p.name for p in parser.args]
        default_args = [
            reqparse.Argument("sort_by", type=str, store_missing=False),
            reqparse.Argument("order", type=str, store_missing=False, choices=('asc', 'desc')),
        ]
        for p in default_args:
            if p.name not in parser_args:
                parser.add_argument(p)

    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):
            fkwargs.update(parser.parse_args())
            return f(*fargs, **fkwargs)

        return inner

    return decorator

def parse_with(schema, arg_name='entity', **kwargs):
    """Decorator used to parse json input using the specified schema
    :param kwargs will be passed down to the dump method from marshmallow Schema
    :param arg_name will be inserted as a keyword argument containing the
        deserialized data.
    """

    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):
            json = request.get_json() or {}
            try:
                entity, errors = schema.load(json, **kwargs)
                fkwargs.update({arg_name: entity})

            except (ValidationError,ValueError, Exception) as e:
                logger.error("parse_with: {}".format(str(e)))
                abort(400)
                logger.error("parse_with: {}".format(str(e)))

            return f(*fargs, **fkwargs)

        return inner

    return decorator


def marshal_with(schema, many=False, success_code=200, **kwargs):
    """Decorator to serialize output using specified schema
    :param kwargs will be passed down to the dump method from marshmallow Schema
    """

    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):
            va = f(*fargs, **fkwargs)
            data = schema(many=many).dump(va)

            response = jsonify(data)
            response.status_code = success_code
            return response

        return inner

    return decorator

# def marshal_with(func):
#     @functools.wraps(func)
#     def wrapper_decorator(*args, **kwargs):
#         # Do something before
#         value = func(*args, **kwargs)
#         # Do something after
#         return value
#     return wrapper_decorator

