from flask import Flask, request, abort, make_response, jsonify
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from marshmallow.exceptions import ValidationError
import logging
import os
import requests
import json
from models import db, WatchlistModel, WatchlistMovieSchema, WatchlistMovieIdSchema, WatchlistMovieAlreadyExistsException

# Setup app
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["API_TITLE"] = "LoginRegisterService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting WatchlistService")
db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)
blp = Blueprint("Watchlist", "watchlist", description="Operations on watchlists")

@blp.route("/service/watchlist/add-movie", methods=["POST"])
class AddMovie(MethodView):
    @blp.arguments(WatchlistMovieSchema)
    @blp.response(201, WatchlistMovieSchema)
    @blp.response(401)
    @blp.response(409)
    def post(self, movie_data):
        logger.debug(f"Post on /add-movie. Data: {movie_data}")
        try:
            jwt = request.cookies.get("jwt")
            if jwt is None:
                abort(401, description="Token is missing")
            token_response = requests.get("http://165.227.245.243/service/login-register/check-token", cookies={"jwt": jwt})
            logger.debug(f"Response from login-register: {token_response}")
            if token_response.status_code != 200:
                abort(401, description="Token is invalid")
            
            user_id = token_response.json()["user_id"]
                        
            movie = WatchlistModel.add_movie(
                user_id,
                movie_data["title"],
                movie_data["type"],
                movie_data["imdb_id"],
                movie_data["added_date"],
                year=movie_data["year"],
                poster=movie_data["poster"]
            )
        except WatchlistMovieAlreadyExistsException as e:
            abort(409, description=str(e))
        except ValidationError as e:
            abort(422, description=str(e))
            
        response = make_response({"message": f"Movie {movie.title} added to watchlist."}, 201)
        return response
    
@blp.route("/service/watchlist/remove-movie", methods=["POST"])
class RemoveMovie(MethodView):
    @blp.arguments(WatchlistMovieIdSchema)
    @blp.response(200)
    @blp.response(401)
    @blp.response(404)
    def post(self, movie_data):
        logger.debug(f"Post on /remove-movie. Data: {movie_data}")
        try:
            jwt = request.cookies.get("jwt")
            if jwt is None:
                abort(401, description="Token is missing")
            token_response = requests.get("http://165.227.245.243/service/login-register/check-token", cookies={"jwt": jwt})
            logger.debug(f"Response from login-register: {token_response}")
            if token_response.status_code != 200:
                abort(401, description="Token is invalid")
            
            user_id = token_response.json()["user_id"]
                        
            movie = WatchlistModel.remove_movie(user_id, movie_data["imdb_id"])
        except WatchlistMovieAlreadyExistsException as e:
            abort(409, description=str(e))
        except ValidationError as e:
            abort(422, description=str(e))
            
        response = make_response({"message": f"Movie {movie.title} removed from watchlist."}, 201)
        return response
    
@blp.route("/service/watchlist/get-movies", methods=["GET"])
class GetMovies(MethodView):
    @blp.response(200)
    @blp.response(401)
    def get(self):
        logger.debug(f"Get on /get-movies.")
        jwt = request.cookies.get("jwt")
        if jwt is None:
            logger.debug("Token is missing")
            abort(401, description="Token is missing")
        token_response = requests.get("http://165.227.245.243/service/login-register/check-token", cookies={"jwt": jwt})
        logger.debug(f"Response from login-register: {token_response}")
        if token_response.status_code != 200:
            logger.debug("Token is invalid")
            abort(401, description="Token is invalid")
            
        user_id = token_response.json()["user_id"]
        movies = [movie.serialize() for movie in WatchlistModel.get_movies(user_id)]
        logger.debug(f"Retrieved movies: {movies}")

        return make_response({"movies": movies}, 200)
    
@app.errorhandler(401)
def custom_401(error):
    response = make_response({"message": error.description}, 401)
    return response

@app.errorhandler(422)
def custom_422(error):
    response = make_response({"message": error.description}, 422)
    return response
        
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)