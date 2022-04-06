from flask import g
from flask_restful import abort
from api import auth
from api.models.user import UserModel
from api.schemas.user import UserSchema, UserRequestSchema, EditUserSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from helpers.shortcuts import get_object_or_404


@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(description='Full: Get users by id')
    @doc(summary='Get users by id')
    @doc(responses={"404": {"description": "Not found"}})
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        return get_object_or_404(UserModel, user_id), 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required(role="admin")
    @doc(description='Edit users by id')
    @doc(responses={"401": {"description": "Unauthorized"}})
    @marshal_with(UserSchema, code=200)
    @use_kwargs(EditUserSchema, location='json')
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required(role="admin")
    @doc(responses={"401": {"description": "Unauthorized"}})
    @doc(responses={"404": {"description": "Not found"}})
    @doc(description='Deleted users by id')
    def delete(self, user_id):
        user = get_object_or_404(UserModel, user_id)
        user.delete()
        return f"Note ${user_id} deleted.", 200


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @doc(description='Full: Get all users')
    @doc(summary='Get all users')
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    # @auth.login_required
    @doc(summary='Create new user')
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location='json')
    def post(self, **kwargs):
        # admin = g.getuser()
        # if admin.role != 'admin':
        #     return {"error": f"Not admin create user"}, 400

        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            return {"error": f"User with username:{user.username} already exist"}, 400
        return user, 201
