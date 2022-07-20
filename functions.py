import re

from bs4 import BeautifulSoup

from config import NEW_SYMBOL, REGEX_TO_ADD_AFTER, HOST


def add_symbol_after_match(match: re.Match) -> str:
    text = match.group()
    return text + NEW_SYMBOL


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
    for tag_text in soup.find_all(string=re.compile(REGEX_TO_ADD_AFTER)):
        new_tag_text = re.sub(REGEX_TO_ADD_AFTER, add_symbol_after_match, tag_text)
        tag_text.replace_with(new_tag_text)
    return soup
