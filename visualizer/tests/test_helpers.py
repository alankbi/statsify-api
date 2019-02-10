from visualizer import helpers
from bs4 import BeautifulSoup


def test_is_http_url_returns_true():
    assert helpers.is_http_url('http://test.com')
    assert helpers.is_http_url('https://test.com')
    assert helpers.is_http_url('test')
    assert helpers.is_http_url('/test')
    assert helpers.is_http_url('./test:colon')


def test_is_http_url_returns_false():
    assert not helpers.is_http_url('test:colon')
    assert not helpers.is_http_url('tel:+1-000-000-0000')
    assert not helpers.is_http_url('file://testing')
    assert not helpers.is_http_url('mailto:email@email.com')


def test_is_outbound_url_returns_true():
    website = 'http://alanbi.com'

    assert helpers.is_outbound_url('http://test.com', website)
    assert helpers.is_outbound_url('https://test.com', website)


def test_is_outbound_url_returns_false():
    website = 'http://alanbi.com'

    assert not helpers.is_outbound_url('test', website)
    assert not helpers.is_outbound_url('/test', website)
    assert not helpers.is_outbound_url('http://alanbi.com', website)
    assert not helpers.is_outbound_url('https://alanbi.com', website)
    assert not helpers.is_outbound_url('#', website)
    assert not helpers.is_outbound_url('', website)


def test_is_outbound_url_from_subfolder():
    website = 'http://alanbi.com/test'

    assert helpers.is_outbound_url('http://test.com', website)
    assert not helpers.is_outbound_url('https://alanbi.com', website)
    assert not helpers.is_outbound_url('https://alanbi.com/testing', website)
    assert not helpers.is_outbound_url('/test', website)
    assert not helpers.is_outbound_url('', website)


def test_relative_to_absolute_url():
    domain = 'http://test.com'

    assert helpers.relative_to_absolute_url('http://test.com', domain) == 'http://test.com'
    assert helpers.relative_to_absolute_url('https://test.com', domain) == 'https://test.com'
    assert helpers.relative_to_absolute_url('/page', domain) == 'http://test.com/page'
    assert helpers.relative_to_absolute_url('page', domain) == 'http://test.com/page'
    assert helpers.relative_to_absolute_url('', domain) == 'http://test.com'

    domain += '/'

    assert helpers.relative_to_absolute_url('page', domain) == 'http://test.com/page'
    assert helpers.relative_to_absolute_url('/page/', domain) == 'http://test.com/page/'

    domain = 'test.com'

    assert helpers.relative_to_absolute_url('page', domain) == 'http://test.com/page'


def test_relative_to_absolute_url_from_subfolder():
    url = 'http://test.com/page1/'

    assert helpers.relative_to_absolute_url('page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('./page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('../page2', url) == 'http://test.com/page2'


def test_strip_scripts_from_html():
    html = BeautifulSoup('<p>Hello</p><script>console.log("test");</script><p>Hi</p>', 'html.parser')

    helpers.strip_scripts_from_html(html)
    assert html.get_text('\n', strip=True) == 'Hello\nHi'


def test_filter_key_phrases():
    phrases = ['test', 'test this2', '3test', 'test4']
    result = helpers.filter_key_phrases(phrases)
    assert len(result) == 3
    assert result == ['Test', 'Test This2', '3Test']


def test_get_key_phrases_from_text():
    html = BeautifulSoup('<p>crawl and is crawl the helpers or website</p>', 'html.parser')

    key_phrases = helpers.get_key_phrases_from_text(html.get_text('\n', strip=True))
    assert key_phrases is not None
    assert len(key_phrases) == 3
    assert all(word in key_phrases for word in ['Crawl', 'Helpers', 'Website'])


def test_get_word_count_from_text():
    html = BeautifulSoup('<p>word1 word2 word3  word4</p><br><p>word5  6</p>', 'html.parser')

    word_count = helpers.get_word_count_from_text(html.get_text('\n', strip=True))
    assert word_count == 6


def test_url_open_mock():
    mock = helpers.UrlOpenMock('http://test.com')
    assert mock.text == 'User-agent: *\nAllow: /'
    assert mock.read() == 'User-agent: *\nAllow: /'.encode()

    mock = helpers.UrlOpenMock('any.url', text='User-agent: *\nDisallow: /')
    assert mock.text == 'User-agent: *\nDisallow: /'
    assert mock.read() == 'User-agent: *\nDisallow: /'.encode()
