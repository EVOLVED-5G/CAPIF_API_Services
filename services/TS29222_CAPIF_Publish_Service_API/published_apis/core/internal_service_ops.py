
from flask import current_app
from .resources import Resource

class InternalServiceOps(Resource):

    def delete_intern_service(self, apf_id):

        current_app.logger.info("Provider removed, removing services published by APF")
        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)
        my_query = {'apf_id': apf_id}
        mycol.delete_many(my_query)
        current_app.logger.info("Removed service")