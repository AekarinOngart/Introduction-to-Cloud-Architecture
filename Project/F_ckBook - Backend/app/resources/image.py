#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask_restful import Resource, reqparse
from flask import send_file
from app.models.user import UserModel
from app.util.encoder import AlchemyEncoder
import json
from app.util.logz import create_logger


class Image(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self, filename):
        print(filename)
        return send_file("image/" + filename, mimetype="image/gif")
