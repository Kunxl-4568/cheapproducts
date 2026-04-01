"""
main.py – Orchestrator that runs all registered scrapers concurrently.

Usage from Django views::

    from main.scraper.main import scrape_all
    results = scrape_all("wireless headphones")
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base import BaseScraper
from .sites.amazon_uk import AmazonUKScraper
from .sites.ebay_uk import EbayUKScraper
from .sites.etsy_uk import EtsyUKScraper
from .sites.tiktok_shop import TikTokShopScraper
from .sites.facebook_marketplace import FacebookMarketplaceScraper
from .sites.wix import WixScraper
from .sites.bigcommerce import BigCommerceScraper

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Registry – add new scrapers here to include them in every search.
# ---------------------------------------------------------------------------
SCRAPERS: list[BaseScraper] = [
    AmazonUKScraper(),
    EbayUKScraper(),
    EtsyUKScraper(),
    TikTokShopScraper(),
    FacebookMarketplaceScraper(),
    WixScraper(),          # no-op until base_url is configured
    BigCommerceScraper(),   # no-op until base_url is configured
]

MAX_WORKERS = 7  # one thread per site


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def scrape_all(query: str, sort_by_price: bool = True) -> list[dict]:
    """
    Hit every registered scraper in parallel and return a merged list of
    product dicts, optionally sorted cheapest-first.
    """
    all_results: list[dict] = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        future_to_name = {
            pool.submit(scraper.search, query): scraper.name
            for scraper in SCRAPERS
        }
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                products = future.result()
                all_results.extend(products)
                logger.info("[Orchestrator] %s returned %d products", name, len(products))
            except Exception as exc:
                logger.exception("[Orchestrator] %s raised %s", name, exc)

    if sort_by_price:
        all_results.sort(key=lambda p: p.get("price") or float("inf"))

    return all_results
