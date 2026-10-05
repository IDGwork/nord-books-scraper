from books_scraper.services.product_service import ProductService


class ProductController:
    def __init__(self, service: ProductService) -> None:
        self._service = service

    async def scrape(self) -> tuple[int, int, int]:
        return await self._service.scrape()
