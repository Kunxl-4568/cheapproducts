"""
parser.py – shared HTML parsing helpers used by all site scrapers.
"""

import re
from typing import Optional

from bs4 import BeautifulSoup, Tag


def make_soup(html: str) -> BeautifulSoup:
    """Parse *html* with the fast ``lxml`` parser."""
    return BeautifulSoup(html, "lxml")


def text(tag: Optional[Tag], selector: str) -> str:
    """Return stripped text from the first match of *selector* inside *tag*."""
    if tag is None:
        return ""
    el = tag.select_one(selector)
    return el.get_text(strip=True) if el else ""


def attr(tag: Optional[Tag], selector: str, attribute: str) -> str:
    """Return an attribute value from the first match of *selector*."""
    if tag is None:
        return ""
    el = tag.select_one(selector)
    if el is None:
        return ""
    val = el.get(attribute, "")
    return val if isinstance(val, str) else (val[0] if val else "")


def extract_price(raw: str) -> Optional[float]:
    """Pull the first decimal number out of a messy price string like '£12.99'."""
    if not raw:
        return None
    cleaned = raw.replace(",", "")
    match = re.search(r"(\d+\.?\d*)", cleaned)
    if match:
        return float(match.group(1))
    return None


def absolute_url(href: str, base: str) -> str:
    """Ensure *href* is an absolute URL."""
    if not href:
        return ""
    if href.startswith("http"):
        return href
    if href.startswith("//"):
        return "https:" + href
    return base.rstrip("/") + "/" + href.lstrip("/")
