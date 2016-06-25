from requests.auth import AuthBase


class JWTAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return all([
            self.token == getattr(other, 'token', None),
        ])

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = "JWT " + self.token;
        return r
