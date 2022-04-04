from sqlalchemy.exc import IntegrityError

from api import db
from api.schemas.user import UserRequestSchema

from api.models.note import NoteModel
from api.models.user import UserModel
from config import BASE_DIR, base_dir

# path_to_fixture = os.path.join(base_dir, "fixtures" , "users.json")
path_to_fixture = BASE_DIR / "fixtures" / "users.json"
with open(path_to_fixture, "r", encoding="UTF-8") as f:
    users_data = UserRequestSchema(many=True).loads(f.read())
    count = 0
    for user_data in users_data:
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
            count += 1
        except IntegrityError:
            db.session.rollback()
    print(f"{count} users created")
