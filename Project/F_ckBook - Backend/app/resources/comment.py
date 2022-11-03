import json
from flask_restful import Resource, reqparse
from app.models.comment import CommentModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger


class Comment(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        post_id = data["post_id"]
        comments = CommentModel.find_by_post_id(post_id)
        if comments:
            return {"post_id": post_id, "comments": [comment.json() for comment in comments]}
        return {"message": "Comment not found"}, 404

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title post_id image"""
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        user = json.loads(get_jwt_identity())

        post_id = data["post_id"]
        owner_comment = user["id"]
        message = data["message"]

        comment = CommentModel(post_id, owner_comment, message)
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred creating the comment."}, 500

        return {"message": "Create Comment success"}

    @jwt_required()  # Requires dat token
    def put(self):
        """update comment require uuid, title,message, post_id, image, like"""

        parser = reqparse.RequestParser()
        parser.add_argument("comment_id", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        comment = CommentModel.find_by_id(data["comment_id"])
        comment.message = data["message"]

        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred updating the comment."}, 500
        return {"message": "Comment update success"}

    @jwt_required()  # Requires dat token
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("comment_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        comment = CommentModel.find_by_id(data["comment_id"])
        if comment:
            try:
                comment.delete_from_db()
            except:
                return {"message": "An error occurred delete the comment."}, 500
        return {"message": "Comment deleted"}


class LikeComment(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("comment_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        comment = CommentModel.find_by_id(data["comment_id"])
        comment.like += 1
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred creating the comment."}, 500
        return {"message": "Like success"}
