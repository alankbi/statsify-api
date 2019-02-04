from visualizer.page import Page
from visualizer import helpers


class Website:
    def __init__(self, root_page):
        self.root_page = root_page
        if root_page.html is not None:
            self.pages = {root_page.url: (root_page, 1)}
            self.text = ''
            self.total_word_count = 0

            self.outbound_links = set(root_page.outbound_links)

            self.traverse_all_pages()

            self.average_word_count = self.total_word_count / len(self.pages)
            self.key_phrases = helpers.get_key_phrases_from_text(self.text, max_length=3)

    def traverse_all_pages(self):
        remaining_pages = [self.root_page]

        while remaining_pages:
            page = remaining_pages.pop()

            self.text += page.text + '\n'
            self.total_word_count += page.word_count
            self.outbound_links.update(page.outbound_links)

            if page.subpages is not None:
                for link in page.subpages:
                    if link in self.pages:
                        self.pages[link] = (self.pages[link][0], self.pages[link][1] + page.subpages[link][1])
                    else:
                        self.pages[link] = (page.subpages[link][0], page.subpages[link][1])
                        remaining_pages.append(page.subpages[link][0])


def main():
    website = Website(Page('http://alanbi.com', generate_subpages=True))
    print(website.pages)
    print(website.text)
    print(website.total_word_count)
    print(website.average_word_count)
    print(website.outbound_links)
    print(website.key_phrases)


if __name__ == '__main__':
    main()
