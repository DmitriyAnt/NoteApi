from api import g, auth
from flask_restful import Resource


class TokenResource(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}
