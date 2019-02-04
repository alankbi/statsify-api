from visualizer import crawl
from visualizer import helpers


class Page:
    def __init__(self, url):
        self.url = url
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
        return self.html.prettify()


class PageNode:
    def __init__(self, page, generate_depth=0, page_store={}):
        self.page = page
        if generate_depth <= 0 or self.page.html is None:
            self.subpages = None
        else:
            self.subpages = self.generate_subpages(generate_depth - 1, page_store)

    def generate_subpages(self, generate_depth, page_store):
        subpages = {}
        for link in self.page.internal_links:
            if link not in subpages:
                if link not in page_store:
                    page = Page(link)
                    page_store[link] = page

                if page_store[link].html is not None:
                    subpage = PageNode(page_store[link], generate_depth, page_store)
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
