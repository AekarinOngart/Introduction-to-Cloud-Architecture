from app.db import db

from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid


class ProductsModel(db.Model):
    __tablename__ = "products"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.String(128))
    type = db.Column(db.String(128))
    sex = db.Column(db.String(128))
    color = db.Column(db.String(128))
    image = db.Column(db.String(128))

    def __init__(self, name, price, type, sex, color, image):
        self.id = uuid.uuid4()
        self.name = name
        self.price = price
        self.type = type
        self.sex = sex
        self.color = color
        self.image = image

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"id": str(self.id), "name": self.name, "price": self.price, "type": self.type, "sex": self.sex, "color": self.color, "image": self.image}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
