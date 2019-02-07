import requests
from requests.exceptions import RequestException
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
from visualizer import helpers


def get_html(url):
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        result = requests.get(url)
    except RequestException:
        return None

    if 'text/html' in result.headers['content-type'] and result.status_code < 400:
        return BeautifulSoup(result.content, 'html.parser')
    else:
        return None


def get_robots_parser_if_exists(url):
    if not url.startswith('http'):
        url = 'http://' + url
    if url.endswith('/'):
        url += 'robots.txt'
    else:
        url += '/robots.txt'
    try:
        r = requests.head(url)
        if r.status_code < 300:
            rp = RobotFileParser()
            rp.set_url(url)
            rp.read()
            return rp
        else:
            return None
    except RequestException:
        return None


def get_all_links(html):
    links = html.find_all('a', href=True)
    return [link['href'] for link in links]


def filter_for_internal_links(links, current_url):
    internal_links = []
    for link in links:
        if not helpers.is_http_url(link) or helpers.is_outbound_url(link, current_url):
            continue

        internal_links.append(helpers.relative_to_absolute_url(link, current_url))

    return internal_links


def filter_for_outbound_links(links, current_url):
    return [link for link in links if not helpers.is_http_url(link) or
            helpers.is_outbound_url(link, current_url)]


def get_internal_and_outbound_links(html, current_url):
    links = get_all_links(html)
    return (filter_for_internal_links(links, current_url),
            filter_for_outbound_links(links, current_url))
