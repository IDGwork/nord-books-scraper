import asyncio
from pathlib import Path

import grpc

from books_scraper.controllers.parser_controller import ParserController
from books_scraper.proto import product_parser_pb2_grpc
from books_scraper.repositories.product_repository import ProductRepository
from books_scraper.services.parser_service import ParserService

PARSER_ADDRESS = "0.0.0.0:50051"
OUTPUT_PATH = Path("data/products.json")


async def main() -> None:
    controller = ParserController(ParserService(ProductRepository(OUTPUT_PATH)))
    server = grpc.aio.server()

    product_parser_pb2_grpc.add_ProductParserServicer_to_server(controller, server)
    server.add_insecure_port(PARSER_ADDRESS)

    await server.start()
    print(f"Parser listening on {PARSER_ADDRESS}")
    await server.wait_for_termination()


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
