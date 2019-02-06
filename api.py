import flask
from flask import request
from visualizer.page import Page

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def home():
    return '<h1>REST API</p>'


@app.route('/page', methods=['GET'])
def api_page():
    if 'url' not in request.args:
        return 'Please specify a url'

    page = Page(request.args['url'])
    return page.url + ' ' + str(page.word_count)


app.run()
