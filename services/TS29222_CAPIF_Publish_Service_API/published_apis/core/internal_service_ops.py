
from flask import current_app
from .resources import Resource
from .auth_manager import AuthManager

class InternalServiceOps(Resource):

    def __init__(self):
        Resource.__init__(self)
        self.auth_manager = AuthManager()

    def delete_intern_service(self, apf_id):

        current_app.logger.info("Provider removed, removing services published by APF")
        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)
        my_query = {'apf_id': apf_id}
        mycol.delete_many(my_query)

        self.auth_manager.remove_auth_all_service(apf_id)

        current_app.logger.info("Removed service")