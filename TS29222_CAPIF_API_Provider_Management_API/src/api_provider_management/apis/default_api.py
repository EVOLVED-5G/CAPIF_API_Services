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

from api_provider_management.models.extra_models import TokenModel  # noqa: F401
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails
from api_provider_management.models.problem_details import ProblemDetails


router = APIRouter()


@router.post(
    "/registrations",
    responses={
        201: {"model": APIProviderEnrolmentDetails, "description": "API provider domain registered successfully"},
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
async def registrations_post(
    api_provider_enrolment_details: APIProviderEnrolmentDetails = Body(None, description=""),
) -> APIProviderEnrolmentDetails:
    """Registers a new API Provider domain with API provider domain functions profiles."""
    ...


@router.delete(
    "/registrations/{registrationId}",
    responses={
        204: {"description": "The API provider domain matching registrationId is deleted."},
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
async def registrations_registration_id_delete(
    registrationId: str = Path(None, description="String identifying an registered API provider domain resource."),
) -> None:
    """Deregisters API provider domain by deleting API provider domain and functions."""
    ...


@router.put(
    "/registrations/{registrationId}",
    responses={
        200: {"model": APIProviderEnrolmentDetails, "description": "API provider domain registration details updated successfully."},
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
async def registrations_registration_id_put(
    registrationId: str = Path(None, description="String identifying an registered API provider domain resource."),
    api_provider_enrolment_details: APIProviderEnrolmentDetails = Body(None, description="Representation of the API provider domain registration details to be updated in CAPIF core function."),
) -> APIProviderEnrolmentDetails:
    """Updates an API provider domain&#39;s registration details."""
    ...
