from flask_apispec import marshal_with, use_kwargs, doc, MethodResource
from webargs import fields
from flask_restful import abort
from api import auth, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import NoteSchema, NoteRequestSchema


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
    @doc(description='Edit note by id')
    @marshal_with(NoteSchema, code=200)
    @use_kwargs(NoteRequestSchema, location='json')
    def put(self, note_id, **kwargs):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
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
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.delete()
        return f"Note ${note_id} deleted.", 200


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @doc(description='Full: Get all notes')
    @doc(summary='Get all notes')
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        notes = NoteModel.query.all()
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
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            return {"error": f"note {note_id} not found"}, 400
        print("note kwargs = ", kwargs)

        tag_id = kwargs.get("tags", [])
        for tag in tag_id:
            t = TagModel.query.get(tag)
            note.tags.append(t)
        note.save()
        return note, 200