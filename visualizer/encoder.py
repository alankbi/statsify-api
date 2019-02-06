from visualizer.page import Page, PageNode
from visualizer.website import Website
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Page):
            return {
                'url': obj.url,
                'text': obj.text,
                'key_phrases': obj.key_phrases,
                'word_count': obj.word_count,
                'internal_links': obj.internal_links,
                'outbound_links': obj.outbound_links,
            }
        elif isinstance(obj, Website):
            return {
                'pages': obj.pages,
                'total_word_count': obj.total_word_count,
                'average_word_count': obj.average_word_count,
                'outbound_links': obj.outbound_links,
                'key_phrases': obj.key_phrases,
                'root_page': obj.root

            }
        elif isinstance(obj, PageNode):
            return {
                'page': obj.page,
                'subpages': obj.subpages,
            }
        elif isinstance(obj, set):
            return list(obj)
        else:
            super().default(obj)
