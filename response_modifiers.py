import http.client as client
import re

from bs4 import BeautifulSoup

from config import NEW_SYMBOL, WORD_TEMPLATE, HOST


def add_content_type_tag(soup: BeautifulSoup) -> BeautifulSoup:
    tag = soup.new_tag('meta')
    tag.attrs['http-equiv'] = 'Content-Type'
    tag.attrs['content'] = 'text/html;charset=utf-8'
    soup.head.insert(1, tag)
    return soup


def replace_absolute_links(soup: BeautifulSoup) -> BeautifulSoup:
    for link in soup.find_all('a', href=True):
        link['href'] = link['href'].replace(HOST, '/')
    return soup


def add_symbols_to_text(soup: BeautifulSoup) -> BeautifulSoup:
    def add_symbol_after_match(match: re.Match) -> str:
        return match.group() + NEW_SYMBOL

    for tag_text in soup.find_all(string=re.compile(WORD_TEMPLATE)):
        new_tag_text = re.sub(WORD_TEMPLATE, add_symbol_after_match, tag_text)
        tag_text.replace_with(new_tag_text)
    return soup


def modify_response(response: client.HTTPResponse) -> str:
    soup = BeautifulSoup(response.read(), 'lxml')
    soup = add_content_type_tag(soup)
    soup = add_symbols_to_text(soup)
    soup = replace_absolute_links(soup)
    return str(soup)
