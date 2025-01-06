from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, Api, abort
from flask_cors import CORS
from hashlib import sha256
import logging

from models import db, UserSchema, UserModel

app = Flask(__name__)
CORS(app)

app.config["API_TITLE"] = "LoginRegisterService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register", methods=["POST"])
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        logger.debug(f"Received registration data: {user_data}")
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            email=user_data["email"],
            password=sha256(user_data["password"].encode('utf-8')).hexdigest()
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201

@blp.route("/login", methods=["POST"])
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        logger.debug(f"Received login data: {user_data}")
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        if not user or user.password != sha256(user_data["password"].encode('utf-8')).hexdigest():
            abort(401, message="Invalid credentials.")
        return {"message": "Login successful."}, 200


@blp.route("/users", methods=["GET"])
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

app.register_blueprint(blp)

if __name__ == '__main__':
    logger.debug("Starting LoginRegisterService")
    app.run(host='0.0.0.0', port=5000, debug=True)