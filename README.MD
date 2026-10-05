# nord-books-scraper

An asynchronous Python scraper for [books.toscrape.com](https://books.toscrape.com/) that collects product data, validates it, checks for duplicates, and stores it in JSON.

The scraper downloads product pages and sends the raw HTML to a gRPC parser service, which parses, validates, deduplicates, and stores the products.

## Run

Requires Python 3.11+.

Install:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Start the parser:

```bash
python -m books_scraper.parser_main
```

In another terminal, run the scraper:

```bash
python -m books_scraper.main
```

Run tests:

```bash
pytest -q
```

Scraped products are stored in:

```text
data/products.json
```