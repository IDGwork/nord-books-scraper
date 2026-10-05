import grpc
import pytest

from books_scraper.controllers.parser_controller import ParserController
from books_scraper.proto import product_parser_pb2, product_parser_pb2_grpc
from books_scraper.repositories.product_repository import ProductRepository
from books_scraper.services.parser_service import ParserService

PRODUCT_HTML = """
<html>
    <body>
        <article class="product_page">
            <div class="product_main">
                <h1>A Light in the Attic</h1>
            </div>
            <table class="table table-striped">
                <tr><th>UPC</th><td>a897fe39b1053632</td></tr>
                <tr><th>Price (excl. tax)</th><td>£51.77</td></tr>
                <tr><th>Tax</th><td>£0.00</td></tr>
                <tr><th>Availability</th><td>In stock (22 available)</td></tr>
            </table>
        </article>
    </body>
</html>
"""


async def start_server(path):
    controller = ParserController(ParserService(ProductRepository(path)))
    server = grpc.aio.server()

    product_parser_pb2_grpc.add_ProductParserServicer_to_server(controller, server)
    port = server.add_insecure_port("127.0.0.1:0")

    await server.start()

    channel = grpc.aio.insecure_channel(f"127.0.0.1:{port}")
    stub = product_parser_pb2_grpc.ProductParserStub(channel)

    return server, channel, stub


async def test_invalid_product_returns_invalid_argument(tmp_path) -> None:
    server, channel, stub = await start_server(tmp_path / "products.json")

    try:
        with pytest.raises(grpc.aio.AioRpcError) as error:
            await stub.ParseAndStore(product_parser_pb2.ParseProductRequest(html="<html></html>"))

        assert error.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    finally:
        await channel.close()
        await server.stop(None)


async def test_duplicate_product_returns_already_exists(tmp_path) -> None:
    server, channel, stub = await start_server(tmp_path / "products.json")
    request = product_parser_pb2.ParseProductRequest(html=PRODUCT_HTML)

    try:
        await stub.ParseAndStore(request)

        with pytest.raises(grpc.aio.AioRpcError) as error:
            await stub.ParseAndStore(request)

        assert error.value.code() == grpc.StatusCode.ALREADY_EXISTS
    finally:
        await channel.close()
        await server.stop(None)
