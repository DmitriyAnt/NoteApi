from flask_apispec import marshal_with, use_kwargs, doc, MethodResource
from webargs import fields
from flask_restful import abort
from api import auth, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.models.user import UserModel
from api.schemas.note import NoteSchema, NoteRequestSchema, EditNoteSchema
from helpers.shortcuts import get_object_or_404


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(description='Full: Note users by id')
    @doc(summary='Get Note by id')
    @marshal_with(NoteSchema(), 200)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note, 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary='Edit note by id')
    @marshal_with(EditNoteSchema, code=200)
    @use_kwargs(NoteRequestSchema, location='json')
    def put(self, note_id, **kwargs):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        note = get_object_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = kwargs["text"]

        note.private = kwargs.get("private") or note.private
        note.save()
        return note, 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(description='Deleted note by id')
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        author = g.user
        note = get_object_or_404(NoteModel, note_id)
        if note.author != author:
            return {"error": f"Forbidden"}, 403
        note.delete()
        return f"Note ${note_id} deleted.", 200


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(description='Full: Get all notes')
    @doc(summary='Get all notes')
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id).all()
        return notes, 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary='Create new note')
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteRequestSchema, location='json')
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = get_object_or_404(NoteModel, note_id)
        # print("note kwargs = ", kwargs)

        tags_ids = kwargs.get("tags", [])
        for tag_id in tags_ids:
            tag = TagModel.query.get(tag_id)
            if tag:
                note.tags.append(tag)
        note.save()
        return note, 200

    # Not implemented
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteSchema)
    def delete(self, note_id, **kwargs):
        note = get_object_or_404(NoteModel, note_id)
        # print("note kwargs = ", kwargs)

        tags_ids = kwargs.get("tags", [])
        for tag_id in tags_ids:
            tag = TagModel.query.get(tag_id)
            if tag:
                note.tags.append(tag)
        note.save()
        return note, 200


@doc(tags=['Notes'])
class NotesFilterResource(MethodResource):
    @doc(description='Get user notes')
    @doc(summary='Get user notes')
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self, user_id):
        author = get_object_or_404(UserModel, user_id)
        notes = NoteModel.query.join(NoteModel.author).filter_by(username=author.username).all()
        return notes, 200

    @doc(summary="Get notes with filters")
    @marshal_with(NoteSchema(many=True))
    @use_kwargs({"private": fields.Bool(), "username": fields.Str(), "tag_name": fields.Str()}, location="query")
    def get(self, **kwargs):
        notes = NoteModel.query
        if kwargs.get("private"):
            notes = notes.filter_by(private=kwargs["private"])
        if kwargs.get("username"):
            notes = notes.join(NoteModel.author).filter_by(username=kwargs["username"])
        if kwargs.get("tag_name"):
            notes = notes.join(NoteModel.tags).filter_by(name=kwargs["tag_name"])
        return notes.all(), 200

