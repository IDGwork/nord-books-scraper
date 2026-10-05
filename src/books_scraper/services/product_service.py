import asyncio
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from books_scraper.services.parser_client import ParserClient
from books_scraper.web import CATALOGUE_NEXT_PAGE, CATALOGUE_PRODUCT_LINK, CATALOGUE_URL

CONCURRENCY = 10


class ProductService:
    def __init__(self, parser_client: ParserClient) -> None:
        self._parser_client = parser_client

    async def scrape(self) -> tuple[int, int, int]:
        async with httpx.AsyncClient(timeout=20) as client:
            urls = await self._discover_product_urls(client)
            semaphore = asyncio.Semaphore(CONCURRENCY)

            async def scrape_product(url: str) -> bool:
                async with semaphore:
                    html = await self._get_html(client, url)
                    return await self._parser_client.parse_and_store(html)

            results = await asyncio.gather(*(scrape_product(url) for url in urls))

        saved = sum(results)
        return len(urls), saved, len(urls) - saved

    async def _discover_product_urls(self, client: httpx.AsyncClient) -> list[str]:
        page_url = CATALOGUE_URL
        urls = []

        while page_url:
            html = await self._get_html(client, page_url)
            page_urls, page_url = self._parse_catalogue(html, page_url)
            urls.extend(page_urls)

        return urls

    @staticmethod
    async def _get_html(client: httpx.AsyncClient, url: str) -> str:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _parse_catalogue(html: str, page_url: str) -> tuple[list[str], str | None]:
        soup = BeautifulSoup(html, "html.parser")
        urls = [urljoin(page_url, link["href"]) for link in soup.select(CATALOGUE_PRODUCT_LINK)]

        next_link = soup.select_one(CATALOGUE_NEXT_PAGE)
        next_page = urljoin(page_url, next_link["href"]) if next_link else None

        return urls, next_page
