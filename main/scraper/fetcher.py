"""
fetcher.py – HTTP layer for the scraping system.

Responsibilities:
  • Rotate User-Agent headers to reduce blocking.
  • Retry failed requests with exponential back-off.
  • Per-domain rate-limiting (polite crawling).
"""

import random
import time
import logging
from typing import Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# User-Agent pool – keeps requests looking like normal browser traffic
# ---------------------------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
]

DEFAULT_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ---------------------------------------------------------------------------
# Simple per-domain rate limiter
# ---------------------------------------------------------------------------
_domain_last_request: dict[str, float] = {}
_MIN_DELAY = 1.5  # seconds between requests to the same domain


def _rate_limit(url: str) -> None:
    domain = urlparse(url).netloc
    now = time.monotonic()
    last = _domain_last_request.get(domain, 0.0)
    wait = _MIN_DELAY - (now - last)
    if wait > 0:
        time.sleep(wait)
    _domain_last_request[domain] = time.monotonic()


# ---------------------------------------------------------------------------
# Session factory with automatic retries
# ---------------------------------------------------------------------------
def _build_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


_session = _build_session()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def fetch(url: str, extra_headers: Optional[dict] = None, timeout: int = 15) -> Optional[str]:
    """Fetch *url* and return the response text, or ``None`` on failure."""
    _rate_limit(url)
    headers = {**DEFAULT_HEADERS, "User-Agent": random.choice(USER_AGENTS)}
    if extra_headers:
        headers.update(extra_headers)
    try:
        resp = _session.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as exc:
        logger.warning("Fetch failed for %s: %s", url, exc)
        return None
