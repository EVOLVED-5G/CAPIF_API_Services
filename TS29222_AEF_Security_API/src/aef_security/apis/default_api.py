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

from aef_security.models.extra_models import TokenModel  # noqa: F401
from aef_security.models.check_authentication_req import CheckAuthenticationReq
from aef_security.models.check_authentication_rsp import CheckAuthenticationRsp
from aef_security.models.problem_details import ProblemDetails
from aef_security.models.revoke_authorization_req import RevokeAuthorizationReq
from aef_security.models.revoke_authorization_rsp import RevokeAuthorizationRsp


router = APIRouter()


@router.post(
    "/check-authentication",
    responses={
        200: {"model": CheckAuthenticationRsp, "description": "The request was successful."},
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
    summary="Check authentication.",
)
async def check_authentication_post(
    check_authentication_req: CheckAuthenticationReq = Body(None, description=""),
) -> CheckAuthenticationRsp:
    ...


@router.post(
    "/revoke-authorization",
    responses={
        200: {"model": RevokeAuthorizationRsp, "description": "The request was successful."},
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
    summary="Revoke authorization.",
)
async def revoke_authorization_post(
    revoke_authorization_req: RevokeAuthorizationReq = Body(None, description=""),
) -> RevokeAuthorizationRsp:
    ...
