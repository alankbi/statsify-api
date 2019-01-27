from visualizer import helpers


def test_is_http_url():
    assert helpers.is_http_url('http://test.com')
    assert helpers.is_http_url('https://test.com')
    assert helpers.is_http_url('test')
    assert helpers.is_http_url('/test')
    assert helpers.is_http_url('./test:colon')
    assert not helpers.is_http_url('test:colon')
    assert not helpers.is_http_url('tel:+1-000-000-0000')
    assert not helpers.is_http_url('file://testing')
    assert not helpers.is_http_url('mailto:email@email.com')


def test_is_outbound_url():
    website = 'http://alanbi.com'

    assert helpers.is_outbound_url('http://test.com', website)
    assert helpers.is_outbound_url('https://test.com', website)
    assert not helpers.is_outbound_url('test', website)
    assert not helpers.is_outbound_url('/test', website)
    assert not helpers.is_outbound_url('http://alanbi.com', website)
    assert not helpers.is_outbound_url('https://alanbi.com', website)
    assert not helpers.is_outbound_url('#', website)
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

    url = 'http://test.com/page1/'

    assert helpers.relative_to_absolute_url('page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('./page2', url) == 'http://test.com/page1/page2'
    assert helpers.relative_to_absolute_url('../page2', url) == 'http://test.com/page2'



