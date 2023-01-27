
from flask import current_app
from .resources import Resource

class InternalSecurityOps(Resource):

    def delete_intern_servicesecurity(self, api_invoker_id):

        current_app.logger.info("Invoker Removed, removing security context")
        mycol = self.db.get_col_by_name(self.db.security_info)
        my_query = {'api_invoker_id': api_invoker_id}
        mycol.delete_many(my_query)
        current_app.logger.info("Removed security context")