class User():
    def __init__(self):
        self.is_authenticated = False
        self.is_active = True
        self.anonymous = False
        self.id = str("unique string for a user")

    def get_id(self):
        return self.id