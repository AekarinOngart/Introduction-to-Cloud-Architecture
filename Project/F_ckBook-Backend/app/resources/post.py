import json
import base64
import os
from uuid import uuid4
from flask_restful import Resource, reqparse
from app.models.post import PostModel
from app.models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger
from sqlalchemy import or_
import werkzeug


class Post(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("owner_post", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        owner_post = data["owner_post"]
        posts = PostModel.find_by_owner_post(owner_post)
        if posts:
            return {"user_id": owner_post, "posts": [post.json() for post in posts]}
        return {"message": "Post not found"}, 404

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title owner_post image"""

        parser = reqparse.RequestParser()
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument(
            "image",
            type=werkzeug.datastructures.FileStorage,
            location="files",
        )
        data = parser.parse_args()

        user = json.loads(get_jwt_identity())
        owner_post = user["id"]

        message = data["message"]
        image = data["image"]
        image_base64 = base64.b64encode(image.read()).decode("utf-8")
        _, filetype = os.path.splitext(image.filename)
        data["image"] = "data:image/" + filetype[1:] + ";base64," + image_base64

        post = PostModel(owner_post, message, data["image"])
        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred creating the post."}, 500

        return {"message": "Create Post success"}

    @jwt_required()  # Requires dat token
    def put(self):
        """update post require uuid, title,message, owner_post, image, like"""

        parser = reqparse.RequestParser()
        parser.add_argument("uuid", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("title", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("owner_post", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("image", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        post = PostModel.find_by_id(data["uuid"])
        post.title = data["title"]
        post.message = data["message"]
        post.owner_post = data["owner_post"]
        post.image = data["image"]

        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred updating the post."}, 500

        return {"message": "Post update success"}

    @jwt_required()  # Requires dat token
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        post = PostModel.find_by_id(data["post_id"])
        if post:
            try:
                post.delete_from_db()
            except:
                return {"message": "An error occurred delete the post."}, 500
        return {"message": "Post deleted"}


class PostList(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        posts = PostModel.query.all()
        return {"posts": [post.json() for post in posts]}


class LikePost(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        post = PostModel.find_by_id(data["post_id"])
        post.like += 1
        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred like the post."}, 500
        return {"message": "Like success"}
