from pydoc import classname
from app.db import db
from app.models.products import ProductsModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class CartModel(db.Model):
    __tablename__ = "cart"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    owner_cart = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey("products.id"), nullable=False)

    def __init__(self, owner_cart, product_id):
        self.id = uuid.uuid4()
        self.owner_cart = owner_cart
        self.product_id = product_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"id": str(self.id), "product": (ProductsModel.find_by_id(self.product_id)).json()}

    @classmethod
    def find_by_owner_cart(cls, owner_cart):
        return cls.query.filter_by(owner_cart=owner_cart).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
