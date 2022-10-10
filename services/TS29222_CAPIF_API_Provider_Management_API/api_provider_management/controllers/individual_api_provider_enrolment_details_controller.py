from email.quoprimime import body_decode
import connexion
import six
import json

from flask import Response, request
from ..core.provider_enrolment_details_api import ProviderManagementOperations
from ..core.check_user import CapifUsersOperations
from ..encoder import JSONEncoder
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.api_provider_enrolment_details_patch import APIProviderEnrolmentDetailsPatch  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util
from cryptography.hazmat.backends import default_backend
from cryptography import x509

check_user = CapifUsersOperations()
provider_management_ops = ProviderManagementOperations()


def modify_ind_api_provider_enrolment(api_prov_dom_id, body):  # noqa: E501
    """modify_ind_api_provider_enrolment

    Modify an individual API provider details. # noqa: E501

    :param registration_id: 
    :type registration_id: str
    :param api_provider_enrolment_details_patch: 
    :type api_provider_enrolment_details_patch: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')


    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

    capif_user = check_user.check_capif_user(cn, "exposer")

    if not capif_user:
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = APIProviderEnrolmentDetailsPatch.from_dict(connexion.request.get_json())  # noqa: E501
   
    res = provider_management_ops.patch_api_provider_enrolment_details(api_prov_dom_id, body)

    return res
