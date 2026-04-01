# CheapProducts

A Django-powered price comparison tool that scrapes multiple UK e-commerce websites in parallel and shows the cheapest products for any search query.

## Supported Sites

| Site | Status | Notes |
|------|--------|-------|
| Amazon UK | Working | Scrapes search results via requests + BeautifulSoup |
| eBay UK | Working | Scrapes search results via requests + BeautifulSoup |
| Etsy UK | Limited | Etsy blocks plain requests (403). Works better with proxies or the Etsy Open API |
| TikTok Shop | Limited | JS-rendered – returns empty with plain requests |
| Facebook Marketplace | Limited | Requires login/auth – returns empty with plain requests |
| Wix eCommerce | Configurable | Needs a specific Wix store URL to be set |
| BigCommerce | Configurable | Needs a specific BigCommerce store URL to be set |

## Quick Start

1. Clone the repo and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/cheapproducts.git
cd cheapproducts
pip install -r requirements.txt
```

2. Apply migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

3. Open http://127.0.0.1:8000/search/ and search for anything (e.g. "toys", "headphones", "shirt").

## How It Works

```
User searches "toys"
        ↓
    views.py → scrapers.py (bridge) → main.py (orchestrator)
                                          ↓
                              ThreadPoolExecutor (7 workers)
                              ┌─────────┬─────────┬─────────┐
                              ↓         ↓         ↓         ↓
                          Amazon UK  eBay UK  Etsy UK  ... (all sites)
                              ↓         ↓         ↓
                           base.py → fetcher.py → parser.py
                                          ↓
                                  selectors.py (CSS config)
                                          ↓
                                Results merged & sorted by price
```

- **fetcher.py** – HTTP layer with User-Agent rotation, retry with backoff, and per-domain rate limiting.
- **parser.py** – BeautifulSoup helpers for extracting text, attributes, and prices.
- **selectors.py** – Centralised CSS selectors for all sites. Update selectors here when a site changes its layout.
- **base.py** – Abstract base class. Every scraper implements `build_search_url()` and `parse_products()`.
- **main.py** – Orchestrator that runs all scrapers in parallel using `ThreadPoolExecutor`.
- **storage.py** – Optional helper to save scraped results into the Django database.

## Adding a New Site

1. Add CSS selectors to `main/scraper/selectors.py`.
2. Create a new scraper file in `main/scraper/sites/` inheriting from `BaseScraper`.
3. Register it in the `SCRAPERS` list in `main/scraper/main.py`.

## Project Structure

```
cheapproducts/          # Django project settings
main/
├── models.py           # Product model
├── views.py            # Search view
├── scrapers.py         # Bridge module (imported by views)
├── scraper/
│   ├── base.py         # Abstract base scraper class
│   ├── fetcher.py      # HTTP client with retries & rate limiting
│   ├── parser.py       # BeautifulSoup parsing helpers
│   ├── selectors.py    # CSS selectors for all sites
│   ├── main.py         # Parallel orchestrator
│   ├── storage.py      # DB persistence (optional)
│   └── sites/          # One file per site
│       ├── amazon_uk.py
│       ├── ebay_uk.py
│       ├── etsy_uk.py
│       ├── tiktok_shop.py
│       ├── facebook_marketplace.py
│       ├── wix.py
│       └── bigcommerce.py
└── templates/
    └── main/
        └── search.html # Search UI
```

## Notes & Caveats

- This uses **requests + BeautifulSoup** (no Selenium needed).
- Sites may change their HTML structure at any time – update CSS selectors in `selectors.py` if parsing breaks.
- Some sites (TikTok Shop, Facebook Marketplace) are heavily JS-rendered and return limited data with plain HTTP requests. For full coverage, consider their official APIs.
- Respect each site's `robots.txt` and terms of service. For production use, consider official APIs or affiliate/partner programs.
