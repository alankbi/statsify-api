from urllib.parse import urljoin
from rake_nltk import Rake


def is_http_url(url):
    return url.startswith('http') or (':' not in url or url.startswith('.'))


def is_outbound_url(url, domain):
    separator = '://'
    if separator in domain:
        domain = domain[domain.index(separator) + len(separator):]
    if '/' in domain:
        domain = domain[:domain.index('/')]
    return url.startswith('http') and domain not in url


def relative_to_absolute_url(url, current_url):
    return urljoin(current_url, url)


def strip_scripts_from_html(html):
    for script in html(['script', 'style']):
        script.decompose()


def filter_key_phrases(phrases):
    return [phrase.title() for phrase in phrases[:3]]


def get_key_phrases_from_text(text, max_length=None):
    if max_length is not None:
        r = Rake(max_length=max_length)
    else:
        r = Rake()
    r.extract_keywords_from_text(text)
    return filter_key_phrases(r.get_ranked_phrases())


def get_word_count_from_text(text):
    return len(text.split())
