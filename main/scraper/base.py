"""
base.py – Abstract base class for every site scraper.

New sites only need to subclass ``BaseScraper`` and implement:
  • build_search_url(query)  – return the search URL for the query.
  • parse_products(html)     – return a list of product dicts.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Optional

from .fetcher import fetch
from .selectors import SELECTORS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lightweight product data container
# ---------------------------------------------------------------------------
@dataclass
class ProductResult:
    title: str
    price: Optional[float]
    image: str = ""
    url: str = ""
    description: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Abstract base scraper
# ---------------------------------------------------------------------------
class BaseScraper(ABC):
    """Every site scraper inherits from this class."""

    name: str = "base"           # human-readable site name
    site_key: str = "base"       # key into SELECTORS dict
    base_url: str = ""           # e.g. "https://www.amazon.co.uk"
    max_products: int = 20       # cap per search

    @property
    def selectors(self) -> dict[str, str]:
        return SELECTORS.get(self.site_key, {})

    # -- Must override --------------------------------------------------
    @abstractmethod
    def build_search_url(self, query: str) -> str: ...

    @abstractmethod
    def parse_products(self, html: str) -> list[ProductResult]: ...

    # -- Common workflow ------------------------------------------------
    def search(self, query: str) -> list[dict]:
        """Fetch the search page and return parsed products as dicts."""
        url = self.build_search_url(query)
        logger.info("[%s] Searching: %s", self.name, url)
        html = fetch(url)
        if not html:
            logger.warning("[%s] Empty response for query '%s'", self.name, query)
            return []
        try:
            products = self.parse_products(html)
        except Exception as exc:
            logger.exception("[%s] Parse error: %s", self.name, exc)
            return []
        results = [p.to_dict() for p in products[: self.max_products]]
        logger.info("[%s] Found %d products", self.name, len(results))
        return results
