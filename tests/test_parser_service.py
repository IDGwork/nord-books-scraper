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


async def test_parser_service_saves_and_detects_duplicate(tmp_path) -> None:
    repository = ProductRepository(tmp_path / "products.json")
    service = ParserService(repository)

    assert await service.parse_and_store(PRODUCT_HTML)
    assert not await service.parse_and_store(PRODUCT_HTML)
    assert repository.exists("a897fe39b1053632")
