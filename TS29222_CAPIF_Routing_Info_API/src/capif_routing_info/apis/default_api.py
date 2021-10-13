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

from capif_routing_info.models.extra_models import TokenModel  # noqa: F401
from capif_routing_info.models.problem_details import ProblemDetails
from capif_routing_info.models.routing_info import RoutingInfo


router = APIRouter()


@router.get(
    "/service-apis/{serviceApiId}",
    responses={
        200: {"model": RoutingInfo, "description": "OK."},
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
async def service_apis_service_api_id_get(
    serviceApiId: str = Path(None, description="Identifier of a published service API"),
    aef_id: str = Query(None, description="Identifier of the AEF"),
    supp_feat: str = Query(None, description="To filter irrelevant responses related to unsupported features", regex=r"^[A-Fa-f0-9]*$"),
) -> RoutingInfo:
    """Retrieves the API routing information."""
    ...
