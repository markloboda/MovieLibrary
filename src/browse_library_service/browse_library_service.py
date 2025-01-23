from flask import Flask
from flask_smorest import Blueprint, Api, abort
from flask_cors import CORS
import logging
import requests
from flask import request, jsonify
import os

app = Flask(__name__)
CORS(app)

app.config["API_TITLE"] = "BrowseLibraryService"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']

# Configure logging
if app.config['DEBUG']:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.debug("Starting BrowseLibraryService")

api = Api(app)

blp = Blueprint('Library', 'library', description='Operations on movies')

@blp.route('/service/browse-library/search', methods=['GET'])
def search_movie():
    logger.debug(f"GET on /search.")
    title = request.args.get('title')
    logger.debug(f"Title: {title}")
    if not title:
        abort(400, message="Title parameter is required")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        abort(500, message="API key is not configured")
    request_string = f'http://www.omdbapi.com/?s={title}&apikey={api_key}'
    logger.debug("Requesting on /search:\n" + request_string)
    response = requests.get(request_string)
    if response.status_code != 200:
        abort(response.status_code, message="Error querying the movie API")
    
    return jsonify(response.json())

api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)