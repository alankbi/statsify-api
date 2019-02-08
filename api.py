import flask

from flask import request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from visualizer import crawl
from visualizer.page import Page
from visualizer.helpers import ERROR_MESSAGES
from visualizer.website import Website
from visualizer.encoder import CustomEncoder

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = CustomEncoder
limiter = Limiter(app, key_func=get_remote_address)


@app.route('/', methods=['GET'])
def home():
    return '<h1>REST API</p>'


@app.route('/page', methods=['GET'])
@limiter.limit("100/day")
def api_page():
    if 'url' not in request.args:
        return jsonify({'error': ERROR_MESSAGES[2]})

    rp = crawl.get_robots_parser_if_exists(request.args['url'])

    page = Page(request.args['url'], rp)

    if page.html is None:
        return jsonify({'error': page.error})

    return jsonify({'data': page})


@app.route('/website', methods=['GET'])
@limiter.limit("1/day")
def api_website():
    if 'url' not in request.args:
        return jsonify({'error': ERROR_MESSAGES[2]})

    if 'depth' in request.args:
        depth = max(min(int(request.args['depth']), 8), 0)  # 0 <= depth <= 8
    else:
        depth = 1

    website = Website(request.args['url'], depth)

    if website.root.page.html is None:
        return jsonify({'error': website.root.page.error})

    return jsonify({'data': website})


@app.errorhandler(429)
def rate_limit_handler(e):
    return make_response(jsonify({'error': ERROR_MESSAGES[3] + e.description}))


app.run()