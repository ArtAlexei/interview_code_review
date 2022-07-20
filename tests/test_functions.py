import unittest

from bs4 import BeautifulSoup

from functions import add_symbols_to_text


class TestAddSymbolsToText(unittest.TestCase):
    def test_add_symbol(self):
        html = '<html><body>target - target small words.target</body></html>'
        html_result = '<html><body>target™ - target™ small words.target™</body></html>'
        soup = BeautifulSoup(html, 'lxml')
        soup = add_symbols_to_text(soup)
        self.assertEqual(str(soup), html_result)

    def test_do_not_add_symbol_to_links(self):
        html = '<html><body>target/target/small</body></html>'
        html_result = '<html><body>target/target/small</body></html>'
        soup = BeautifulSoup(html, 'lxml')
        soup = add_symbols_to_text(soup)
        self.assertEqual(str(soup), html_result)


