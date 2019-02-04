from bs4 import BeautifulSoup
from visualizer import crawl
import responses


@responses.activate
def test_get_html_success():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    html = crawl.get_html('http://test.com')
    assert isinstance(html, BeautifulSoup)
    assert html.get_text() == 'hi'

    html = crawl.get_html('test.com')
    assert isinstance(html, BeautifulSoup)
    assert html.get_text() == 'hi'


@responses.activate
def test_get_html_failure():
    responses.add(responses.GET, 'http://badurl.com', body='')

    html = crawl.get_html('http://badurl.com')
    assert html is None


def test_get_all_links():
    html = BeautifulSoup('<a href="/test">hi</a><a class="no-href">hi</a>', 'html.parser')

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


def test_filter_for_internal_links_from_subfolder():
    current_url = 'http://test.com/test'
    links = ['http://test.com', 'https://test.com/test', 'http://wrong.com',
             'mailto:test@test.com', 'test', '/test', '#', '']
    result = ['http://test.com', 'https://test.com/test', 'http://test.com/test',
              'http://test.com/test', 'http://test.com/test', 'http://test.com/test']
    assert crawl.filter_for_internal_links(links, current_url) == result


def test_filter_for_outbound_links():
    current_url = 'http://test.com/test'
    links = ['http://test.com', 'https://test.com/test', 'http://outbound.com',
             'mailto:test@test.com', '/test', '', 'tel:+1-555-555-5555']
    result = ['http://outbound.com', 'mailto:test@test.com', 'tel:+1-555-555-5555']
    assert crawl.filter_for_outbound_links(links, current_url) == result


def test_get_internal_and_outbound_links():
    html = BeautifulSoup('<a href="/test">hi</a><a href="http://outbound.com">hi</a>', 'html.parser')
    current_url = 'http://test.com'

    internal_links, outbound_links = crawl.get_internal_and_outbound_links(html, current_url)
    assert len(internal_links) == 1
    assert internal_links[0] == 'http://test.com/test'

    assert len(outbound_links) == 1
    assert outbound_links[0] == 'http://outbound.com'
