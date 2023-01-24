from ..models.problem_details import ProblemDetails
from ..encoder import JSONEncoder
from flask import Response
import json

mimetype = "application/json"


def make_response(object, status):
    res = Response(json.dumps(object, cls=JSONEncoder), status=status, mimetype=mimetype)

    return res


def internal_server_error(detail, cause):
    prob = ProblemDetails(title="Internal Server Error", status=500, detail=detail, cause=cause)

    return Response(json.dumps(prob, cls=JSONEncoder), status=500, mimetype=mimetype)


def forbidden_error(detail, cause):
    prob = ProblemDetails(title="Forbidden", status=403, detail=detail, cause=cause)

    return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=mimetype)


def bad_request_error(detail, cause, invalid_params):
    prob = ProblemDetails(title="Bad Request", status=400, detail=detail, cause=cause, invalid_params=invalid_params)

    return Response(json.dumps(prob, cls=JSONEncoder), status=400, mimetype=cause)


def not_found_error(detail, cause):
    prob = ProblemDetails(title="Not Found", status=404, detail=detail, cause=cause)

    return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=mimetype)