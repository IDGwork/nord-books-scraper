from books_scraper.services.product_service import ProductService

CATALOGUE_HTML = """
<html>
    <body>
        <ol class="row">
            <article class="product_pod">
                <h3><a href="book-one_1/index.html">Book One</a></h3>
            </article>
            <article class="product_pod">
                <h3><a href="book-two_2/index.html">Book Two</a></h3>
            </article>
        </ol>
    </body>
</html>
"""

PRODUCT_HTML = """
<html>
    <body>
        <article class="product_page"></article>
    </body>
</html>
"""


class FakeParserClient:
    def __init__(self) -> None:
        self.received = []

    async def parse_and_store(self, html: str) -> bool:
        self.received.append(html)
        return True


async def test_product_service_scrapes_products(monkeypatch) -> None:
    async def get_html(client, url):
        return CATALOGUE_HTML if url.endswith("page-1.html") else PRODUCT_HTML

    monkeypatch.setattr(ProductService, "_get_html", staticmethod(get_html))

    parser_client = FakeParserClient()
    result = await ProductService(parser_client).scrape()

    assert result == (2, 2, 0)
    assert len(parser_client.received) == 2
