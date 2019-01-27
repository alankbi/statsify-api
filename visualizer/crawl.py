import requests
from bs4 import BeautifulSoup
from visualizer import helpers


def get_all_links(url):

    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    links = soup.find_all('a')

    return [link['href'] for link in links]


def get_internal_links(links, current_url):
    internal_links = []
    for link in links:
        if not helpers.is_http_url(link) or helpers.is_outbound_url(link, current_url):
            continue

        internal_links.append(helpers.relative_to_absolute_url(link, current_url))

    return internal_links


website = 'http://alanbi.com'
all_links = get_all_links(website)
internal_links = get_internal_links(all_links, website)
print(internal_links)


