class CapifUserManager():
    def __init__(self):
        self.capif_users = {}
        self.register_users = []

    def update_register_users(self, value):
        self.register_users.append(value)

    def update_capif_users_dicts(self, key, value):
        self.capif_users[key] = value

    def remove_capif_users_entry(self, key):
        self.capif_users.pop(key)

    def remove_register_users_entry(self, value):
        self.register_users.remove(value)

    def get_capif_users_dict(self):
        return self.capif_users

    def get_register_users(self):
        return self.register_users


CAPIF_USERS = CapifUserManager()