"""
scrapers.py – Bridge module imported by views.py.

Delegates to the scraper package orchestrator so the view layer stays clean.
"""

from .scraper.main import scrape_all


def search_products(query: str) -> list[dict]:
    """Run all scrapers and return results sorted cheapest-first."""
    return scrape_all(query, sort_by_price=True)
