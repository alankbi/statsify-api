from visualizer import crawl
import responses


@responses.activate
def test_get_all_links():
    responses.add(responses.GET, 'http://test.com',
                  body='<div class="test"><a href="/test">hi</a></div>')

    links = crawl.get_all_links('http://test.com')
    assert len(links) == 1

    links = crawl.get_all_links('test.com')
    assert len(links) == 1


def test_filter_internal_links():
    current_url = 'http://test.com'
    links = ['http://test.com', 'https://test.com/test', 'http://wrong.com',
             'mailto:test@test.com', 'test', '/test', '#', '']
    result = ['http://test.com', 'https://test.com/test', 'http://test.com/test',
              'http://test.com/test', 'http://test.com', 'http://test.com']
    assert crawl.get_internal_links(links, current_url) == result
