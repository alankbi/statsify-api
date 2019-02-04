from visualizer.page import Page, PageNode
import responses


@responses.activate
def test_page_with_bad_url():
    # For some reason body=Exception throws a TypeError in responses.py, so for
    # now body='', which produces the same result (crawl.get_html returns None)
    responses.add(responses.GET, 'http://badurl.com', body='')

    page = Page('http://badurl.com')
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
    assert page.subpages[key][0].subpages is not None
    assert len(page.subpages[key][0].subpages) == 1
    assert page.subpages[key][0].subpages[key][0].subpages is None
