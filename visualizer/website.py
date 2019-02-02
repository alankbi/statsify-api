class Website:
    def __init__(self, root_page):
        self.root_page = root_page
        if root_page is not None:
            self.pages = None   # { url: (Page, frequency) }
            self.text = None    # Large string
            self.key_phrases = None
            self.word_count = None

            self.outbound_links = None
