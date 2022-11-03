from app.db import db
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    display_name = db.Column(db.String(128))
    display_image = db.Column(db.String)
    create_time = db.Column(db.DateTime)

    def __init__(self, username, password, display_name, display_image):
        self.id = uuid.uuid4()
        self.username = username
        self.password = password
        self.display_name = display_name
        self.display_image = display_image
        self.create_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password):
        if password == self.password:
            return True
        return False

    def json(self):
        return {"id": str(self.id), "username": self.username, "display_name": self.display_name, "display_image": self.display_image}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
