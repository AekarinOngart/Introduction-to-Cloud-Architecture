from flask_restful import Resource, reqparse
from app.models.products import ProductsModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger


class Product(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        carts = ProductsModel.get_all()
        if carts:
            return {"products": [cart.json() for cart in carts]}
        return {"message": "Product not found"}, 404

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title owner_post image"""

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("price", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("type", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("sex", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("color", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("image", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        product = ProductsModel(**data)

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred creating the product."}, 500
        return {"message": "Create Post success"}

    @jwt_required()  # Requires dat token
    def put(self):
        """update post require uuid, title,message, owner_post, image, like"""

        parser = reqparse.RequestParser()
        parser.add_argument("uuid", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("name", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("price", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("type", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("sex", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("color", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("image", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        post = ProductsModel.find_by_id(data["uuid"])
        post.name = data["name"]
        post.price = data["price"]
        post.type = data["type"]
        post.sex = data["sex"]
        post.color = data["color"]
        post.image = data["image"]

        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred updating the product."}, 500
        return {"message": "Product update success"}

    @jwt_required()  # Requires dat token
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        post = ProductsModel.find_by_id(data["product_id"])
        if post:
            try:
                post.delete_from_db()
            except:
                return {"message": "An error occurred delete the product."}, 500
        return {"message": "Product deleted"}
