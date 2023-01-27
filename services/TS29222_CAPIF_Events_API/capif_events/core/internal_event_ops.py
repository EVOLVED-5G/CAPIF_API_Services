from flask import current_app
from .resources import Resource

class InternalEventOperations(Resource):

    def delete_all_events(self, subscriber_id):

        mycol = self.db.get_col_by_name(self.db.event_collection)
        my_query = {'subscriber_id': subscriber_id}
        mycol.delete_many(my_query)

    def get_event_subscriptions(self, event):
        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)

            query= {'events':event}
            subscriptions = mycol.find(query)

            if  subscriptions is None:
                current_app.logger.error("Not found event subscriptions")

            else:
                json_docs=[]
                for subscription in subscriptions:
                    json_docs.append(subscription)

                return json_docs

        except Exception as e:
            current_app.logger.error("An exception occurred ::" + str(e))
            return False