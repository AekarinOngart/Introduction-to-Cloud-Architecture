#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
import os
import base64
from uuid import uuid4
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from itsdangerous import base64_encode
from app.models.user import UserModel
from app.util.encoder import AlchemyEncoder
import json
from app.util.logz import create_logger
import werkzeug


class User(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("password", type=str, required=True, help="This field cannot be left blank")

    def post(self):
        data = User.parser.parse_args()
        username = data["username"]
        password = data["password"]
        user = UserModel.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {"message": "Wrong username or password."}, 401
        access_token = create_access_token(identity=json.dumps({"id": str(user.id), "username": user.username, "display_name": user.display_name}))
        return jsonify(access_token=access_token)

    @jwt_required()  # Requires bearer token
    def get(self):
        identify = json.loads(get_jwt_identity())
        user = UserModel.find_by_id(str(identify["id"]))
        return user.json()


class UserRegister(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("display_name", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("username", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument("password", type=str, required=True, help="This field cannot be left blank")
        parser.add_argument(
            "display_image",
            type=werkzeug.datastructures.FileStorage,
            location="files",
        )
        data = parser.parse_args()

        image = data["display_image"]
        image_base64 = base64.b64encode(image.read()).decode("utf-8")
        _, filetype = os.path.splitext(image.filename)
        data["display_image"] = "data:image/" + filetype[1:] + ";base64," + image_base64

        if UserModel.find_by_username(data["username"]):
            return {"message": "UserModel has already been created, aborting."}, 400
        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred creating the user."}, 500
        return {"message": "user has been created successfully."}, 201
