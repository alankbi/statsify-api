from visualizer import crawl


class Page:
    def __init__(self, url, generate_subpages=False, generate_depth=1):
        self.url = url
        self.html = crawl.get_html(url)

        if not generate_subpages or generate_depth <= 0:
            self.subpages = None
        else:
            self.subpages = []
            if self.html is not None:
                for link in crawl.get_internal_links(self.html, url):
                    self.subpages.append(Page(link, generate_subpages, generate_depth - 1))

    def __str__(self):
        if self.html is None:
            return ''
        return self.html.prettify()


website = 'http://alanbi.com'
root_page = Page(website, True)
for page in root_page.subpages:
    print(page.url)
    print(page)
