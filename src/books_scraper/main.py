import asyncio
import os

from books_scraper.controllers.product_controller import ProductController
from books_scraper.services.parser_client import ParserClient
from books_scraper.services.product_service import ProductService

PARSER_ADDRESS = os.getenv("PARSER_ADDRESS", "127.0.0.1:50051")


async def main() -> None:
    parser_client = ParserClient(PARSER_ADDRESS)

    try:
        controller = ProductController(ProductService(parser_client))
        discovered, saved, duplicates = await controller.scrape()

        print(f"Discovered: {discovered}")
        print(f"Saved: {saved}")
        print(f"Duplicates: {duplicates}")
    finally:
        await parser_client.close()


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
