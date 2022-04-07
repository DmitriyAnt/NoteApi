from werkzeug.exceptions import NotFound


def get_object_or_404(model, object_id):
    obj = model.query.get(object_id)
    if not obj:
        raise NotFound(description=f"{model} with id={object_id} not found")
    return obj
