
from flask import current_app
from .resources import Resource

class InternalSecurityOps(Resource):

    def delete_intern_servicesecurity(self, api_invoker_id):

        mycol = self.db.get_col_by_name(self.db.security_info)
        my_query = {'api_invoker_id': api_invoker_id}
        mycol.delete_many(my_query)

    def update_intern_servicesecurity(self, id):

        security_col = self.db.get_col_by_name(self.db.security_info)

        security_contexts = security_col.find({"$or":[{"security_info.aef_id":id}, {"security_info.api_id":id}]})

        for security_context in security_contexts:
            new_security_info = [info for info  in security_context["security_info"] if info["aef_id"]!=id and info["api_id"] != id]
            security_context["security_info"] = new_security_info
            security_col.update_one({'api_invoker_id':security_context["api_invoker_id"]}, {"$set":security_context})
