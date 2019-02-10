from visualizer.helpers import relative_to_absolute_url
from visualizer.page import Page, PageNode
from visualizer.website import Website
from flask import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Page):
            if obj.html is None:
                return {'error': obj.error}
            else:
                return {
                    'url': obj.url,
                    'text': obj.text,
                    'key_phrases': obj.key_phrases,
                    'word_count': obj.word_count,
                    'internal_links': set([relative_to_absolute_url(link, obj.url)
                                           for link in obj.internal_links]),
                    'outbound_links': set(obj.outbound_links),
                }
        elif isinstance(obj, Website):
            if obj.root.page.html is None:
                return {'error': obj.root.page.error}
            else:
                return {
                    'pages': obj.pages,
                    'total_word_count': obj.total_word_count,
                    'average_word_count': obj.average_word_count,
                    'outbound_links': obj.outbound_links,
                    'key_phrases': obj.key_phrases,
                    # 'root_page_node': obj.root

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
