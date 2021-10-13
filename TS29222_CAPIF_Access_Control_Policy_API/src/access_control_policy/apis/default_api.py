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

from access_control_policy.models.extra_models import TokenModel  # noqa: F401
from access_control_policy.models.access_control_policy_list import AccessControlPolicyList
from access_control_policy.models.problem_details import ProblemDetails


router = APIRouter()


@router.get(
    "/accessControlPolicyList/{serviceApiId}",
    responses={
        200: {"model": AccessControlPolicyList, "description": "OK."},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        406: {"model": ProblemDetails, "description": "Not Acceptable"},
        414: {"model": ProblemDetails, "description": "URI Too Long"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def access_control_policy_list_service_api_id_get(
    serviceApiId: str = Path(None, description="Identifier of a published service API"),
    aef_id: str = Query(None, description="Identifier of the AEF"),
    api_invoker_id: str = Query(None, description="Identifier of the API invoker"),
    supported_features: str = Query(None, description="To filter irrelevant responses related to unsupported features", regex=r"^[A-Fa-f0-9]*$"),
) -> AccessControlPolicyList:
    """Retrieves the access control policy list."""
    ...
