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

from capif_events.models.extra_models import TokenModel  # noqa: F401
from capif_events.models.event_subscription import EventSubscription
from capif_events.models.problem_details import ProblemDetails


router = APIRouter()


@router.post(
    "/{subscriberId}/subscriptions",
    responses={
        201: {"model": EventSubscription, "description": "Created (Successful creation of subscription)"},
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
async def subscriber_id_subscriptions_post(
    subscriberId: str = Path(None, description="Identifier of the Subscriber"),
    event_subscription: EventSubscription = Body(None, description=""),
) -> EventSubscription:
    """Creates a new individual CAPIF Event Subscription."""
    ...


@router.delete(
    "/{subscriberId}/subscriptions/{subscriptionId}",
    responses={
        204: {"description": "The individual CAPIF Events Subscription matching the subscriptionId is deleted."},
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
async def subscriber_id_subscriptions_subscription_id_delete(
    subscriberId: str = Path(None, description="Identifier of the Subscriber"),
    subscriptionId: str = Path(None, description="Identifier of an individual Events Subscription"),
) -> None:
    """Deletes an individual CAPIF Event Subscription."""
    ...
