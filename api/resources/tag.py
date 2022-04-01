from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from flask_restful import abort
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema


@doc(tags=['Tags'])
class TagResource(MethodResource):
    @doc(description='Full: Get tags by id')
    @doc(summary='Get tags by id')
    @doc(responses={"404": {"description": "Not found"}})
    @marshal_with(TagSchema, code=200)
    def get(self, tags_id):
        tag = TagModel.query.get(tags_id)
        if not tag:
            abort(404, error=f"Tag with id={tags_id} not found")
        return tag, 200

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
        note = TagModel.query.get(tag_id)
        if not note:
            abort(404, error=f"tag {tag_id} not found")
        note.delete()
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
            abort(400, error=f"Tag already exist")
        return tag, 201
