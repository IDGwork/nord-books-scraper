from decimal import Decimal

from books_scraper.models.product import Product
from books_scraper.repositories.product_repository import ProductRepository


def test_repository_saves_product(tmp_path) -> None:
    path = tmp_path / "products.json"

    product = Product(
        name="A Light in the Attic",
        availability=22,
        upc="a897fe39b1053632",
        price_excl_tax=Decimal("51.77"),
        tax=Decimal("0.00"),
    )

    repository = ProductRepository(path)
    repository.add(product)

    assert ProductRepository(path).exists(product.upc)
