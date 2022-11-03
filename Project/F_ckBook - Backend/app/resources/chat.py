import json
from flask_restful import Resource, reqparse
from app.models.chat import ChatModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger


class Chat(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("receiver_id", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        receiver_id = data["receiver_id"]
        user = json.loads(get_jwt_identity())
        chats = ChatModel.find_by_receiver_id(user["id"], receiver_id)
        if chats:
            return {"receiver_id": receiver_id, "comments": [chat.json() for chat in chats]}
        return {"message": "Chat not found"}, 404

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title post_id image"""
        parser = reqparse.RequestParser()
        parser.add_argument("receiver_id", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        user = json.loads(get_jwt_identity())

        receiver_id = data["receiver_id"]
        sender_id = user["id"]
        message = data["message"]

        comment = ChatModel(sender_id, receiver_id, message)
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred creating the chat."}, 500

        return {"message": "Create chat success"}


class ChatList(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def post(self):
        """create require title post_id image"""
        parser = reqparse.RequestParser()
        parser.add_argument("receiver_id", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("message", type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        user = json.loads(get_jwt_identity())

        receiver_id = data["receiver_id"]
        sender_id = user["id"]
        message = data["message"]

        comment = ChatModel(sender_id, receiver_id, message)
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred list the chat."}, 500

        return {"message": "Create Comment success"}
