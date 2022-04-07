from werkzeug.exceptions import NotFound
from flask_babel import _


def get_object_or_404(model, object_id):
    obj = model.query.get(object_id)
    if not obj:
        raise NotFound(description=_("{model} with id=%(object_id)s not found", bject_id=object_id))
    return obj
