from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.resources.user import UserRegister, User
from app.resources.post import Post, PostList, LikePost
from app.resources.comment import Comment, LikeComment
from app.resources.chat import Chat, ChatList
from app.resources.product import Product
from app.resources.image import Image
from app.config import postgresqlConfig
from app.resources.cart import Cart
from flask_cors import CORS


app = Flask(__name__)

UPLOAD_FOLDER = "./image"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app.config["SQLALCHEMY_DATABASE_URI"] = postgresqlConfig
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Setup the Flask-JWT-Extended extension
# Change this!
app.config["JWT_SECRET_KEY"] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
api = Api(app)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_first_request
def create_tables():
    from app.db import db

    db.init_app(app)
    db.create_all()


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user")
api.add_resource(Post, "/post")
api.add_resource(PostList, "/post_list")
api.add_resource(LikePost, "/like_post")
api.add_resource(Comment, "/comment")
api.add_resource(LikeComment, "/like_comment")
api.add_resource(Chat, "/chat")
api.add_resource(ChatList, "/chat_list")
api.add_resource(Cart, "/cart")
api.add_resource(Product, "/product")
api.add_resource(Image, "/image/<filename>")

if __name__ == "__main__":
    # TODO: Add swagger integration
    app.run(debug=True)  # important to mention debug=True
