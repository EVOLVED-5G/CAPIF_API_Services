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

from api_invoker_management.models.extra_models import TokenModel  # noqa: F401
from api_invoker_management.models.api_invoker_enrolment_details import APIInvokerEnrolmentDetails
from api_invoker_management.models.problem_details import ProblemDetails


router = APIRouter()


@router.delete(
    "/onboardedInvokers/{onboardingId}",
    responses={
        204: {"description": "The individual API Invoker matching onboardingId was offboarded."},
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
async def onboarded_invokers_onboarding_id_delete(
    onboardingId: str = Path(None, description="String identifying an individual on-boarded API invoker resource"),
) -> None:
    """Deletes an individual API Invoker."""
    ...


@router.put(
    "/onboardedInvokers/{onboardingId}",
    responses={
        200: {"model": APIInvokerEnrolmentDetails, "description": "API invoker details updated successfully."},
        202: {"description": "The CAPIF core has accepted the API invoker update details request and is processing it."},
        204: {"description": "API invoker’s information updated successfully, with no content to be sent in the response body."},
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
async def onboarded_invokers_onboarding_id_put(
    onboardingId: str = Path(None, description="String identifying an individual on-boarded API invoker resource"),
    api_invoker_enrolment_details: APIInvokerEnrolmentDetails = Body(None, description="representation of the API invoker details to be updated in CAPIF core function"),
) -> APIInvokerEnrolmentDetails:
    """Updates an individual API invoker details."""
    ...


@router.post(
    "/onboardedInvokers",
    responses={
        201: {"model": APIInvokerEnrolmentDetails, "description": "API invoker on-boarded successfully."},
        202: {"description": "The CAPIF core has accepted the Onboarding request and is processing it."},
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
async def onboarded_invokers_post(
    api_invoker_enrolment_details: APIInvokerEnrolmentDetails = Body(None, description=""),
) -> APIInvokerEnrolmentDetails:
    """Creates a new individual API Invoker profile."""
    ...
