# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from api_invocation_logs.models.extra_models import TokenModel  # noqa: F401
from api_invocation_logs.models.invocation_log import InvocationLog
from api_invocation_logs.models.problem_details import ProblemDetails


router = APIRouter()


@router.post(
    "/{aefId}/logs",
    responses={
        201: {"model": InvocationLog, "description": "Log of service API invocations provided by API exposing function successfully stored on the CAPIF core function."},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        411: {"model": ProblemDetails, "description": "Length Required"},
        413: {"model": ProblemDetails, "description": "Payload Too Large"},
        415: {"model": ProblemDetails, "description": "Unsupported Media Type"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def aef_id_logs_post(
    aefId: str = Path(None, description="Identifier of the API exposing function"),
    invocation_log: InvocationLog = Body(None, description=""),
) -> InvocationLog:
    """Creates a new log entry for service API invocations."""
    ...
