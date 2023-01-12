
from .resources import Resource
from flask import current_app


class InvokerInternalOperations(Resource):

    def update_services_list(self, invoker_id, api_id):

        service_col = self.db.get_col_by_name(self.db.service_col)
        invoker_col = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        invoker = invoker_col.find_one({'api_invoker_id':invoker_id})
        service = service_col.find_one({'api_id': api_id}, {"_id":0})

        invoker_api_list = invoker["api_list"]
        if invoker_api_list is None:
            invoker_api_list = []

        invoker_api_list.append(service)
        invoker["api_list"] = invoker_api_list

        invoker_col.update_one({'api_invoker_id':invoker_id}, {"$set":invoker})

    def remove_services_list(self, invoker_id, api_id):
        service_col = self.db.get_col_by_name(self.db.service_col)
        invoker_col = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        invoker = invoker_col.find_one({'api_invoker_id':invoker_id})
        service = service_col.find_one({'api_id': api_id})

        invoker_api_list = invoker["api_list"]

        if service in invoker_api_list:
            invoker_api_list.remove(service)

        invoker["api_list"] = invoker_api_list

        invoker_col.update_one({'api_invoker_id':invoker_id}, {"$set":invoker})

