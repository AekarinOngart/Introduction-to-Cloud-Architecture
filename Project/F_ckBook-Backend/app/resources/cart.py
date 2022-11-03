import json
from flask_restful import Resource, reqparse
from app.models.cart import CartModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger


class Cart(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        user = json.loads(get_jwt_identity())
        carts = CartModel.find_by_owner_cart(user["id"])

        if carts:
            return {"owner_cart": user["id"], "products": [cart.json() for cart in carts]}
        return {"message": "Cart not found"}, 404

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title owner_post image"""

        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        user = json.loads(get_jwt_identity())
        post = CartModel(user["id"], data["product_id"])
        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred creating the post."}, 500
        return {"message": "Create Cart success"}

    @jwt_required()  # Requires dat token
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("cart_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        post = CartModel.find_by_id(data["cart_id"])
        if post:
            post.delete_from_db()
        return {"message": "Cart deleted"}
