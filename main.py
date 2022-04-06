from api import api, app, docs
from api.resources import note
from api.resources.tag import TagListResource, TagResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from config import Config

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE
api.add_resource(TokenResource,
                 '/auth/token')  # GET
api.add_resource(note.NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(note.NotesPublicResource,
                 '/notes/public',  # GET
                 )
api.add_resource(note.NotesPublicFilterResource,
                 '/notes/public/filter',  # GET
                 )
api.add_resource(note.NoteResource,
                 '/notes/<int:note_id>'  # GET, PUT, DELETE
                 )
api.add_resource(note.NoteSetTagsResource,
                 '/notes/<int:note_id>/set_tags')
api.add_resource(TagListResource,
                 '/tags')  # GET, POST
api.add_resource(TagResource,
                 '/tags/<int:tags_id>')  # GET, PUT, DELETE
api.add_resource(note.NotesFilterResource,
                 '/users/<int:user_id>/notes',
                 "/notes/filter")

# Doc
docs.register(UserResource)
docs.register(UsersListResource)
docs.register(note.NoteResource)
docs.register(note.NotesPublicResource)
docs.register(note.NotesPublicFilterResource)
docs.register(note.NotesListResource)
docs.register(note.NoteSetTagsResource)
docs.register(TagResource)
docs.register(TagListResource)
docs.register(note.NotesFilterResource)


# Дляформирования правильной ошибки десериализации:
@app.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, 'exc')
    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']
    return {'status': 'error', 'result': messages}, 400


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
