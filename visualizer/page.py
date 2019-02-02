from visualizer import crawl
from visualizer import helpers


class Page:
    def __init__(self, url, generate_subpages=False, generate_depth=1):
        self.url = url
        self.html = crawl.get_html(url)

        if self.html is not None:
            helpers.strip_scripts_from_html(self.html)
            self.text = self.html.get_text('\n', strip=True)
            self.key_phrases = helpers.get_key_phrases_from_text(self.text, max_length=3)

            self.word_count = helpers.get_word_count_from_text(self.text)

            self.internal_links, self.outbound_links = crawl.get_internal_and_outbound_links(self.html, url)

            if not generate_subpages or generate_depth <= 0:
                self.subpages = None
            else:
                self.subpages = self.generate_subpages(generate_depth - 1)

    def generate_subpages(self, generate_depth):
        subpages = {}
        for link in self.internal_links:
            if link not in subpages:
                subpage = Page(link, True, generate_depth)
                if subpage.html is not None:
                    subpages[link] = (subpage, 1)
            else:
                subpages[link] = (subpages[link][0], subpages[link][1] + 1)

        return subpages

    def __str__(self):
        if self.html is None:
            return ''
        return self.html.prettify()

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


def main():
    website = 'http://alanbi.com'
    root_page = Page(website)
    print(root_page)
    print(root_page.text)

    print(root_page.key_phrases)

    print(root_page.word_count)

    print(root_page.internal_links)
    print(root_page.outbound_links)


if __name__ == '__main__':
    main()
