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
