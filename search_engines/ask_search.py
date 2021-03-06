from search_engines.utils import extract_first
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//li[@class="PartialWebPagination-condensed PartialWebPagination-pgsel PartialWebPagination-button"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/@href')),
            'title': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/text()')),
            'preview_text': extract_first(result.xpath('.//p[@class="PartialSearchResults-item-abstract"]/text()')),
            'search_url': search_url,
            'page_number': page_number if page_number else "1",
        } for result in root.xpath('//div[@class="PartialSearchResults-item"]')]
    print(
        f"Extracted {len(results)} results from page {page_number}.")
    next_page_url = extract_first(
        root.xpath('//li[@class="PartialWebPagination-next"]/parent::a/@href'))
    if next_page_url:
        next_page_url = 'https://www.ask.com' + next_page_url
        print(f"Extracted next page url: {next_page_url}")
    else:
        print(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f'https://www.ask.com/web?q={quote(query)}'
