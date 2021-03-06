from visualizer.website import Website
from visualizer import helpers
from urllib import request
import responses
import pytest


@pytest.fixture
@responses.activate
def website():
    """
    pages: {
             'http://test.com/': (<Page object>, 2),
             'http://test.com/page1': (<Page object>, 4),
             'http://test.com/page2': (<Page object>, 2),
             'http://test.com/page3': (<Page object>, 1),
           }
    text: 1 2 3.\n\n6 7 8. 9 10 11. 12.\n4 5\n
    total_word_count: 12
    average_word_count: 3
    outbound_links: {'http://out.com', 'mailto:out@out.com'}
    key_phrases: Collection of numbers 1 - 12
    """

    urls = ['http://test.com/', 'http://test.com/page1',
            'http://test.com/page2', 'http://test.com/page3']
    bodies = ['<a href="/"></a><a href="/page1"></a><a href="/page2"></a><p>1 2 3.</p>',
              '<a href="/"></a><a href="/page1"></a><a href="/page2"></a><p>4 5</p>',
              '<a href="/page3"></a><a href="http://out.com"></a><a href="mailto:out@out.com"></a>',
              '<a href="/page1"></a><a href="/page1"></a><p>6 7 8. 9 10 11. 12.</p>']

    responses.add(responses.GET, urls[0], content_type='text/html', body=bodies[0])
    responses.add(responses.GET, urls[1], content_type='text/html', body=bodies[1])
    responses.add(responses.GET, urls[2], content_type='text/html', body=bodies[2])
    responses.add(responses.GET, urls[3], content_type='text/html', body=bodies[3])
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=404)

    return Website(urls[0], 3)


def test_website_pages(website):
    urls = ['http://test.com/', 'http://test.com/page1',
            'http://test.com/page2', 'http://test.com/page3']

    assert len(website.pages) == 4
    print(website.pages)
    assert urls[0] in website.pages and website.pages[urls[0]]['freq'] == 2
    assert urls[1] in website.pages and website.pages[urls[1]]['freq'] == 4
    assert urls[2] in website.pages and website.pages[urls[2]]['freq'] == 2
    assert urls[3] in website.pages and website.pages[urls[3]]['freq'] == 1


def test_website_text(website):
    # Order is flipped because pages are counted using a list as a stack
    assert website.text == '1 2 3.\n\n6 7 8. 9 10 11. 12.\n4 5\n'


def test_website_word_count(website):
    assert website.total_word_count == 12
    assert website.average_word_count == 3


def test_website_outbound_links(website):
    assert website.outbound_links == {'http://out.com', 'mailto:out@out.com'}


def test_website_key_phrases(website):
    assert len(website.key_phrases) == 3
    assert '9 10 11' in website.key_phrases


@responses.activate
def test_website_root_page_is_none():
    responses.add(responses.GET, 'http://test.com', body='')
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=404)

    website = Website('http://test.com')
    assert website.root.page.html is None
    assert hasattr(website, 'error')
    assert website.error == helpers.ERROR_MESSAGES[1]
    assert not hasattr(website, 'pages')


@responses.activate
def test_website_no_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<a href=""></a><a href="/test"></a><a href="http://out.com"></a><p>1 2 3</p>')
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=404)

    website = Website('http://test.com', 0)
    assert len(website.pages) == 1
    assert 'http://test.com' in website.pages and website.pages['http://test.com']['freq'] == 0
    assert website.text == '1 2 3\n'
    assert website.total_word_count == 3
    assert website.average_word_count == 3
    assert website.outbound_links == {'http://out.com'}
    assert '1 2 3' in website.key_phrases


@responses.activate
def test_website_robot_disallowed():
    responses.add(responses.GET, 'http://test.com', content_type='text/html', body='<p>hi</p>')
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)
    request.urlopen = lambda url: helpers.UrlOpenMock(url, text='User-agent: *\nDisallow: /')

    website = Website('http://test.com/', 2)
    assert website.root.page.html is None
    assert hasattr(website, 'error')
    assert website.error == helpers.ERROR_MESSAGES[0]
    assert website.root.subpages is None


@responses.activate
def test_website_some_pages_disallowed():
    responses.add(responses.GET, 'http://test.com/', content_type='text/html',
                  body='<a href="/test/"></a><a href="/test/test"></a>')
    responses.add(responses.GET, 'http://test.com/test/', content_type='text/html', body='<p>hi</p>')
    responses.add(responses.GET, 'http://test.com/test/test', content_type='text/html', body='<p>hi</p>')
    responses.add(responses.HEAD, 'http://test.com/robots.txt', status=200)

    request.urlopen = lambda url: helpers.UrlOpenMock(url, text='User-agent: *\nAllow: /test/test\nDisallow: /test')

    website = Website('http://test.com/')
    assert website.root.page.html is not None
    assert website.root.subpages is not None
    assert len(website.root.subpages) == 1
    assert 'http://test.com/test/test' in website.root.subpages
