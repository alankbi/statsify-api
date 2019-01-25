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

print(is_http_url('http://test.com'))
print(is_http_url('https://test.com'))
print(is_http_url('test'))
print(is_http_url('/test'))
print(is_http_url('tel:+1-000-000-0000'))
print(is_http_url('file://testing'))
print(is_http_url('mailto:email@email.com'))

print(is_outbound_url('http://test.com', website))
print(is_outbound_url('https://test.com', website))
print(is_outbound_url('test', website))
print(is_outbound_url('/test', website))
print(is_outbound_url('http://alanbi.com', website))
