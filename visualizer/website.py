from visualizer import crawl
from rake_nltk import Rake


class Page:
    def __init__(self, url, generate_subpages=False, generate_depth=1):
        self.url = url
        self.html = crawl.get_html(url)

        if self.html is not None:
            self.strip_scripts_from_html()
            self.text = self.html.get_text('\n', strip=True)
            self.key_phrases = self.get_key_phrases()

        if not generate_subpages or generate_depth <= 0 or self.html is None:
            self.subpages = None
        else:
            self.subpages = {}
            for link in crawl.get_internal_links(self.html, url):
                if link not in self.subpages:
                    subpage = Page(link, generate_subpages, generate_depth - 1)
                    if subpage.html is not None:
                        self.subpages[link] = (subpage, 1)
                else:
                    self.subpages[link] = (self.subpages[link][0], self.subpages[link][1] + 1)

    def strip_scripts_from_html(self):
        for script in self.html(['script', 'style']):
            script.decompose()

    def get_key_phrases(self):
        r = Rake()
        r.extract_keywords_from_text(self.text)
        return r.get_ranked_phrases()

    def __str__(self):
        if self.html is None:
            return ''
        return self.html.prettify()

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


website = 'http://alanbi.com'
root_page = Page(website)
print(root_page)
keywords = root_page.key_phrases
print(root_page.text)
print(keywords)


