from visualizer import crawl
from rake_nltk import Rake


class Page:
    def __init__(self, url, generate_subpages=False, generate_depth=1):
        self.url = url
        self.html = crawl.get_html(url)

        if self.html is not None:
            self.strip_scripts_from_html()
            self.text = self.html.get_text('\n', strip=True)
            self.key_phrases = self.get_key_phrases(max_length=3)

            self.word_count = self.get_word_count()

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

    def strip_scripts_from_html(self):
        for script in self.html(['script', 'style']):
            script.decompose()

    def get_key_phrases(self, max_length=None):
        if max_length is not None:
            r = Rake(max_length=max_length)
        else:
            r = Rake()
        r.extract_keywords_from_text(self.text)
        return self.filter_key_phrases(r.get_ranked_phrases())

    def filter_key_phrases(self, phrases):
        return [phrase.title() for phrase in phrases[:3]]

    def get_word_count(self):
        return len(self.text.split())

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
print(root_page.text)

print(root_page.key_phrases)

print(root_page.word_count)

print(root_page.internal_links)
print(root_page.outbound_links)
