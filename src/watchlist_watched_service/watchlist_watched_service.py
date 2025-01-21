from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, Api, abort
from flask_cors import CORS
import jwt
from models import db, Movie, WatchlistEntry, WatchedEntry, MovieSchema, WatchlistEntrySchema, WatchedEntrySchema

app = Flask(__name__)
CORS(app)

app.config["API_TITLE"] = "LoginRegisterService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlist_watched.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'  #TODO:Change this to the same secret key as login_register_service

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

blp = Blueprint('WatchlistWatched', 'watchlist_watched', description='Operations on watchlist and watched list')

def get_user_id_from_token():
    token = request.headers.get('Authorization')
    if not token:
        abort(401, message="Token is missing")
    try:
        data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        abort(401, message="Token has expired")
    except jwt.InvalidTokenError:
        abort(401, message="Invalid token")

class Watchlist(MethodView):
    def post(self):
        user_id = get_user_id_from_token()
        data = request.get_json()
        movie_data = data.get('movie')

        if not movie_data:
            abort(400, message="Movie data is required")

        movie = Movie.query.filter_by(imdb_id=movie_data['imdb_id']).first()
        if not movie:
            movie = Movie(
                title=movie_data['title'],
                year=movie_data.get('year'),
                imdb_id=movie_data['imdb_id'],
                poster=movie_data.get('poster')
            )
            db.session.add(movie)
            db.session.commit()

        watchlist_entry = WatchlistEntry(user_id=user_id, movie_id=movie.id)
        db.session.add(watchlist_entry)
        db.session.commit()

        return jsonify(WatchlistEntrySchema().dump(watchlist_entry)), 201

    def get(self):
        user_id = get_user_id_from_token()
        watchlist_entries = WatchlistEntry.query.filter_by(user_id=user_id).all()
        return jsonify(WatchlistEntrySchema(many=True).dump(watchlist_entries)), 200

class Watched(MethodView):
    def post(self):
        user_id = get_user_id_from_token()
        data = request.get_json()
        movie_data = data.get('movie')

        if not movie_data:
            abort(400, message="Movie data is required")

        movie = Movie.query.filter_by(imdb_id=movie_data['imdb_id']).first()
        if not movie:
            movie = Movie(
                title=movie_data['title'],
                year=movie_data.get('year'),
                imdb_id=movie_data['imdb_id'],
                poster=movie_data.get('poster')
            )
            db.session.add(movie)
            db.session.commit()

        watched_entry = WatchedEntry(user_id=user_id, movie_id=movie.id)
        db.session.add(watched_entry)
        db.session.commit()

        return jsonify(WatchedEntrySchema().dump(watched_entry)), 201

    def get(self):
        user_id = get_user_id_from_token()
        watched_entries = WatchedEntry.query.filter_by(user_id=user_id).all()
        return jsonify(WatchedEntrySchema(many=True).dump(watched_entries)), 200

class MovieView(MethodView):
    def post(self):
        data = request.get_json()
        movie_data = data.get('movie')

        if not movie_data:
            abort(400, message="Movie data is required")

        movie = Movie.query.filter_by(imdb_id=movie_data['imdb_id']).first()
        if movie:
            abort(400, message="Movie already exists")

        movie = Movie(
            title=movie_data['title'],
            year=movie_data.get('year'),
            imdb_id=movie_data['imdb_id'],
            poster=movie_data.get('poster')
        )
        db.session.add(movie)
        db.session.commit()

        return jsonify(MovieSchema().dump(movie)), 201

blp.add_url_rule('/watchlist', view_func=Watchlist.as_view('watchlist_post'), methods=['POST'])
blp.add_url_rule('/watchlist', view_func=Watchlist.as_view('watchlist_get'), methods=['GET'])
blp.add_url_rule('/watched', view_func=Watched.as_view('watched_post'), methods=['POST'])
blp.add_url_rule('/watched', view_func=Watched.as_view('watched_get'), methods=['GET'])
blp.add_url_rule('/movies', view_func=MovieView.as_view('movie_post'), methods=['POST'])

app.register_blueprint(blp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)