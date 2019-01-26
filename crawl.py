import requests
from bs4 import BeautifulSoup


def is_http_url(url):
    return ':' not in url or url.startswith('http')


def is_outbound_url(url, domain):
    # TODO: check domain in url starting after the :// (need to then
    # validate that domain contains the http beginning part)
    return url.startswith('http') and domain not in url


def relative_to_absolute_url(url, domain):
    # TODO: needs to take into account things like ./ and ../
    # domain may need to be renamed since it's the current url not just domain
    if not url.startswith('http'):
        optional_slash = '' if domain.endswith('/') or url.startswith('/') else '/'
        return domain + optional_slash + url
    else:
        return url


website = 'http://alanbi.com'

result = requests.get(website)
soup = BeautifulSoup(result.content, 'html.parser')

links = soup.find_all('a')

# Gets all links to different pages in same domain
for link in links:
    url = link['href']
    if not is_http_url(url) or is_outbound_url(url, website):
        continue

    url = relative_to_absolute_url(url, website)

    print(url)
