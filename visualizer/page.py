from visualizer import crawl
from visualizer import helpers


class Page:
    def __init__(self, url, rp=None):
        self.url = url
        self.rp = rp
        if rp is not None and not rp.can_fetch('*', url):
            self.html = None
        else:
            self.html = crawl.get_html(url)

        if self.html is not None:
            helpers.strip_scripts_from_html(self.html)
            self.text = self.html.get_text('\n', strip=True)
            self.key_phrases = helpers.get_key_phrases_from_text(self.text, max_length=3)

            self.word_count = helpers.get_word_count_from_text(self.text)

            self.internal_links, self.outbound_links = crawl.get_internal_and_outbound_links(self.html, url)

    def __str__(self):
        if self.html is None:
            return ''
        return self.url


class PageNode:
    def __init__(self, page, generate_depth=0, page_store={}):
        self.page = page
        if generate_depth <= 0 or self.page.html is None:
            self.subpages = None
        else:
            page_store[page.url] = page
            self.generate_all_subpages(generate_depth, page_store)

    def generate_all_subpages(self, generate_depth, page_store):
        finished = set()    # tracks if this page's subpages have already been generated previously
        pages = [self]
        next_pages = []     # all pages at the next depth to generate next
        for i in range(generate_depth):
            for page_node in pages:
                if page_node.page.url not in finished:
                    page_node.subpages = page_node.generate_subpages(page_store)
                    finished.add(page_node.page.url)
                    next_pages.extend(page_node.subpages[link][0] for link in page_node.subpages.keys())
                else:
                    page_node.subpages = None

            pages = next_pages
            next_pages = []

    def generate_subpages(self, page_store):
        subpages = {}
        for link in self.page.internal_links:
            if link not in subpages:
                if link not in page_store:
                    page = Page(link, self.page.rp)
                    page_store[link] = page

                if page_store[link].html is not None:
                    subpage = PageNode(page_store[link], page_store=page_store)
                    subpages[link] = (subpage, 1)

            else:
                subpages[link] = (subpages[link][0], subpages[link][1] + 1)

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
