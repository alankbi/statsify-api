from visualizer.page import Page, PageNode
from visualizer.helpers import UrlOpenMock
from visualizer import crawl
from urllib import request
import responses


@responses.activate
def test_page_with_bad_url():
    # For some reason body=Exception throws a TypeError in responses.py, so for
    # now body='', which produces the same result (crawl.get_html returns None)
    responses.add(responses.GET, 'http://badurl.com', body='')

    page = Page('http://badurl.com')
    assert page.html is None


@responses.activate
def test_page_text():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<p> hi </p><p>  hello  hello  </p><br><p>hey</p>')

    page = Page('http://test.com')
    assert page.text == 'hi\nhello  hello\nhey'


@responses.activate
def test_page_disallowed():
    responses.add(responses.GET, 'http://test.com/test', content_type='text/html', body='<p>hi</p>')
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)

    request.urlopen = lambda url: UrlOpenMock(url, text='User-agent: *\nAllow: /test/test\nDisallow: /test')
    rp = crawl.get_robots_parser_if_exists('http://test.com')

    page = Page('http://test.com/test', rp)
    assert page.rp is rp
    assert page.html is None


@responses.activate
def test_page_node_with_no_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    page = PageNode(Page('http://test.com'))
    assert page.subpages is None

    page = PageNode(Page('http://test.com'), generate_depth=-1)
    assert page.subpages is None


@responses.activate
def test_page_node_with_empty_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<p>hi</p>')

    page = PageNode(Page('http://test.com'), 2)
    assert page.subpages is not None
    assert not page.subpages


@responses.activate
def test_page_node_with_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<a href="">hi</a><a href="/test">hi1</a>'
                       '<a href="/test2">hi2</a><a href="/test">hi3</a>')
    responses.add(responses.GET, 'http://test.com/test', content_type='text/html',
                  body='<a href="/test">hi</a>')
    responses.add(responses.GET, 'http://test.com/test2', body='')

    page = PageNode(Page('http://test.com'), 1)
    assert page.subpages is not None
    assert len(page.subpages) == 2
    assert page.subpages['http://test.com'][1] == 1
    assert page.subpages['http://test.com/test'][1] == 2
    assert page.subpages['http://test.com'][0].subpages is None
    assert page.subpages['http://test.com/test'][0].subpages is None


@responses.activate
def test_page_node_with_subpages_two_deep():
    responses.add(responses.GET, 'http://test.com/test', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    page = PageNode(Page('http://test.com/test'), 2)
    key = 'http://test.com/test'
    assert page.subpages is not None
    assert len(page.subpages) == 1
    assert page.subpages[key][0].subpages is None
