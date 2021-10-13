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

from published_apis.models.extra_models import TokenModel  # noqa: F401
from published_apis.models.problem_details import ProblemDetails
from published_apis.models.service_api_description import ServiceAPIDescription


router = APIRouter()


@router.get(
    "/{apfId}/service-apis",
    responses={
        200: {"model": ServiceAPIDescription, "description": "Definition of all service API(s) published by the API publishing function."},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        406: {"model": ProblemDetails, "description": "Not Acceptable"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def apf_id_service_apis_get(
    apfId: str = Path(None, description=""),
) -> ServiceAPIDescription:
    """Retrieve all published APIs."""
    ...


@router.post(
    "/{apfId}/service-apis",
    responses={
        201: {"model": ServiceAPIDescription, "description": "Service API published successfully The URI of the created resource shall be returned in the \&quot;Location\&quot; HTTP header."},
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
async def apf_id_service_apis_post(
    apfId: str = Path(None, description=""),
    service_api_description: ServiceAPIDescription = Body(None, description=""),
) -> ServiceAPIDescription:
    """Publish a new API."""
    ...


@router.delete(
    "/{apfId}/service-apis/{serviceApiId}",
    responses={
        204: {"description": "The individual published service API matching the serviceAPiId is deleted."},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def apf_id_service_apis_service_api_id_delete(
    serviceApiId: str = Path(None, description=""),
    apfId: str = Path(None, description=""),
) -> None:
    """Unpublish a published service API."""
    ...


@router.get(
    "/{apfId}/service-apis/{serviceApiId}",
    responses={
        200: {"model": ServiceAPIDescription, "description": "Definition of all service API published by the API publishing function."},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        406: {"model": ProblemDetails, "description": "Not Acceptable"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def apf_id_service_apis_service_api_id_get(
    serviceApiId: str = Path(None, description=""),
    apfId: str = Path(None, description=""),
) -> ServiceAPIDescription:
    """Retrieve a published service API."""
    ...


@router.put(
    "/{apfId}/service-apis/{serviceApiId}",
    responses={
        200: {"model": ServiceAPIDescription, "description": "Definition of service API updated successfully."},
        204: {"description": "No Content"},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
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
async def apf_id_service_apis_service_api_id_put(
    serviceApiId: str = Path(None, description=""),
    apfId: str = Path(None, description=""),
    service_api_description: ServiceAPIDescription = Body(None, description=""),
) -> ServiceAPIDescription:
    """Update a published service API."""
    ...
