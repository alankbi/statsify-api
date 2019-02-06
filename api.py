import flask
from flask import request, jsonify
from visualizer.page import Page
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
        return 'Please specify a url'

    page = Page(request.args['url'])
    return jsonify(page)


@app.route('/website', methods=['GET'])
def api_website():
    if 'url' not in request.args:
        return 'Please specify a url'

    website = Website(request.args['url'])
    return jsonify(website)


app.run()
