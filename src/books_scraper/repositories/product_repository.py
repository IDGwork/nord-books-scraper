import json
from pathlib import Path

from books_scraper.models.product import Product


class ProductRepository:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._products = self._load()

    def exists(self, upc: str) -> bool:
        return upc in self._products

    def add(self, product: Product) -> None:
        self._products[product.upc] = product
        self._write()

    def _load(self) -> dict[str, Product]:
        if not self._path.exists():
            return {}

        data = json.loads(self._path.read_text(encoding="utf-8"))
        products = [Product.model_validate(item) for item in data]

        return {product.upc: product for product in products}

    def _write(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [product.model_dump(mode="json") for product in self._products.values()]
        self._path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
