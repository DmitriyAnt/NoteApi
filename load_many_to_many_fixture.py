import json

from sqlalchemy.exc import IntegrityError

from api import db
from config import BASE_DIR


def load_tags_to_note_fixture():
    path_to_fixture = BASE_DIR / "fixtures" / "tags_to_note.json"
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
                print(f"Object skipped")
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
    load_tags_to_note_fixture()