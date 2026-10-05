import grpc

from books_scraper.proto import product_parser_pb2, product_parser_pb2_grpc


class ParserClient:
    def __init__(self, address: str) -> None:
        self._channel = grpc.aio.insecure_channel(address)
        self._stub = product_parser_pb2_grpc.ProductParserStub(self._channel)

    async def parse_and_store(self, html: str) -> bool:
        request = product_parser_pb2.ParseProductRequest(html=html)

        try:
            await self._stub.ParseAndStore(request)
            return True
        except grpc.aio.AioRpcError as exc:
            if exc.code() == grpc.StatusCode.ALREADY_EXISTS:
                return False

            raise

    async def close(self) -> None:
        await self._channel.close()
