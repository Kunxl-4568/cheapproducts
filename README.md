Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Apply migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

3. Open http://127.0.0.1:8000/search/ and try a query (example: "shirt", "bag").

Notes

- This project includes a simple demo scraper that uses the public FakeStore API and returns cheapest matching items.
- For production or real e-commerce sites, implement site-specific scrapers in `main/scrapers.py`. Selenium-based scrapers are hinted at but require driver setup.
 - For production or real e-commerce sites, implement site-specific scrapers in `main/scrapers.py`.
 - The project now includes Selenium-capable multi-site scrapers. To use Selenium (recommended for real sites), install drivers and run with the instructions below.

Selenium setup (Windows / Chrome)

1. Install dependencies (in virtualenv):

```bash
pip install -r requirements.txt
```

2. Run the dev server (ChromeDriver will be downloaded automatically by webdriver-manager when first used):

```bash
python manage.py runserver
```

3. Use the search UI at `http://127.0.0.1:8000/search/?q=your+query`.

Notes and caveats

- The built-in Selenium scrapers target eBay, BestBuy, and Walmart with heuristic selectors. Selectors may need updates per region/site UI changes.
- Sites may block automated access; respect robots.txt and site terms. For reliable production scraping, consider using official APIs or partner programs.
- If Selenium or a driver isn't available, the app falls back to a demo FakeStore API so the UI remains functional.
