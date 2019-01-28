from bs4 import BeautifulSoup
from visualizer import crawl
import responses


@responses.activate
def test_get_html():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    html = crawl.get_html('http://test.com')
    assert isinstance(html, BeautifulSoup)
    assert html.get_text() == 'hi'

    html = crawl.get_html('test.com')
    assert isinstance(html, BeautifulSoup)
    assert html.get_text() == 'hi'

    html = crawl.get_html('http://badurl.com')
    assert html is None


def test_get_all_links():
    html = BeautifulSoup('<a href="/test">hi</a>', 'html.parser')

    links = crawl.get_all_links(html)
    assert len(links) == 1
    assert links[0] == '/test'


def test_filter_for_internal_links():
    current_url = 'http://test.com'
    links = ['http://test.com', 'https://test.com/test', 'http://wrong.com',
             'mailto:test@test.com', 'test', '/test', '#', '']
    result = ['http://test.com', 'https://test.com/test', 'http://test.com/test',
              'http://test.com/test', 'http://test.com', 'http://test.com']
    assert crawl.filter_for_internal_links(links, current_url) == result

    current_url = 'http://test.com/test'
    links = ['http://test.com', 'https://test.com/test', 'http://wrong.com',
             'mailto:test@test.com', 'test', '/test', '#', '']
    result = ['http://test.com', 'https://test.com/test', 'http://test.com/test',
              'http://test.com/test', 'http://test.com/test', 'http://test.com/test']
    assert crawl.filter_for_internal_links(links, current_url) == result


def test_get_internal_links():
    html = BeautifulSoup('<a href="/test">hi</a><a href="http://wrong.com">hi</a>', 'html.parser')
    current_url = 'http://test.com'

    internal_links = crawl.get_internal_links(html, current_url)
    assert len(internal_links) == 1
    assert internal_links[0] == 'http://test.com/test'
