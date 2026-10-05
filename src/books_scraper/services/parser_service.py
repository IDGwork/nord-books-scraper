import asyncio
import re
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup

from books_scraper.models.product import Product
from books_scraper.repositories.product_repository import ProductRepository
from books_scraper.web import PRODUCT_INFORMATION_ROW, PRODUCT_NAME


class ParserService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository
        self._lock = asyncio.Lock()

    async def parse_and_store(self, html: str) -> bool:
        product = await asyncio.to_thread(self._parse_product, html)

        async with self._lock:
            if self._repository.exists(product.upc):
                return False

            await asyncio.to_thread(self._repository.add, product)
            return True

    @staticmethod
    def _parse_product(html: str) -> Product:
        soup = BeautifulSoup(html, "html.parser")
        name = soup.select_one(PRODUCT_NAME)

        if name is None:
            raise ValueError("Invalid product data")

        information = {}

        for row in soup.select(PRODUCT_INFORMATION_ROW):
            header = row.find("th")
            value = row.find("td")

            if header is not None and value is not None:
                information[header.get_text(" ", strip=True)] = value.get_text(" ", strip=True)

        try:
            return Product(
                name=name.get_text(" ", strip=True),
                availability=ParserService._parse_availability(information["Availability"]),
                upc=information["UPC"].lower(),
                price_excl_tax=ParserService._parse_money(information["Price (excl. tax)"]),
                tax=ParserService._parse_money(information["Tax"]),
            )
        except (KeyError, InvalidOperation) as exc:
            raise ValueError("Invalid product data") from exc

    @staticmethod
    def _parse_availability(value: str) -> int:
        match = re.search(r"\d+", value)

        if match is None:
            raise ValueError("Invalid product data")

        return int(match.group())

    @staticmethod
    def _parse_money(value: str) -> Decimal:
        return Decimal(value.replace("£", "").strip())
