from visualizer.page import Page


class Website:
    def __init__(self, root_page):
        self.root_page = root_page
        if root_page is not None:
            self.pages = {root_page.url: (root_page, 1)}
            self.text = root_page.text
            self.word_count = 0

            self.outbound_links = list(root_page.outbound_links)

            self.traverse_all_pages()


            self.key_phrases = None

    def traverse_all_pages(self):
        remaining_pages = [self.root_page]

        while remaining_pages:
            page = remaining_pages.pop()

            if page.subpages is not None:
                for link in page.subpages:
                    if link in self.pages:
                        self.pages[link] = (self.pages[link][0], self.pages[link][1] + page.subpages[link][1])
                    else:
                        self.pages[link] = (page.subpages[link][0], page.subpages[link][1])
                        remaining_pages.append(page.subpages[link][0])


website = Website(Page('http://alanbi.com', generate_subpages=True))
print(website.pages)
