import json

from sqlalchemy.exc import IntegrityError

from api import db
from api.models.note import NoteModel
from api.models.tag import TagModel
from config import BASE_DIR


def load_tags_to_note_fixture():
    path_to_fixture = BASE_DIR / "fixtures" / "tags_to_note.json"
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        data = json.load(f)
        count = 0
        for record in data["records"]:
            note = NoteModel.query.get(record["note"])
            for tag_id in record["tags"]:
                tag = TagModel.query.get(tag_id)
                if tag:
                    note.tags.append(tag)
            db.session.add(note)
            try:
                db.session.commit()
                count += 1
            except IntegrityError:
                print(f"Object skipped")
                db.session.rollback()

        print(f"{count} notes updated")


if __name__ == "__main__":
    load_tags_to_note_fixture()