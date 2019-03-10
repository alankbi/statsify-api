import time

from bs4 import BeautifulSoup
from visualizer import crawl
from visualizer import helpers


class Page:
    def __init__(self, url, rp=None, is_other_page=False):
        """
        Creates a Page object to represent the contents of a single url. If
        the given url is valid and able to be requested, self.html contains
        the page's contents; otherwise, self.html is None and self.error
        describes what went wrong.

        :param url: the url to request.
        :type url: str
        :param rp: the robot parser to use for this url.
        :type rp: RobotParser or None
        :param is_other_page: whether to create an empty page object used to
            represent pages requested after the time limit has been exceeded.
        :type is_other_page: bool
        """

        self.url = url
        self.rp = rp
        if rp is not None and not self.can_fetch():
            self.html = None
            self.error = helpers.ERROR_MESSAGES[0]
            return

        if is_other_page:  # to represent all pages that weren't requested due to limits
            self.url = '*'
            self.rp = rp
            self.html = BeautifulSoup(features='html.parser')  # features set to ignore warning
            self.text = ''
            self.key_phrases = []
            self.word_count = 0
            self.internal_links = []
            self.outbound_links = []
            return

        self.html = crawl.get_html(url)

        if self.html is None:
            self.error = helpers.ERROR_MESSAGES[1]
        else:
            helpers.strip_scripts_from_html(self.html)
            self.text = self.html.get_text('\n', strip=True)
            self.key_phrases = helpers.get_key_phrases_from_text(self.text, max_length=3)

            self.word_count = helpers.get_word_count_from_text(self.text)

            self.internal_links, self.outbound_links = crawl.get_internal_and_outbound_links(self.html, url)

    def can_fetch(self):
        """
        Determines whether this Page's url can be fetched.

        :return: whether robots.txt allows this page to be requested.
        :rtype: bool
        """

        if self.url.startswith('http'):
            return self.rp.can_fetch('*', self.url)
        else:
            return self.rp.can_fetch('*', 'http://' + self.url)

    def __str__(self):
        return self.url


class PageNode:
    def __init__(self, page, generate_depth=0, page_store=None):
        """
        Creates a PageNode object to represent a Page object and any subpages it
        has. If the Page is valid and the recursive depth for generating subpages
        hasn't been exceeded, self.subpages will contain a list of Page subpages;
        otherwise, self.subpages will be None.

        :param page: the Page object this PageNode represents.
        :type page: Page
        :param generate_depth: the maximum recursive depth to follow a page's
            subpage links and generate Page objects for each url, and so on
            with each of those Pages' subpages.
        :type generate_depth: int
        :param page_store: a dictionary that maps previously created Page objects
            to their url keys, preventing duplicate requests to repeated urls.
        :type page_store: dict of str : Page or None
        """

        self.page = page
        if generate_depth <= 0 or self.page.html is None:
            self.subpages = None
        else:
            if page_store is None:
                page_store = {'*': Page('', is_other_page=True)}
            page_store[page.url] = page
            self.generate_all_subpages(generate_depth, page_store)

    def generate_all_subpages(self, generate_depth, page_store):
        """
        Starts the recursive generation of Page and PageNode objects with this
        object being the root PageNode. Stops requesting new urls after 25 seconds
        have passed and defaults to the '*' url to represent all remaining pages.

        :param generate_depth: the maximum recursive depth to generate subpages.
        :type generate_depth: int
        :param page_store: a dictionary that maps previously created Page objects
            to their url keys, preventing duplicate requests to repeated urls.
        :type page_store: dict of str : Page
        """

        start_time = time.time()
        finished = set('*')  # tracks if this page's subpages have already been generated previously
        pages = [self]
        next_pages = []  # all pages at the next depth to generate next
        for i in range(generate_depth):
            for page_node in pages:
                if page_node.page.url not in finished:
                    page_node.subpages = page_node.generate_subpages(page_store, start_time)
                    finished.add(page_node.page.url)
                    next_pages.extend(page_node.subpages[link]['page_node'] for link in page_node.subpages.keys())
                else:
                    page_node.subpages = None

            pages = next_pages
            next_pages = []

    def generate_subpages(self, page_store, start_time):
        """
        Generates subpages for just this PageNode. Stops requesting new urls if
        total elapsed time has passed 25 seconds or if over 100 unique urls have
        already been requested.

        :param page_store: a dictionary that maps previously created Page objects
            to their url keys, preventing duplicate requests to repeated urls.
        :type page_store: dict of str : Page
        :param start_time: the time at which subpages first started being generated
            under the root PageNode.
        :type start_time: float
        :return: a dictionary of subpage url keys mapping to another dictionary that
            contains the url's Page object mapped to the 'page' key and the frequency
            that the url appeared in its parent Page mapped to the 'freq' key.
        :rtype: dict of str : dict of str : (Page|int)
        """

        subpages = {}
        for link in self.page.internal_links:
            if link not in subpages:
                if link not in page_store:
                    # Stop after 100 requests or 25 seconds to prevent from taking too long
                    if time.time() - start_time > 25 or len(page_store) > 100:
                        if '*' not in subpages:
                            subpages['*'] = {
                                'page_node': PageNode(page_store['*'], page_store=page_store),
                                'freq': 0
                            }
                        subpages['*']['freq'] += 1
                        continue

                    else:
                        page = Page(link, self.page.rp)
                        page_store[link] = page

                if page_store[link].html is not None:
                    subpage = PageNode(page_store[link], page_store=page_store)
                    subpages[link] = {'page_node': subpage, 'freq': 1}

            else:
                subpages[link]['freq'] += 1

        return subpages

    def __str__(self):
        return self.page.url + '\n' + str(self.subpages)


def main():
    website = 'http://alanbi.com'
    page_node = PageNode(Page(website), 1)
    print(page_node)

    page = page_node.page
    print(page)
    print(page.text)

    print(page.key_phrases)

    print(page.word_count)

    print(page.internal_links)
    print(page.outbound_links)


if __name__ == '__main__':
    main()
