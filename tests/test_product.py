from decimal import Decimal

import pytest
from pydantic import ValidationError

from books_scraper.models.product import Product


def test_product_accepts_valid_data() -> None:
    product = Product(
        name="A Light in the Attic",
        availability=22,
        upc="a897fe39b1053632",
        price_excl_tax=Decimal("51.77"),
        tax=Decimal("0.00"),
    )

    assert product.name == "A Light in the Attic"
    assert product.availability == 22


def test_product_rejects_invalid_upc() -> None:
    with pytest.raises(ValidationError):
        Product(
            name="Book",
            availability=1,
            upc="invalid",
            price_excl_tax=Decimal("10.00"),
            tax=Decimal("0.00"),
        )
