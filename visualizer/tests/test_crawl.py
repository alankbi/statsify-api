from bs4 import BeautifulSoup
from visualizer import crawl
from visualizer.helpers import UrlOpenMock
from urllib import request
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

    responses.add(responses.GET, 'http://test.com', status=404, content_type='text/html', body='<p>404</p>')

    html = crawl.get_html('http://test.com')
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


@responses.activate
def test_get_robots_parser_if_exists():
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)
    request.urlopen = lambda url: UrlOpenMock(url, text='User-agent: *\nAllow: /test\nDisallow: /')

    rp = crawl.get_robots_parser_if_exists('http://test.com/')
    assert rp.can_fetch('*', 'http://test.com/test')
    assert not rp.can_fetch('*', 'http://test.com')
    assert not rp.can_fetch('*', 'http://test.com/other')


@responses.activate
def test_get_robots_parser_if_does_not_exist():
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=404)
    request.urlopen = lambda url: UrlOpenMock(url)

    rp = crawl.get_robots_parser_if_exists('http://test.com')
    assert rp is None


@responses.activate
def test_get_robots_parser_not_from_root():
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)
    request.urlopen = lambda url: UrlOpenMock(url)

    rp = crawl.get_robots_parser_if_exists('http://test.com/test')
    assert rp is not None

    rp = crawl.get_robots_parser_if_exists('test.com/test/test1')
    assert rp is not None
