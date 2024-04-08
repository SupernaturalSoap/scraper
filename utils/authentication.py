class Authentication:
    def __init__(self, token):
        self.token = token

    def authenticate(self, provided_token):
        return provided_token == self.token