from app.db import db

from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.user import UserModel
import uuid


class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey("post.id"), nullable=False)
    owner_comment = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String)
    like = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, post_id, owner_comment, message):
        self.id = uuid.uuid4()
        self.post_id = post_id
        self.owner_comment = owner_comment
        self.message = message
        self.like = 0
        self.create_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        self.update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": str(self.id),
            "owner_comment": UserModel.find_by_id(str(self.owner_comment)).json(),
            "message": self.message,
            "like": self.like,
            "update_time": str(self.update_time),
        }

    @classmethod
    def find_by_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
