import unittest

from bs4 import BeautifulSoup

from functions import add_symbols_to_text, replace_absolute_links


class TestAddSymbolsToText(unittest.TestCase):
    def test_add_symbol(self):
        html = '<html><body>target - target small words.target</body></html>'
        html_result = '<html><body>target™ - target™ small words.target™</body></html>'
        soup = add_symbols_to_text(BeautifulSoup(html, 'lxml'))
        self.assertEqual(str(soup), html_result)

    def test_do_not_add_symbol_to_links(self):
        html = '<html><body>target/target/small</body></html>'
        html_result = '<html><body>target/target/small</body></html>'
        soup = add_symbols_to_text(BeautifulSoup(html, 'lxml'))
        self.assertEqual(str(soup), html_result)


class TestReplaceAbsoluteLinks(unittest.TestCase):
    def test_replace_absolute_links(self):
        html = '<html><body><a href="https://news.ycombinator.com"></a></body></html>'
        html_result = '<html><body><a href="/"></a></body></html>'
        soup = replace_absolute_links(BeautifulSoup(html, 'lxml'))
        self.assertEqual(str(soup), html_result)
