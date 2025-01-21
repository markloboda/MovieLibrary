from flask import Flask, request, jsonify, abort, make_response
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import logging
import os
import jwt
from models import db, UserModel, UserSchema, UserAlreadyExistsException, InvalidCredentialsException

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["API_TITLE"] = "LoginRegisterService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting LoginRegisterService")

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
            abort(409, description=str(e))
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
            abort(401, description=str(e))
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')

        response = make_response({'message': 'Login successful'}, 200)
        response.set_cookie('jwt', token, httponly=True, secure=False, samesite='strict')
        
        return response

@blp.route("/check-token", methods=["GET"])
class CheckToken(MethodView):
    @blp.response(200)
    @blp.response(401)
    def get(self):
        logger.debug(f"Get on /check-token:\nheaders {request.headers}, cookies {request.cookies}")
        token = request.cookies.get('jwt')
        if not token:
            abort(401, description="Token is missing")

        try:
            decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded_token['user_id']
            user = UserModel.query.get(user_id)
            if not user:
                abort(401, description="Invalid token")
            return {"user_id": user.id, "email": user.email}, 200
        except jwt.ExpiredSignatureError:
            abort(401, description="Token has expired")
        except jwt.InvalidTokenError:
            abort(401, description="Invalid token")

@app.errorhandler(401)
def custom_401(error):
    response = jsonify({"message": error.description})
    response.status_code = 401
    return response

app.register_blueprint(blp)

if __name__ == '__main__':
    logger.debug("Starting LoginRegisterService")
    app.run(host='0.0.0.0', port=8080, debug=True)