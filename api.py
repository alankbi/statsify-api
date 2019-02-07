import flask
from flask import request, jsonify
from visualizer import crawl
from visualizer.page import Page
from visualizer.helpers import ERROR_MESSAGES
from visualizer.website import Website
from visualizer.encoder import CustomEncoder

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = CustomEncoder


@app.route('/', methods=['GET'])
def home():
    return '<h1>REST API</p>'


@app.route('/page', methods=['GET'])
def api_page():
    if 'url' not in request.args:
        return jsonify({'error': ERROR_MESSAGES[2]})

    rp = crawl.get_robots_parser_if_exists(request.args['url'])

    page = Page(request.args['url'], rp)

    if page.html is None:
        return jsonify({'error': page.error})

    return jsonify({'data': page})


@app.route('/website', methods=['GET'])
def api_website():
    if 'url' not in request.args:
        return jsonify({'error': ERROR_MESSAGES[2]})

    if 'depth' in request.args:
        depth = max(min(request.args['depth'], 8), 0)  # 0 <= depth <= 8
    else:
        depth = 1

    website = Website(request.args['url'], depth)

    if website.root.page.html is None:
        return jsonify({'error': website.root.page.error})

    return jsonify({'data': website})


app.run()
