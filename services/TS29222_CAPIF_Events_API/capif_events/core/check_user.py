import sys
from ..db.db import MongoDatabse

class CapifUsersOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def check_capif_user(self, common_name, role_invoker, role_apf):
        try:
            mycol = self.db.get_col_by_name(self.db.user_collection)

            capif_user = mycol.find_one({"$and": [{"cn": common_name}, {"$or": [{"role": role_invoker}, {"role": role_apf}]}]})

            if capif_user is None:
                return False
            
            return True
        except Exception as e:
            print("An exception occurred ::", e, file=sys.stderr)
            return False