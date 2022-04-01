from flask_restful import abort, Resource, reqparse
from api import auth, docs
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc


@doc(description='Api for notes.', tags=['Users'])
class UserResource(MethodResource):
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required #(role="admin")
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        user.username = user_data["username"]
        user.save()
        return user_schema.dump(user), 200

    @auth.login_required  #(role="admin")
    def delete(self, user_id):
        note = UserModel.query.get(user_id)
        if not note:
            abort(404, error=f"User {user_id} not found")
        note.delete()
        return f"Note ${user_id} deleted.", 200


class UsersListResource(Resource):
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user_data.username} already exist")
        return user_schema.dump(user), 201
