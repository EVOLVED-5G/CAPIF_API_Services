from flask import jsonify
from ..db.db import MongoDatabse


class Operations:

    def __init__(self):
        self.db = MongoDatabse()

    def get_invokers(self):

        mycol = self.db.get_col_by_name(self.db.invokers)

        try:
            invokers = mycol.find({}, {"_id": 0})
            json_invokers = []
            for invoker in invokers:
                json_invokers.append(invoker)

            return jsonify(message="Invokers retrieved succesfully",
                           object=json_invokers), 200
        except Exception as e:
            return "Error when retreiving invoker list: ", e

    def get_invoker_security_context(self, invoker_id):

        security_context_col = self.db.get_col_by_name(
            self.db.security_context)

        try:
            security_contexts = security_context_col.find(
                {"api_invoker_id": invoker_id}, {"_id": 0})
            json_security_contexts = []
            for security_context in security_contexts:
                json_security_contexts.append(security_context)

            return jsonify(message="Security context retrieved succesfully",
                           object=json_security_contexts), 200

        except Exception as e:
            return "Error when retreiving invoker list: ", e

    def get_providers(self):

        try:
            mycol = self.db.get_col_by_name(self.db.providers)

            providers = mycol.find({}, {"_id": 0})
            json_providers = []
            for provider in providers:
                json_providers.append(provider)

            return jsonify(message="Providers retrieved succesfully",
                           object=json_providers), 200
        except Exception as e:
            return "Error when retreiving provider list: ", e

    def get_provider_services(self, id):

        services_col = self.db.get_col_by_name(self.db.services)

        try:
            services = services_col.find({"apf_id": id}, {"_id": 0})

            json_services = []
            for service in services:
                json_services.append(service)

            return jsonify(message="Services retrieved succesfully",
                           object=json_services), 200

        except Exception as e:
            return "Error when retreiving apf service list: ", e

    def get_events(self, id):

        events_col = self.db.get_col_by_name(self.db.events)

        try:
            events = events_col.find({"subscriber_id": id}, {"_id": 0})

            json_events = []
            for event in events:
                json_events.append(event)

            return jsonify(message="Events retrieved succesfully",
                           object=json_events), 200

        except Exception as e:
            return "Error when retreiving event: ", e
