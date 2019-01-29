from visualizer import helpers


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


def test_relative_to_absolute_url_from_subfolder():
    url = 'http://test.com/page1/'

    assert helpers.relative_to_absolute_url('page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('./page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('../page2', url) == 'http://test.com/page2'



