import requests
from bs4 import BeautifulSoup


def is_http_url(url):
    return ':' not in url or url.startswith('http')


def is_outbound_url(url, website):
    return url.startswith('http') and website not in url


website = 'http://alanbi.com'

result = requests.get(website)
soup = BeautifulSoup(result.content, 'html.parser')

links = soup.find_all('a')

# Gets all links to different pages in same domain
for link in links:
    url = link['href']
    if not is_http_url(url) or is_outbound_url(url, website):
        continue

    if not url.startswith('http'):
        url = website + url
    print(url)
