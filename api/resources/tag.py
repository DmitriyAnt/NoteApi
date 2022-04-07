from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema
from helpers.shortcuts import get_object_or_404


@doc(tags=['Tags'])
class TagResource(MethodResource):
    @doc(description='Full: Get tags by id')
    @doc(summary='Get tags by id')
    @doc(responses={"404": {"description": "Not found"}})
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        return get_object_or_404(TagModel, tag_id), 200

    @doc(description='Edit tags by id')
    @doc(responses={"401": {"description": "Unauthorized"}})
    @marshal_with(TagSchema, code=200)
    @use_kwargs(TagRequestSchema, location='json')
    def put(self, tags_id, **kwargs):
        user = TagModel.query.get(tags_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @doc(responses={"401": {"description": "Unauthorized"}})
    @doc(responses={"404": {"description": "Not found"}})
    @doc(description='Deleted tag by id')
    def delete(self, tag_id):
        tag = get_object_or_404(TagModel, tag_id)
        tag.delete()
        return f"Tag ${tag_id} deleted.", 200


@doc(tags=['Tags'])
class TagListResource(MethodResource):
    @doc(description='Full: Get all tags')
    @doc(summary='Get all tags')
    @marshal_with(TagSchema(many=True), code=200)
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary='Create new tags')
    @marshal_with(TagSchema, code=201)
    @use_kwargs(TagRequestSchema, location='json')
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if not tag.id:
            return {"error": f"Tag already exist"}, 400
        return tag, 201
