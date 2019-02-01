from visualizer.website import Page
import responses


@responses.activate
def test_page_with_bad_url():
    responses.add(responses.GET, 'http://badurl.com', body=Exception)

    page = Page('http://test.com')
    assert page.html is None


@responses.activate
def test_page_with_no_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    page = Page('http://test.com')
    assert page.subpages is None

    page = Page('http://test.com', generate_subpages=True, generate_depth=0)
    assert page.subpages is None


@responses.activate
def test_page_with_subpages():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<a href="">hi</a><a href="/test">hi1</a>'
                       '<a href="/test2">hi2</a><a href="/test">hi3</a>')
    responses.add(responses.GET, 'http://test.com/test', content_type='text/html',
                  body='<a href="/test">hi</a>')
    # For some reason body=Exception throws a TypeError in responses.py, so for
    # now body='', which produces the same result (crawl.get_html returns None)
    responses.add(responses.GET, 'http://test.com/test2', body='')

    page = Page('http://test.com', generate_subpages=True)
    assert page.subpages is not None
    print(page.subpages)
    assert len(page.subpages) == 2
    assert page.subpages['http://test.com'][1] == 1
    assert page.subpages['http://test.com/test'][1] == 2
    assert page.subpages['http://test.com'][0].subpages is None


@responses.activate
def test_page_with_subpages_two_deep():
    responses.add(responses.GET, 'http://test.com/test', content_type='text/html',
                  body='<div class="test"><a href="/test">hi</a></div>')

    page = Page('http://test.com/test', generate_subpages=True, generate_depth=2)
    key = 'http://test.com/test'
    assert page.subpages is not None
    assert len(page.subpages) == 1
    assert page.subpages[key][0].subpages is not None
    assert len(page.subpages[key][0].subpages) == 1
    assert page.subpages[key][0].subpages[key][0].subpages is None


@responses.activate
def test_strip_scripts_from_html():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<p>Hello</p><script>console.log("test");</script><p>Hi</p>')

    page = Page('http://test.com')
    assert page.html is not None
    assert page.text == 'Hello\nHi'


@responses.activate
def test_get_key_phrases():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<p>crawl and is crawl the helpers or website</p>')

    page = Page('http://test.com')
    assert page.html is not None
    key_phrases = page.get_key_phrases()
    assert key_phrases is not None
    assert len(key_phrases) == 3
    assert all(word in key_phrases for word in ['crawl', 'helpers', 'website'])


@responses.activate
def test_get_word_count():
    responses.add(responses.GET, 'http://test.com', content_type='text/html',
                  body='<p>word1 word2 word3  word4</p><br><p>word5  6</p>')

    page = Page('http://test.com')
    assert page.html is not None
    assert page.word_count == 6


def test_filter_key_phrases():
    phrases = ['test', 'test this2', '3test', 'test4']
    result = Page('').filter_key_phrases(phrases)
    assert len(result) == 3
    assert result == ['Test', 'Test This2', '3Test']
