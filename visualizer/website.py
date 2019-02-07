from visualizer.page import Page, PageNode
from visualizer import helpers
from visualizer import crawl


class Website:
    def __init__(self, url, generate_depth=1):
        rp = crawl.get_robots_parser_if_exists(url)
        self.root = PageNode(Page(url, rp), generate_depth=generate_depth)

        if self.root.page.html is None:
            self.error = self.root.page.error
        else:
            self.pages = {self.root.page.url: {'page': self.root.page, 'freq': 0}}
            self.text = ''
            self.total_word_count = 0

            self.outbound_links = set(self.root.page.outbound_links)

            self.traverse_all_pages()

            self.average_word_count = self.total_word_count / len(self.pages)
            self.key_phrases = helpers.get_key_phrases_from_text(self.text, max_length=3)

    def traverse_all_pages(self):
        remaining_pages = [self.root]

        while remaining_pages:
            page_node = remaining_pages.pop()
            page = page_node.page

            self.text += page.text + '\n'
            self.total_word_count += page.word_count
            self.outbound_links.update(page.outbound_links)

            if page_node.subpages is not None:
                for link in page_node.subpages:
                    if link in self.pages:
                        self.pages[link]['freq'] += page_node.subpages[link]['freq']
                    else:
                        self.pages[link] = {
                            'page': page_node.subpages[link]['page_node'].page,
                            'freq': page_node.subpages[link]['freq']
                        }
                        remaining_pages.append(page_node.subpages[link]['page_node'])


def main():
    website = Website('http://alanbi.com', 3)
    print(website.pages)
    print(website.text)
    print(website.total_word_count)
    print(website.average_word_count)
    print(website.outbound_links)
    print(website.key_phrases)
    print(len(website.pages))


if __name__ == '__main__':
    main()
