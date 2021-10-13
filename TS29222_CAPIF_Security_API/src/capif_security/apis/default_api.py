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

from capif_security.models.extra_models import TokenModel  # noqa: F401
from capif_security.models.access_token_err import AccessTokenErr
from capif_security.models.access_token_rsp import AccessTokenRsp
from capif_security.models.problem_details import ProblemDetails
from capif_security.models.security_notification import SecurityNotification
from capif_security.models.service_security import ServiceSecurity


router = APIRouter()


@router.post(
    "/securities/{securityId}/token",
    responses={
        200: {"model": AccessTokenRsp, "description": "Successful Access Token Request"},
        307: {"description": "Temporary Redirect"},
        308: {"description": "Permanent Redirect"},
        400: {"model": AccessTokenErr, "description": "Error in the Access Token Request"},
    },
    tags=["default"],
)
async def securities_security_id_token_post(
    securityId: str = Path(None, description="Identifier of an individual API invoker"),
    grant_type: str = Form(None, description=""),
    client_id: str = Form(None, description=""),
    client_secret: str = Form(None, description=""),
    scope: str = Form(None, description=""),
) -> AccessTokenRsp:
    ...


@router.delete(
    "/trustedInvokers/{apiInvokerId}",
    responses={
        204: {"description": "No Content (Successful deletion of the existing subscription)"},
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
async def trusted_invokers_api_invoker_id_delete(
    apiInvokerId: str = Path(None, description="Identifier of an individual API invoker"),
) -> None:
    ...


@router.post(
    "/trustedInvokers/{apiInvokerId}/delete",
    responses={
        204: {"description": "Successful revoked."},
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
async def trusted_invokers_api_invoker_id_delete_post(
    apiInvokerId: str = Path(None, description="Identifier of an individual API invoker"),
    security_notification: SecurityNotification = Body(None, description="Revoke the authorization of the API invoker for APIs."),
) -> None:
    ...


@router.get(
    "/trustedInvokers/{apiInvokerId}",
    responses={
        200: {"model": ServiceSecurity, "description": "The security related information of the API Invoker based on the request from the API exposing function."},
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
async def trusted_invokers_api_invoker_id_get(
    apiInvokerId: str = Path(None, description="Identifier of an individual API invoker"),
    authentication_info: bool = Query(None, description="When set to &#39;true&#39;, it indicates the CAPIF core function to send the authentication information of the API invoker. Set to false or omitted otherwise."),
    authorization_info: bool = Query(None, description="When set to &#39;true&#39;, it indicates the CAPIF core function to send the authorization information of the API invoker. Set to false or omitted otherwise."),
) -> ServiceSecurity:
    ...


@router.put(
    "/trustedInvokers/{apiInvokerId}",
    responses={
        201: {"model": ServiceSecurity, "description": "Successful created."},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        411: {"model": ProblemDetails, "description": "Length Required"},
        413: {"model": ProblemDetails, "description": "Payload Too Large"},
        414: {"model": ProblemDetails, "description": "URI Too Long"},
        415: {"model": ProblemDetails, "description": "Unsupported Media Type"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["default"],
)
async def trusted_invokers_api_invoker_id_put(
    apiInvokerId: str = Path(None, description="Identifier of an individual API invoker"),
    service_security: ServiceSecurity = Body(None, description="create a security context for an API invoker"),
) -> ServiceSecurity:
    ...


@router.post(
    "/trustedInvokers/{apiInvokerId}/update",
    responses={
        200: {"model": ServiceSecurity, "description": "Successful updated."},
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
async def trusted_invokers_api_invoker_id_update_post(
    apiInvokerId: str = Path(None, description="Identifier of an individual API invoker"),
    service_security: ServiceSecurity = Body(None, description="Update the security context (e.g. re-negotiate the security methods)."),
) -> ServiceSecurity:
    ...
