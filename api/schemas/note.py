from api import ma
from api.models.note import NoteModel
from api.schemas.tag import TagSchema
from api.schemas.user import UserSchema, EditUserSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    _links = ma.Hyperlinks({
        'self': ma.URLFor('noteresource', values=dict(note_id="<id>")),
        'collection': ma.URLFor('noteslistresource')
    })

    id = ma.auto_field()
    text = ma.auto_field()
    private = ma.auto_field()
    author = ma.Nested(UserSchema())
    tags = ma.Nested(TagSchema(many=True))
    isDeleted = ma.auto_field()


class NoteRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    text = ma.Str(required=True)
    private = ma.Bool(required=True)


class EditNoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    text = ma.auto_field()
    private = ma.auto_field()
    author = ma.Nested(EditUserSchema())
    tags = ma.Nested(TagSchema(many=True))
