from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, Api, abort
from flask_cors import CORS
from hashlib import sha256
import logging
import jwt
import datetime

from models import db, UserSchema, UserModel, UserAlreadyExistsException, InvalidCredentialsException

app = Flask(__name__)
CORS(app)

app.config["API_TITLE"] = "LoginRegisterService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  # TODO: Change this to a secure key

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
    @blp.response(201, UserSchema)
    @blp.response(409)
    def post(self, user_data):
        logger.debug(f"Post on /register. Data: {user_data}")
        try:
            user = UserModel.add_user(user_data["email"], user_data["password"])
        except UserAlreadyExistsException as e:
            abort(409, message=str(e))
        return {"message": f"User {user.email} created."}, 201

@blp.route("/login", methods=["POST"])
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    @blp.response(401)
    def post(self, user_data):
        logger.debug(f"Post on /login. Data: {user_data}")
        try:
            user = UserModel.verify_user(user_data["email"], user_data["password"])
        except InvalidCredentialsException as e:
            abort(401, message=str(e))
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return {"token": token, "message": "Login successful."}, 200
    
@blp.route("/clearDB", methods=["POST"])
class ClearDatabase(MethodView):
    def post(self):
        db.drop_all()
        db.create_all()
        return {"message": "Database cleared and recreated."}, 200


app.register_blueprint(blp)

if __name__ == '__main__':
    logger.debug("Starting LoginRegisterService")
    app.run(host='0.0.0.0', port=5000, debug=True)