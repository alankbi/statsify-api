from visualizer import crawl


class Page:
    def __init__(self, url, generate_subpages=False, generate_depth=1):
        self.url = url
        self.html = crawl.get_html(url)

        if not generate_subpages or generate_depth <= 0:
            self.subpages = None
        else:
            self.subpages = {}
            if self.html is not None:
                for link in crawl.get_internal_links(self.html, url):
                    if link not in self.subpages:
                        subpage = Page(link, generate_subpages, generate_depth - 1)
                        if subpage.html is not None:
                            self.subpages[link] = (subpage, 1)
                    else:
                        self.subpages[link] = (self.subpages[link][0], self.subpages[link][1] + 1)

    def __str__(self):
        if self.html is None:
            return ''
        return self.html.prettify()

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


website = 'http://alanbi.com'
root_page = Page(website, True)
print(root_page.subpages)
for link in root_page.subpages:
    print(root_page.subpages[link][0].url + ' ' + str(root_page.subpages[link][1]))

