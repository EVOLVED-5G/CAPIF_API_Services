from flask import current_app
from .resources import Resource
from .auth_manager import AuthManager

class InternalEventOperations(Resource):

    def __init__(self):
        Resource.__init__(self)
        self.auth_manager = AuthManager()

    def delete_all_events(self, subscriber_id):

        mycol = self.db.get_col_by_name(self.db.event_collection)
        my_query = {'subscriber_id': subscriber_id}
        mycol.delete_many(my_query)

        self.auth_manager.remove_auth_all_event(subscriber_id)

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