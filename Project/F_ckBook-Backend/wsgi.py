from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@192.168.1.180:5432/admin'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#class User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    display_name = db.Column(db.String(128))
    display_image = db.Column(db.String(128))
    token = db.Column(db.String(128))
    create_time = db.Column(
        db.DateTime, default=datetime.utcnow)


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    sender_id = db.Column(UUID(as_uuid=True),
                          db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String)
    create_time = db.Column(
        db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.String(128))
    image = db.Column(db.String)
    like = db.Column(db.Integer)
    owner_post = db.Column(
        UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    create_time = db.Column(
        db.DateTime, default=datetime.utcnow)
    update_time = db.Column(
        db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    post_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('post.id'), nullable=False)
    owner_comment = db.Column(
        UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String)
    like = db.Column(db.Integer)
    create_time = db.Column(
        db.DateTime, default=datetime.utcnow)
    update_time = db.Column(
        db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.String(128))
    type = db.Column(db.String(128))
    sex = db.Column(db.String(128))
    color = db.Column(db.String(128))
    image = db.Column(db.String(128))


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    owner_cart = db.Column(
        UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    product = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('product.id'), nullable=False)
