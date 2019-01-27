import requests
from bs4 import BeautifulSoup
import helpers


website = 'http://alanbi.com'

result = requests.get(website)
soup = BeautifulSoup(result.content, 'html.parser')

links = soup.find_all('a')

# Gets all links to different pages in same domain
for link in links:
    url = link['href']
    if not helpers.is_http_url(url) or helpers.is_outbound_url(url, website):
        continue

    url = helpers.relative_to_absolute_url(url, website)

    print(url)
