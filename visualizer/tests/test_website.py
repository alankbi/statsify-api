from visualizer.website import Page
import responses


def test_page():
    # tests: html exists, html is None, subpages is none (if false, if <= 0),
    # subpages is size 2 (after implementing unique feature), subpages is size 1
    # and subpages[0].subpages is size 1, and after that .subpages is None,
    # throws Exception if url produces None (after implementing this),
    # subpages length is 0 if all links are bad
    assert True