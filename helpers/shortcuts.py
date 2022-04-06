def get_object_or_404(model, object_id):
    obj = model.query.get(object_id)
    if not obj:
        return {"error": f"{model} with id={object_id} not found"}, 404
    return obj
