from search_engines.utils import extract_first, join_all
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(
        root.xpath('//a[@class="sb_pagS sb_pagS_bp b_widePag sb_bp"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath("./h2/a/@href")),
            'title': join_all(result.xpath("./h2/a//text()")),
            'preview_text': join_all(result.xpath("./*[@class='b_caption']/p//text()")),
            'search_url': search_url,
            'page_number': page_number,
        } for result in root.xpath("//*[@class='b_algo']")]
    print(
        f"Extracted {len(results)} results from page {page_number}.")
    # extract url of next page.
    next_page_url = extract_first(root.xpath("//a[@title='Next page']/@href"))
    if next_page_url:
        next_page_url = 'https://www.bing.com' + next_page_url
        print(f"Extracted next page url: {next_page_url}")
    else:
        print(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f'https://www.bing.com/search?q={quote(query)}'
