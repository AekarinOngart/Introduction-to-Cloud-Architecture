from app.db import db

from sqlalchemy.dialects.postgresql import UUID
from app.models.comment import CommentModel
from app.models.user import UserModel
from datetime import datetime
import uuid


class PostModel(db.Model):
    __tablename__ = "post"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.String(128))
    message = db.Column(db.String)
    image = db.Column(db.String)
    like = db.Column(db.Integer)
    owner_post = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, owner_post, message="", image="", like=0):
        self.id = uuid.uuid4()
        self.title = ""
        self.image = image
        self.message = message
        self.owner_post = owner_post
        self.like = like
        self.comment_list = []
        self.create_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        self.update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_comment(self):
        return CommentModel.find_by_post_id(self.id)

    def json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "message": self.message,
            "image": self.image,
            "like": self.like,
            "owner_post": UserModel.find_by_id(str(self.owner_post)).json(),
            "comment_list": [comment.json() for comment in self.get_comment()],
            "update_time": str(self.update_time),
        }

    @classmethod
    def find_by_owner_post(cls, owner_post):
        """input owner post uuid will return post list"""
        return cls.query.filter_by(owner_post=owner_post).limit(100).all()

    @classmethod
    def find_by_id(cls, _id):
        """input post uuid will return post obj"""
        return cls.query.filter_by(id=_id).first()
