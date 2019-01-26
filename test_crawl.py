import crawl


def test_is_http_url():
    assert crawl.is_http_url('http://test.com')
    assert crawl.is_http_url('https://test.com')
    assert crawl.is_http_url('test')
    assert crawl.is_http_url('/test')
    assert not crawl.is_http_url('tel:+1-000-000-0000')
    assert not crawl.is_http_url('file://testing')
    assert not crawl.is_http_url('mailto:email@email.com')


def test_is_outbound_url():
    website = 'http://alanbi.com'

    assert crawl.is_outbound_url('http://test.com', website)
    assert crawl.is_outbound_url('https://test.com', website)
    assert not crawl.is_outbound_url('test', website)
    assert not crawl.is_outbound_url('/test', website)
    assert not crawl.is_outbound_url('http://alanbi.com', website)


def test_relative_to_absolute_url():
    domain = 'http://test.com'

    assert crawl.relative_to_absolute_url('http://test.com', domain) == 'http://test.com'
    assert crawl.relative_to_absolute_url('https://test.com', domain) == 'https://test.com'
    assert crawl.relative_to_absolute_url('/page', domain) == 'http://test.com/page'
    assert crawl.relative_to_absolute_url('page', domain) == 'http://test.com/page'
    assert crawl.relative_to_absolute_url('', domain) == 'http://test.com/'

    domain += '/'

    assert crawl.relative_to_absolute_url('page', domain) == 'http://test.com/page'
    assert crawl.relative_to_absolute_url('/page', domain) == 'http://test.com//page'

    url = 'http://test.com/page1'

    assert crawl.relative_to_absolute_url('page2', url) == 'http://test.com/page1/page2'
    assert crawl.relative_to_absolute_url('./page2', url) == 'http://test.com/page1/page2'
    assert crawl.relative_to_absolute_url('../page2', url) == 'http://test.com/page2'



