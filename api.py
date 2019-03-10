import flask
import os

from flask import request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import flask_monitoringdashboard as dashboard

from visualizer import crawl
from visualizer.page import Page
from visualizer.helpers import ERROR_MESSAGES
from visualizer.website import Website
from visualizer.encoder import CustomEncoder

app = flask.Flask(__name__)
app.json_encoder = CustomEncoder
app.config['PROPAGATE_EXCEPTIONS'] = True
limiter = Limiter(app, key_func=get_remote_address)


def create_config_file():
    """Creates a config file for the API monitoring dashboard."""

    lines = ['[dashboard]',
             'APP_VERSION=1.0',
             '',
             '[authentication]',
             'USERNAME=admin',
             'PASSWORD=' + os.environ.get('STATSIFY_DASHBOARD_PASSWORD', 'admin'),
             '',
             '[visualization]',
             'TIMEZONE=America/Los_Angeles',
             '']

    db_path = os.environ.get('STATSIFY_DB_URL')
    if db_path is not None:
        lines.extend(['[database]',
                      'DATABASE=' + db_path])

    for i in range(len(lines)):
        lines[i] += '\n'

    f = open('config.cfg', 'w')
    f.writelines(lines)


create_config_file()
dashboard.config.init_from(file='./config.cfg')


# Does not seem to have any effect in the monitoring dashboard
def group_by_origin():
    """Group incoming requests by source: website, extension, or API."""

    if 'source' in request.args:
        return request.args['source']
    else:
        return 'api'


dashboard.config.group_by = group_by_origin
dashboard.bind(app)


@app.route('/', methods=['GET'])
def home():
    """Returns an html page with a link to https://www.statsify.us."""

    return '<html>' \
           '<head><link rel="shortcut icon" href="/favicon.ico"></head>' \
           '<body><a href="https://www.statsify.us"><h1 style="text-align: center; ' \
           'font-size: large; margin-top: 20px;">Statsify Home Page</h1></a></body>' \
           '</html>'


@app.route('/favicon.ico')
def favicon():
    """Returns the favicon used by the home page."""

    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')


@app.route('/page', methods=['GET'])
@limiter.limit("1000/day")
def api_page():
    """
    API endpoint for requesting page data. https://www.statsify.us/api

    :param url: The url to gather data from.
    :type url: str
    :return: If a successful request is made, the data will be returned in
        a JSON object under the 'data' key. Otherwise, a JSON object
        with an 'error' key will be returned.
    :rtype: object
    """

    if 'url' not in request.args:
        response = jsonify({'error': ERROR_MESSAGES[2]})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    rp = crawl.get_robots_parser_if_exists(request.args['url'])

    page = Page(request.args['url'], rp)

    if page.html is None:
        response = jsonify({'error': page.error})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    response = jsonify({'data': page})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/website', methods=['GET'])
@limiter.limit("200/day")
def api_website():
    """
    API endpoint for requesting website data. https://www.statsify.us/api

    :param url: The url to gather data from.
    :type url: str
    :param depth: The maximum recursive depth to follow internal links.
    :type depth: int
    :return: If a successful request is made, the data will be returned in
        a JSON object under the 'data' key. Otherwise, a JSON object
        with an 'error' key will be returned.
    :rtype: object
    """

    if 'url' not in request.args:
        response = jsonify({'error': ERROR_MESSAGES[2]})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if 'depth' in request.args:
        depth = max(min(int(request.args['depth']), 8), 0)  # 0 <= depth <= 8
    else:
        depth = 1

    website = Website(request.args['url'], depth)

    if website.root.page.html is None:
        response = jsonify({'error': website.root.page.error})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    response = jsonify({'data': website})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.errorhandler(404)
def page_not_found_handler(e):
    """JSON response for a 404 error."""

    response = jsonify({'error': e.description})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 404


@app.errorhandler(429)
def rate_limit_handler(e):
    """JSON response for exceeding the rate limit."""

    response = jsonify({'error': ERROR_MESSAGES[3] + e.description})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 429


@app.errorhandler(Exception)
def internal_error_handler(e):
    """JSON response that attempts to catch all other errors."""

    response = jsonify({'error': ERROR_MESSAGES[4]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
