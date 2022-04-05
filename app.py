from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NoteSetTagsResource
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

api.add_resource(NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                )
api.add_resource(NoteSetTagsResource,
                 '/notes/<int:note_id>/set_tags')
api.add_resource(TagListResource,
                 '/tags')  # GET, POST
api.add_resource(TagResource,
                 '/tags/<int:tags_id>')  # GET, PUT, DELETE

# Doc
docs.register(UserResource)
docs.register(UsersListResource)
docs.register(NoteResource)
docs.register(NotesListResource)
docs.register(NoteSetTagsResource)
docs.register(TagResource)
docs.register(TagListResource)


#Дляформирования правильной ошибки десериализации:
@app.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, 'exc')
    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']
    return { 'status': 'error', 'result': messages }, 400


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
