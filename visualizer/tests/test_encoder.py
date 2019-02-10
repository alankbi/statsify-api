import json
import responses

from visualizer.encoder import CustomEncoder
from visualizer import helpers
from visualizer.page import Page, PageNode
from visualizer.website import Website
from urllib import request


@responses.activate
def test_page_encoder():
    responses.add(responses.GET, 'http://badurl.com', body='')
    result = json.dumps(Page('http://badurl.com'), cls=CustomEncoder)
    assert result == '{"error": "' + helpers.ERROR_MESSAGES[1] + '"}'

    responses.add(responses.GET, 'http://test.com', content_type='text/html', body='<p>hi</p>')
    result = json.dumps(Page('http://test.com'), cls=CustomEncoder)
    expected = {
        'url': 'http://test.com',
        'text': 'hi',
        'key_phrases': ['Hi'],
        'word_count': 1,
        'internal_links': [],
        'outbound_links': [],
    }
    assert result == json.dumps(expected)


@responses.activate
def test_page_node_encoder():
    responses.add(responses.GET, 'http://test.com', content_type='text/html', body='<p>hi</p>')
    result = json.dumps(PageNode(Page('http://test.com'), 1), cls=CustomEncoder)
    expected = {
        'page': {
            'url': 'http://test.com',
            'text': 'hi',
            'key_phrases': ['Hi'],
            'word_count': 1,
            'internal_links': [],
            'outbound_links': [],
        },
        'subpages': {}
    }
    assert result == json.dumps(expected)


@responses.activate
def test_website_encoder():
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)
    request.urlopen = lambda url: helpers.UrlOpenMock(url, text='User-agent: *\nDisallow: /')
    result = json.dumps(Website('http://test.com'), cls=CustomEncoder)
    assert result == '{"error": "' + helpers.ERROR_MESSAGES[0] + '"}'

    responses.add(responses.GET, 'http://test2.com', content_type='text/html', body='<p>hi</p><a href=""></a>')
    result = json.dumps(Website('http://test2.com'), cls=CustomEncoder)
    page = {
        'url': 'http://test2.com',
        'text': 'hi',
        'key_phrases': ['Hi'],
        'word_count': 1,
        'internal_links': ['http://test2.com'],
        'outbound_links': [],
    }
    expected = {
        'pages': {
            'http://test2.com': {'page': page, 'freq': 1}
        },
        'total_word_count': 1,
        'average_word_count': 1.0,
        'outbound_links': [],
        'key_phrases': ['Hi'],
        # 'root_page_node': {
        #     'page': page,
        #     'subpages': {
        #         'http://test2.com': {
        #             'page_node': {'page': page, 'subpages': None},
        #             'freq': 1,
        #         }
        #     },
        # }
    }
    assert result == json.dumps(expected)


test_page_encoder()
test_website_encoder()