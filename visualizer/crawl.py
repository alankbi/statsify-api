import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
from visualizer import helpers


def get_html(url):
    """
    Gets html data from a url.

    :param url: the url to request.
    :type url: str
    :return: if the url request returns a valid html page, returns a BeautifulSoup
    object; otherwise, returns None
    :rtype: BeautifulSoup or None
    """

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
    """
    Attempts to parse the robots.txt file for a url.

    :param url: the url to request.
    :type url: str
    :return: a RobotFileParser object if a valid robots.txt is found; otherwise None.
    :rtype: RobotFileParser or None
    """

    if not url.startswith('http'):
        url = 'http://' + url

    parsed_url = urlparse(url)
    robot_path = '{url.scheme}://{url.netloc}/robots.txt'.format(url=parsed_url)

    try:
        r = requests.head(robot_path)
        if r.status_code < 300:
            rp = RobotFileParser()
            rp.set_url(robot_path)
            rp.read()
            return rp
        else:
            return None
    except RequestException:
        return None


def get_all_links(html):
    """
    Finds all links within an html page.

    :param html: a BeautifulSoup object that represents an html page.
    :type html: BeautifulSoup
    :return: a list of all the links in the page.
    :rtype: list of str
    """

    links = html.find_all('a', href=True)
    return [link['href'] for link in links]


def filter_for_internal_links(links, current_url):
    """
    Filters for only links that are from the same domain as the current url.

    :param links: a list of urls
    :type links: list of str
    :param current_url: the current url that links should be matched against.
    :type current_url: str
    :return: a list of all internal links
    :rtype: list of str
    """

    internal_links = []
    for link in links:
        if not helpers.is_http_url(link) or helpers.is_outbound_url(link, current_url):
            continue

        internal_links.append(helpers.relative_to_absolute_url(link, current_url))

    return internal_links


def filter_for_outbound_links(links, current_url):
    """
    Filters for only links that are from a different domain than the current url.

    :param links: a list of urls
    :type links: list of str
    :param current_url: the current url that links should be matched against.
    :type current_url: str
    :return: a list of all outbound links
    :rtype: list of str
    """

    return [link for link in links if not helpers.is_http_url(link) or
            helpers.is_outbound_url(link, current_url)]


def get_internal_and_outbound_links(html, current_url):
    """
    Filters the internal and outbound links from an html page.

    :param html: a BeautifulSoup object representing an html page.
    :type html: BeautifulSoup
    :param current_url: the current url that links should be matched against.
    :type current_url: str
    :return: a tuple of the lists for internal and outbound links.
    :rtype: (list of str, list of str)
    """

    links = get_all_links(html)
    return (filter_for_internal_links(links, current_url),
            filter_for_outbound_links(links, current_url))
