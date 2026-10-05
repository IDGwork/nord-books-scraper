# nord-books-scraper

An asynchronous Python scraper for [books.toscrape.com](https://books.toscrape.com/) that collects:

- Name
- Availability
- UPC
- Price excluding tax
- Tax

The scraper discovers and downloads product pages asynchronously and sends the raw HTML to a separate gRPC parser service.

The parser service parses the HTML, validates products with Pydantic, checks for duplicate UPCs, and stores validated products in:

```text
data/products.json
```

The application uses a simple Controller → Service → Repository structure.

## Run

Requires Python 3.11+.

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

A clean run should produce approximately:

```text
Discovered: 1000
Saved: 1000
Duplicates: 0
```

Running the scraper again against the same JSON file should produce:

```text
Discovered: 1000
Saved: 0
Duplicates: 1000
```

## Tests

Run:

```bash
pytest -q
```

The tests cover product validation, JSON persistence, scraping logic, duplicate detection, and gRPC response codes.

For a clean end-to-end test:

```bash
rm -f data/products.json
```

Start the parser and scraper again and verify that `data/products.json` contains the scraped products.

## Docker

Build both applications:

```bash
docker build -f Dockerfile.parser -t nord-books-parser .
docker build -f Dockerfile.scraper -t nord-books-scraper .
```

The parser is a long-running service, while the scraper is designed as a scheduled job.

## Kubernetes

The Kubernetes configuration is in:

```text
k8s/app.yaml
```

It contains:

- a parser Deployment
- a parser Service
- a PersistentVolumeClaim for JSON storage
- a scraper CronJob

Apply it with:

```bash
kubectl apply -f k8s/app.yaml
```

The scraper CronJob communicates with the parser through `parser:50051`.

## Possible issues and improvements

- **JSON persistence does not scale well.** The repository rewrites the JSON file when products are added and the parser is intended to run as a single instance. For a distributed production system, this could be replaced with a database providing atomic uniqueness on UPC.
- **The scraper depends on the website HTML structure.** Changes to the catalogue or product selectors could break parsing. Additional selector validation and monitoring could make failures easier to detect.
- **HTTP requests currently have basic error handling.** Production use could add retry policies, exponential backoff, rate limiting, and structured logging.
- **gRPC uses an insecure internal channel.** TLS and authentication could be added if communication crossed a trusted internal boundary.