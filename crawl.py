import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def is_http_url(url):
    return url.startswith('http') or (':' not in url or url.startswith('.'))


def is_outbound_url(url, domain):
    separator = '://'
    if separator in domain:
        domain = domain[domain.index(separator) + len(separator):]
    return url.startswith('http') and domain not in url


def relative_to_absolute_url(url, current_url):
    return urljoin(current_url, url)


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
