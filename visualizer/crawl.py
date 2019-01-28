import requests
from bs4 import BeautifulSoup
from visualizer import helpers


def get_html(url):
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        result = requests.get(url)
    except requests.exceptions.RequestException:
        return None

    if 'text/html' in result.headers['content-type']:
        return BeautifulSoup(result.content, 'html.parser')
    else:
        return None


def get_all_links(html):
    links = html.find_all('a')
    return [link['href'] for link in links]


def filter_for_internal_links(links, current_url):
    internal_links = []
    for link in links:
        if not helpers.is_http_url(link) or helpers.is_outbound_url(link, current_url):
            continue

        internal_links.append(helpers.relative_to_absolute_url(link, current_url))

    return internal_links


def get_internal_links(html, current_url):
    links = get_all_links(html)
    return filter_for_internal_links(links, current_url)
