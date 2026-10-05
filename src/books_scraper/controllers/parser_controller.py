import grpc

from books_scraper.proto import product_parser_pb2, product_parser_pb2_grpc
from books_scraper.services.parser_service import ParserService


class ParserController(product_parser_pb2_grpc.ProductParserServicer):
    def __init__(self, service: ParserService) -> None:
        self._service = service

    async def ParseAndStore(self, request, context):
        try:
            saved = await self._service.parse_and_store(request.html)
        except ValueError as exc:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))

        if not saved:
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, "Product already exists")

        return product_parser_pb2.ParseProductResponse()
