import logging
import requests
import os
import threading
import etcd3
from flask import Flask, request, jsonify
from flask_smorest import Blueprint, Api, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["API_TITLE"] = "BrowseLibraryService"
app.config["API_VERSION"] = "v1"
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'

etcd = etcd3.client(host='etcd', port=2379)

def update_flask_debug():
    value, _ = etcd.get('/config/FLASK_DEBUG')
    debug_enabled = value.decode('utf-8').lower() in ['true', '1', 't'] if value else False
    app.config['DEBUG'] = debug_enabled
   
    if app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG, force = True)
    else:
        logging.basicConfig(level=logging.INFO, force = True)
    logger = logging.getLogger(__name__)
    logger.info(f"Setting logger to {'DEBUG' if debug_enabled else 'INFO'}")
    return logger

def watch_flask_debug():
    events, _ = etcd.watch('/config/FLASK_DEBUG')
    for _ in events:
        update_flask_debug()

threading.Thread(target=watch_flask_debug, daemon=True).start()

api = Api(app)
blp = Blueprint('Library', 'library', description='Operations on movies')
blp_health = Blueprint('Health', 'health', description='Health operations')

# Suppress werkzeug logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logger = update_flask_debug()
logger.debug("Starting BrowseLibraryService")

@blp.route('/service/browse-library/search', methods=['GET'])
@blp.response(200)
@blp.response(400)
@blp.response(500)
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

@blp_health.route('/service/browse-library/health/live', methods=['GET'])
@blp_health.response(503)
@blp_health.response(200)
def health_live():
    logger.debug(f"GET on /health/live.")
    api_key = os.getenv('API_KEY')
    if not api_key:
        abort(503, message="API key is not configured")
    
    ## TODO: Commented to avoid calling the API because of the rate limit.
    # request_string = f'http://www.omdbapi.com/?s=batman&apikey={api_key}'
    # response = requests.get(request_string)
    # if response.status_code != 200:
    #     abort(503, message="Error querying the movie API")
    
    return {"status": "UP"}, 200

@blp_health.route('/service/browse-library/health/api-key-demo', methods=['GET'])
@blp_health.response(200)
def health_demo():
    logger.debug(f"GET on /health/api-key-demo.")
    os.environ['API_KEY'] = ''
    return {"status": "API key removed"}, 200

    
@blp.route('/service/browse-library/openapi', methods=['GET'])
def send_openapi():
    data = api.spec.to_dict()
    return jsonify(data)

api.register_blueprint(blp)
api.register_blueprint(blp_health)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)