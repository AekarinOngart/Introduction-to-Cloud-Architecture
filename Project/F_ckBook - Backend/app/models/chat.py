from app.db import db

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc
from datetime import datetime
import uuid


class ChatModel(db.Model):
    __tablename__ = "chat"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sender_id, receiver_id, message):
        self.id = uuid.uuid4()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.create_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"receiver_id": str(self.receiver_id), "message": self.message, "create_time": str(self.create_time)}

    @classmethod
    def find_by_receiver_id(cls, sender_id, receiver_id):
        return cls.query.filter_by(receiver_id=receiver_id, sender_id=sender_id).order_by(desc(cls.create_time)).limit(100).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
