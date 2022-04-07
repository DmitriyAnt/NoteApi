from sqlalchemy.sql import expression
from api import db
from api.models.user import UserModel
from api.models.tag import TagModel
from api.models.mixins import ModelDBExt

# Core
tags_to_notes = db.Table('tags_to_notes',
                         db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                         db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                         )


# ORM
class NoteModel(db.Model, ModelDBExt):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship(TagModel, secondary=tags_to_notes, lazy='subquery', backref=db.backref('notes', lazy=True))
    isDeleted = db.Column(db.Boolean(), default=False, server_default=expression.false(), nullable=False)

    def delete(self):
        self.isDeleted = True
        db.session.commit()

