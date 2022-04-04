import json

import click
from sqlalchemy.exc import IntegrityError
from api import db
from api.models.note import NoteModel
from api.models.user import UserModel
from config import BASE_DIR

# path_to_fixture = os.path.join(base_dir, "fixtures" , "users.json")
# path_to_fixture = BASE_DIR / "fixtures" / "notes.json"
models = {
    "NoteModel": NoteModel,
    "UserModel": UserModel,
}


@click.command
@click.argument('message')
def load_fixtures(message):
    path_to_fixture = BASE_DIR / "fixtures" / message
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        data = json.load(f)
        count = 0
        model_name = data["model"]
        model = models[model_name]
        for record in data["records"]:
            model_obj = model(**record)
            db.session.add(model_obj)
            try:
                db.session.commit()
                count += 1
            except IntegrityError:
                db.session.rollback()

        print(f"{count} records created")


# users_data = UserRequestSchema(many=True).loads(f.read())
# count = 0
# for user_data in users_data:
#     user = UserModel(**user_data)
#     db.session.add(user)
#     try:
#         db.session.commit()
#         count += 1
#     except IntegrityError:
#         db.session.rollback()
#         print(f"User {user.username} already exists")


if __name__ == "__main__":
    load_fixtures()
