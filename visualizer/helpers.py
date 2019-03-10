from urllib.parse import urljoin
from rake_nltk import Rake


def is_http_url(url):
    """
    Checks if url is in valid http format or is a relative url.

    :param url: the url to check.
    :type url: str
    :return: whether or not the url is an http url.
    :rtype: bool
    """

    return url.startswith('http') or (':' not in url or url.startswith('.'))


def is_outbound_url(url, domain):
    """
    Checks if a url falls outside the given domain.

    :param url: the url to check.
    :type url: str
    :param domain: the current domain.
    :type domain: str
    :return: whether or not the url is an outbound url.
    :rtype: bool
    """

    separator = '://'
    if separator in domain:
        domain = domain[domain.index(separator) + len(separator):]
    if '/' in domain:
        domain = domain[:domain.index('/')]
    return url.startswith('http') and domain not in url


def relative_to_absolute_url(url, current_url):
    """
    Changes a relative url into a full http url.

    :param url: a relative url.
    :type url: str
    :param current_url: the domain the relative url belongs to.
    :type current_url: str
    :return: the relative url converted into a full http url.
    :rtype: str
    """

    if not current_url.startswith('http'):
        current_url = 'http://' + current_url
    return urljoin(current_url, url)


def strip_scripts_from_html(html):
    """
    Remove scripts from an html page.

    :param html: a BeautifulSoup object representing an html page.
    :type html: BeautifulSoup
    """

    for script in html(['script', 'style']):
        script.decompose()


def filter_key_phrases(phrases):
    """
    Filters through and formats a list of key phrases.

    :param phrases: a list of the key phrases.
    :type phrases: list of str
    :return: a list of key phrases (max len 3) with all elements in title form.
    :rtype: list of str
    """

    return [phrase.title() for phrase in phrases[:3]]


def get_key_phrases_from_text(text, max_length=None):
    """
    Find key phrases within an html page.

    :param text: the text from an html page.
    :type text: str
    :param max_length: the max length of each key phrase.
    :type max_length: int or None
    :return: a list of all key phrases within the text.
    :rtype: list of str
    """

    if max_length is not None:
        r = Rake(max_length=max_length)
    else:
        r = Rake()
    r.extract_keywords_from_text(text)
    return filter_key_phrases(r.get_ranked_phrases())


def get_word_count_from_text(text):
    """Returns the word count of a string containing an html page's text."""

    return len(text.split())


class UrlOpenMock:
    def __init__(self, url, text='User-agent: *\nAllow: /'):
        """
        Creates a mock object that replaces urllib's request.urlopen's return object.
        Used to mock a robots.txt file for unit testing.

        :param url: the url meant to be requested.
        :type url: str
        :param text: the contents of a mock robots.txt file for user agent '*'.
        :type text: str
        """

        self.url = url
        self.text = text

    def read(self):
        """Returns the mock robots.txt text encoded."""

        return self.text.encode()


# Common error messages
ERROR_MESSAGES = ['Robots are restricted from accessing this page. ',
                  'An error occurred when trying to reach this url. ',
                  'Please specify a url. ',
                  'Rate limit exceeded. ',
                  'An internal server error occurred. Please try again later. ']
